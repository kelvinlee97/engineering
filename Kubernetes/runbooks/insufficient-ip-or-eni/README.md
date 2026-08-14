# Kubernetes IP or ENI Exhaustion Scheduling Failure Runbook

Chinese version: [README_ZH.md](README_ZH.md)

Use this generic runbook when Pods remain `Pending` and scheduler events report `InsufficientIPOrENI`, an ENI/IP extended-resource shortage, or a missing Pod subnet in an ENI-based Kubernetes network. It is written for Tencent Kubernetes Engine (TKE) VPC-CNI as a concrete example, but all environment values are placeholders and must be confirmed from the active cluster configuration.

TKE documents that, in VPC-CNI mode, Pod IPs are allocated from Pod subnets and a node's schedulable Pod count is constrained by its supported ENIs and IPs. Nodes and Pod subnets must also be in the same availability zone. See [TKE container network overview](https://intl.cloud.tencent.com/document/product/457/38966) and [TKE cluster network planning](https://cloud.tencent.com/document/product/457/106706).

## Contents

- [Safety boundary](#safety-boundary)
- [Collect symptoms and capacity evidence](#collect-symptoms-and-capacity-evidence)
- [Classify the failure](#classify-the-failure)
- [Remediate in dependency order](#remediate-in-dependency-order)
- [Restart workloads only when required](#restart-workloads-only-when-required)
- [Acceptance criteria](#acceptance-criteria)
- [Prevention and incident record](#prevention-and-incident-record)

## Safety Boundary

Do not treat all `Pending` Pods as an IP or ENI problem. A `node.kubernetes.io/unreachable` taint, for example, indicates a node-health path that must be investigated separately. DaemonSet Pods receive some automatic tolerations, but these do not prove that a node is healthy or has available network resources. See the Kubernetes [DaemonSet documentation](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/).

Before making a change, establish change authority and record the active cluster, network mode, affected availability zone, and maintenance window locally. Do not commit those values.

- Do not add a subnet before confirming that it belongs to the cluster VPC, is intended for Pod allocation, and is in the affected node availability zone.
- Do not expand node capacity before distinguishing subnet-IP exhaustion from node ENI/IP allocatable exhaustion.
- Do not delete business Pods merely to make a scheduler event disappear.
- Do not run a broad `rollout restart` before checking workload replicas, update strategy, availability requirements, and the rollback path.
- Do not publish cluster IDs, VPC or subnet IDs, CIDRs, account IDs, hostnames, business names, screenshots, or internal-console URLs.

The optional capacity numbers in a local operating policy (for example, a utilization target or IP buffer) are not Kubernetes or TKE product guarantees. Set them from measured workload demand and approved service objectives.

## Collect Symptoms and Capacity Evidence

Start with read-only evidence. Replace every placeholder only in the authorized incident environment.

```bash
kubectl get pods -A --field-selector=status.phase=Pending
kubectl get events -A --sort-by=.lastTimestamp
kubectl describe pod <pod-name> -n <namespace>
kubectl get nodes -L topology.kubernetes.io/zone
kubectl describe node <node-name>
```

Capture the exact scheduler messages, then compare the Pod's requested extended resources to the candidate node's allocatable resources:

```bash
kubectl get pod <pod-name> -n <namespace> \
  -o jsonpath='{range .spec.containers[*]}{.name}{"\t"}{.resources.requests}{"\n"}{end}'

kubectl get node <node-name> \
  -o jsonpath='{.status.allocatable}{"\n"}'
```

For TKE VPC-CNI, the `tke-eni-ip-webhook` can add an extended request such as `tke.cloud.tencent.com/eni-ip`; TKE documents this admission behavior and the corresponding resource names in its [webhook documentation](https://cloud.tencent.com/document/product/457/123793). Confirm the actual request and allocatable keys in the affected cluster rather than assuming the key or network mode.

Also collect, through the approved cloud-console or API workflow:

- Pod subnet association with the cluster and VPC.
- Node and Pod subnet availability zones.
- Remaining allocatable IP addresses in the affected Pod subnet.
- Node ENI and secondary-IP limits for the actual instance type.
- CNI/IPAM component health and relevant control-plane or cloud-API errors.

## Classify the Failure

Use the following decision order. Multiple conditions can coexist; clear each condition before closing the incident.

```text
Pod remains Pending
    |
    +-- Candidate node NotReady or unreachable?
    |       +-- Yes: restore node health first; do not label this only as ENI/IP exhaustion.
    |
    +-- Pod subnet missing from the affected availability zone or cluster?
    |       +-- Yes: add an approved, same-zone Pod subnet through change control.
    |
    +-- Pod subnet has insufficient available IPs?
    |       +-- Yes: extend approved Pod-subnet capacity, then confirm IPAM recognizes it.
    |
    +-- Node extended-resource allocatable capacity exhausted?
    |       +-- Yes: add nodes or use an approved node shape/density plan.
    |
    +-- No clear shortage?
            +-- Inspect CNI/IPAM, admission webhook, and cloud API errors before retrying.
```

Do not infer a cause from one event string alone. Correlate scheduler events, node taints and readiness, subnet state, available IP count, extended resource requests, and allocatable capacity.

## Remediate in Dependency Order

### 1. Resolve node-health blockers

If candidate nodes are `NotReady` or unreachable, follow the approved node-health runbook first. Record the taint, condition, and recovery evidence. Do not use an unreachable-node toleration as a substitute for restoring node health.

### 2. Make Pod subnet capacity usable

If the required Pod subnet is not associated with the cluster or is unavailable in the affected availability zone, add a subnet only through the approved cloud change process. Verify all of the following before proceeding:

- The subnet belongs to the cluster VPC and is reserved for the intended Pod networking use.
- Its availability zone matches the affected worker nodes.
- It does not overlap existing Node, Pod, or Service address ranges.
- It has sufficient free IPs for the approved near-term workload and failure buffer.
- The cluster's CNI/IPAM components have observed the change.

TKE's network-planning documentation states that extra Pod subnets can address a Pod-subnet IP shortage in VPC-CNI mode; it also describes the availability-zone constraint. This confirms the mechanism, not a universal sizing formula. Use your own approved capacity calculation.

### 3. Restore node ENI/IP headroom

If the subnet has free addresses but node `allocatable` ENI/IP capacity is exhausted, use the approved node-pool scaling or instance-type workflow. Avoid routing new workload to known-exhausted nodes while capacity is added; any temporary taint must be documented, scoped, and removed after validation.

After each infrastructure change, create or observe a low-risk, authorized workload in the affected availability zone before restarting production workloads. Confirm it is scheduled, receives an IP, and does not generate a new network-resource scheduling event.

### 4. Investigate IPAM and admission components when capacity appears healthy

When the subnet and node capacities appear sufficient, inspect the cluster's CNI/IPAM and admission components. In TKE VPC-CNI, the documented components include `tke-eni-ipamd` and `tke-eni-agent`; do not restart or reconfigure them blindly. Preserve sanitized error signatures and escalate with the cloud provider if the control plane or cloud API cannot allocate capacity.

## Restart Workloads Only When Required

Adding capacity does not automatically justify restarting every workload. Restart only the affected workload when a fresh reconciliation is necessary and the service owner has approved the impact.

Before a restart, inspect replica availability and update policy:

```bash
kubectl get deployment <deployment-name> -n <namespace> -o yaml
kubectl get daemonset <daemonset-name> -n <namespace> -o yaml
kubectl get statefulset <statefulset-name> -n <namespace> -o yaml
kubectl get pdb -n <namespace>
```

For an approved rolling restart:

```bash
kubectl rollout restart deployment/<deployment-name> -n <namespace>
kubectl rollout status deployment/<deployment-name> -n <namespace>

kubectl rollout restart daemonset/<daemonset-name> -n <namespace>
kubectl rollout status daemonset/<daemonset-name> -n <namespace>

kubectl rollout restart statefulset/<statefulset-name> -n <namespace>
kubectl rollout status statefulset/<statefulset-name> -n <namespace>
```

`kubectl rollout restart` supports Deployments, DaemonSets, and StatefulSets; see the [kubectl reference](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/kubectl_rollout_restart/). PodDisruptionBudgets constrain some voluntary disruptions, but Kubernetes documents that direct deletion of Pods or Deployments can bypass them. Treat PDBs as one input to the operational decision, not as a blanket restart safety guarantee. See [Disruptions](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/).

## Acceptance Criteria

Do not close the incident until the authorized evidence shows all applicable conditions:

- Affected nodes are `Ready`, and any blocking taint is understood, removed, or intentionally retained.
- The cluster has a usable, same-zone Pod subnet with enough approved capacity.
- Node ENI/IP extended-resource capacity is no longer exhausted.
- An authorized new Pod can schedule and obtain network resources in the affected availability zone.
- Each affected DaemonSet reaches `DESIRED = CURRENT = READY`.
- Each restarted Deployment or StatefulSet completes its rollout and its service-specific health check passes.
- New scheduler events do not show `InsufficientIPOrENI` during the agreed observation period.
- The incident record distinguishes observed evidence, completed actions, and actions still pending validation.

Useful workload checks include:

```bash
kubectl get pods -n <namespace> -o wide
kubectl get daemonset <daemonset-name> -n <namespace>
kubectl rollout history deployment/<deployment-name> -n <namespace>
kubectl get events -A --sort-by=.lastTimestamp
```

## Prevention and Incident Record

Monitor capacity by availability zone, rather than only at cluster level:

- Free IP addresses in every Pod subnet.
- ENI/IP extended-resource allocatable versus requested capacity on each node pool.
- Pending Pods and scheduler events grouped by reason and availability zone.
- CNI/IPAM allocation errors and cloud API failures.

For a reusable incident record, store only sanitized evidence: the error signature, resource types, capacity trend, node and Pod conditions, completed change class, rollout outcome, and observation period. Keep environment identifiers, raw logs, command history, and screenshots in the authorized internal incident system rather than this public repository.
