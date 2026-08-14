# Kubernetes IP 或 ENI 耗尽导致的调度失败手册

English version: [README.md](README.md)

当 Pod 长时间处于 `Pending`，且 scheduler event 出现 `InsufficientIPOrENI`、ENI/IP 扩展资源不足，或 ENI 型 Pod 网络缺少容器子网时，可使用本通用手册。本文以腾讯云容器服务（TKE）的 VPC-CNI 为具体示例；所有环境值均为占位符，必须以实际集群生效配置为准。

TKE 文档说明：在 VPC-CNI 模式下，Pod IP 从容器子网分配；一个节点可调度的 Pod 数量受该节点支持的 ENI 和 IP 数量限制；节点与容器子网还必须位于相同可用区。参考 [TKE 容器网络概述](https://intl.cloud.tencent.com/zh/document/product/457/38966) 和 [TKE 容器集群网络规划](https://cloud.tencent.com/document/product/457/106706)。

## 目录

- [安全边界](#安全边界)
- [收集症状与容量证据](#收集症状与容量证据)
- [故障分类](#故障分类)
- [按依赖顺序处置](#按依赖顺序处置)
- [仅在需要时重启工作负载](#仅在需要时重启工作负载)
- [验收条件](#验收条件)
- [预防与事故记录](#预防与事故记录)

## 安全边界

不要把所有 `Pending` Pod 都归因为 IP 或 ENI 问题。例如，`node.kubernetes.io/unreachable` taint 表示节点健康路径，必须单独排查。DaemonSet Pod 虽会自动获得部分 toleration，但这不代表节点健康，也不代表网络资源充足。参见 Kubernetes [DaemonSet 文档](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/)。

变更前，应在本地记录已生效的集群、网络模式、受影响可用区和维护窗口，并确认变更授权；不得提交这些实际值。

- 未确认子网属于集群 VPC、用于 Pod 分配且位于受影响节点可用区前，不要添加子网。
- 未区分容器子网 IP 耗尽和节点 ENI/IP allocatable 耗尽前，不要扩容节点。
- 不要为了让 scheduler event 消失而删除业务 Pod。
- 未检查副本数、更新策略、可用性要求和回滚路径前，不要大范围执行 `rollout restart`。
- 不要公开 cluster ID、VPC/subnet ID、CIDR、账号 ID、主机名、业务名、截图或内部控制台 URL。

本地运维策略中的容量数字（例如使用率目标或 IP 预留）不是 Kubernetes 或 TKE 的产品保证。应根据实测工作负载需求和已批准的服务目标设置。

## 收集症状与容量证据

先收集只读证据。所有占位符只能在获授权的事故环境中替换。

```bash
kubectl get pods -A --field-selector=status.phase=Pending
kubectl get events -A --sort-by=.lastTimestamp
kubectl describe pod <pod-name> -n <namespace>
kubectl get nodes -L topology.kubernetes.io/zone
kubectl describe node <node-name>
```

记录原始 scheduler message 后，将 Pod 请求的扩展资源与候选 Node 的 allocatable 资源对比：

```bash
kubectl get pod <pod-name> -n <namespace> \
  -o jsonpath='{range .spec.containers[*]}{.name}{"\t"}{.resources.requests}{"\n"}{end}'

kubectl get node <node-name> \
  -o jsonpath='{.status.allocatable}{"\n"}'
```

对于 TKE VPC-CNI，`tke-eni-ip-webhook` 可能会为 Pod 添加 `tke.cloud.tencent.com/eni-ip` 一类扩展资源 request。TKE 在 [webhook 文档](https://cloud.tencent.com/document/product/457/123793) 中说明了此 admission 行为和相关资源名。必须查看实际 Pod request、Node allocatable 和网络模式，不能假定资源 key 或网络模式。

还应通过获批准的云控制台或 API 流程收集：

- 容器子网与集群、VPC 的关联状态。
- Node 与 Pod subnet 的可用区。
- 受影响 Pod subnet 剩余可分配 IP。
- 实际实例规格的 ENI 与辅助 IP 限额。
- CNI/IPAM 组件健康状态，以及关联 control-plane 或 cloud API 错误。

## 故障分类

按以下顺序判断。多个条件可能同时存在；所有条件都清除前不得关闭事故。

```text
Pod 持续 Pending
    |
    +-- 候选节点 NotReady 或 unreachable？
    |       +-- 是：先恢复节点健康，不能仅标记为 ENI/IP 耗尽。
    |
    +-- 受影响可用区或集群未关联 Pod subnet？
    |       +-- 是：按变更流程添加同可用区的获批准 Pod subnet。
    |
    +-- Pod subnet 的可用 IP 不足？
    |       +-- 是：扩展获批准的 Pod subnet 容量，再确认 IPAM 已识别。
    |
    +-- Node 的扩展资源 allocatable 已耗尽？
    |       +-- 是：扩容节点，或执行获批准的实例规格/Pod 密度方案。
    |
    +-- 未发现明确容量不足？
            +-- 在重试前检查 CNI/IPAM、admission webhook 与 cloud API 错误。
```

不要只凭一条 event 推断根因。应关联 scheduler event、Node taint 和 Ready 状态、subnet 状态、可用 IP 数、扩展资源 request，以及 allocatable 容量。

## 按依赖顺序处置

### 1. 先解除节点健康阻塞

候选 Node 处于 `NotReady` 或 unreachable 时，先按已批准的节点健康手册处理。记录 taint、condition 和恢复证据。不要用对 unreachable Node 的 toleration 替代节点健康恢复。

### 2. 让 Pod subnet 容量可用

若所需 Pod subnet 未关联集群，或不在受影响可用区内，只能通过获批准的云变更流程添加子网。继续前必须确认：

- 子网属于集群 VPC，且已预留作预期 Pod 网络用途。
- 子网可用区与受影响 worker node 一致。
- 它不与现有 Node、Pod 或 Service 地址范围重叠。
- 它具有满足获批准的近期负载和故障预留的可用 IP。
- 集群 CNI/IPAM 组件已观察到该变更。

TKE 网络规划文档确认，在 VPC-CNI 模式下可通过添加容器子网处理 Pod subnet IP 不足，并说明了可用区约束。该文档确认的是机制，不是通用的容量计算公式；应使用自己的获批准容量计算。

### 3. 恢复节点 ENI/IP 余量

若子网仍有可用 IP，但 Node `allocatable` ENI/IP 已耗尽，应通过获批准的节点池扩容或实例规格流程处理。在容量加入前，避免新工作负载继续进入已耗尽节点；若使用临时 taint，必须记录范围、原因，并在验证后移除。

每次基础设施变更后，先在受影响可用区创建或观察一个低风险、已获授权的工作负载，再重启生产工作负载。确认它能够调度、获得 IP，且没有产生新的网络资源调度 event。

### 4. 容量看似正常时检查 IPAM 与 admission 组件

若子网与 Node 容量看似充足，检查集群 CNI/IPAM 与 admission 组件。在 TKE VPC-CNI 中，文档列出的组件包括 `tke-eni-ipamd` 与 `tke-eni-agent`；不要盲目重启或修改它们。保留脱敏错误特征；若 control plane 或 cloud API 无法分配容量，应向云厂商升级处理。

## 仅在需要时重启工作负载

增加容量不等于必须重启全部工作负载。仅当需要重新协调，且服务 owner 已批准影响时，才重启受影响 workload。

重启前检查副本可用性和更新策略：

```bash
kubectl get deployment <deployment-name> -n <namespace> -o yaml
kubectl get daemonset <daemonset-name> -n <namespace> -o yaml
kubectl get statefulset <statefulset-name> -n <namespace> -o yaml
kubectl get pdb -n <namespace>
```

获批准后的滚动重启：

```bash
kubectl rollout restart deployment/<deployment-name> -n <namespace>
kubectl rollout status deployment/<deployment-name> -n <namespace>

kubectl rollout restart daemonset/<daemonset-name> -n <namespace>
kubectl rollout status daemonset/<daemonset-name> -n <namespace>

kubectl rollout restart statefulset/<statefulset-name> -n <namespace>
kubectl rollout status statefulset/<statefulset-name> -n <namespace>
```

`kubectl rollout restart` 支持 Deployment、DaemonSet 和 StatefulSet，参见 [kubectl reference](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/kubectl_rollout_restart/)。PodDisruptionBudget 会约束部分自愿中断，但 Kubernetes 文档明确说明直接删除 Pod 或 Deployment 可能绕过它。PDB 只是运维决策的一个输入，不能当作重启一定安全的保证。参见 [Disruptions](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/)。

## 验收条件

只有获授权证据显示以下适用条件全部满足，才可关闭事故：

- 受影响 Node 为 `Ready`，所有阻塞 taint 已被解释、移除或有意保留。
- 集群拥有可用、同可用区且容量足够的 Pod subnet。
- Node ENI/IP 扩展资源不再耗尽。
- 一个已获授权的新 Pod 能在受影响可用区成功调度并获取网络资源。
- 每个受影响 DaemonSet 均达到 `DESIRED = CURRENT = READY`。
- 每个已重启 Deployment 或 StatefulSet 均完成 rollout，且通过服务专属健康检查。
- 约定观察期内不再出现 `InsufficientIPOrENI` scheduler event。
- 事故记录明确区分已观察证据、已完成动作，以及仍待验证的动作。

常用工作负载检查：

```bash
kubectl get pods -n <namespace> -o wide
kubectl get daemonset <daemonset-name> -n <namespace>
kubectl rollout history deployment/<deployment-name> -n <namespace>
kubectl get events -A --sort-by=.lastTimestamp
```

## 预防与事故记录

应按可用区监控容量，而不是只看集群总体：

- 每个 Pod subnet 的可用 IP。
- 每个节点池的 ENI/IP 扩展资源 allocatable 与 request。
- 按原因、可用区聚合的 Pending Pod 与 scheduler event。
- CNI/IPAM 分配错误和 cloud API 失败。

可复用事故记录只应保存脱敏证据：错误特征、资源类型、容量趋势、Node/Pod condition、已完成的变更类别、rollout 结果和观察期。真实环境标识、原始日志、命令历史和截图应保留在获授权的内部事故系统，不应进入公开仓库。
