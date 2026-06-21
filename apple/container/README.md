# Apple Container 项目解读

## 项目定位

**apple/container** 是苹果官方开发的 **macOS 原生容器工具**，用 Swift 编写，专为 Apple Silicon (M1/M2/M3/M4) 优化。

**核心思路**：不像 Docker Desktop 那样运行一个庞大的 Linux VM 来托管所有容器，而是 **每个容器运行在独立的轻量级虚拟机中**。

---

## 架构设计

```
┌─────────────────────────────────────────────┐
│          container CLI (Swift)              │
│                   │                         │
│         container-apiserver (launchd)       │
│              ┌────┴────┐                   │
│   container-core-images  container-network  │
│   (镜像管理 XPC helper)  (网络 XPC helper) │
└─────────────────────────────────────────────┘
         │                    │
    ┌────▼────┐        ┌───▼────┐
    │ Container│        │ Container│
    │ VM 1    │        │ VM 2    │
    │(轻量VM) │        │(轻量VM) │
    └─────────┘        └─────────┘
```

### 核心组件

| 组件 | 职责 |
|------|------|
| `container` CLI | 用户命令行接口，管理容器、镜像、网络 |
| `container-apiserver` | launchd 管理的服务进程，提供客户端 API |
| `container-core-images` | XPC helper，管理镜像和本地内容存储 |
| `container-network-vmnet` | XPC helper，管理虚拟网络 |
| `container-runtime-linux` | 每个容器一个，管理该容器的运行时 API |

### 关键技术栈

- **Virtualization.framework** — 管理 Linux VM 和 attached devices
- **vmnet.framework** — 管理虚拟网络
- **XPC** — 进程间通信
- **Launchd** — 服务管理
- **Keychain** — 存储 registry 凭证
- **统一日志系统** — 应用日志

---

## 核心特点

| 特点 | 说明 |
|------|------|
| **强隔离** | 每个容器 = 独立 VM，隔离性和完整 VM 一样 |
| **隐私** | 只挂载必要数据到每个 VM，而非全部共享 |
| **快速启动** | 定制优化 Linux 内核 + 最小根文件系统，子秒级启动 |
| **OCI 兼容** | 完全兼容 OCI 镜像标准，可和 Docker 互操作 |
| **Rosetta 2** | 支持在 Apple Silicon 上运行 `linux/amd64` 容器 |

---

## 项目结构

### apple/container

CLI 工具，用户直接使用的命令。

**安装：**
```bash
# 从 Release 页面下载 .pkg 后安装
sudo installer -pkg container-*.pkg -target /

# 启动服务
container system start
```

**主要命令：**
```bash
container run              # 运行容器
container build            # 构建镜像
container push/pull        # 推送/拉取镜像
container machine          # 管理持久化 Linux VM（新特性）
container network          # 管理虚拟网络
container system           # 启动/停止系统服务
```

### apple/containerization

底层 Swift 包，提供核心 API 能力：

1. **OCI 镜像管理** — 创建、读取、修改 OCI 标准镜像
2. **远程仓库交互** — 支持 Docker Hub、私有 registry
3. **文件系统创建** — 创建和填充 ext4 文件系统
4. **轻量虚拟机管理** — 创建轻量 VM，管理容器运行时环境
5. **容器进程交互** — 启动容器化进程并与之交互
6. **vminitd** — 内置轻量 init 系统，作为 VM 的初始进程，通过 vsock 提供 gRPC API

---

## 和 Docker Desktop 的核心区别

| 对比维度 | Docker Desktop | apple/container |
|---------|---------------|-----------------|
| VM 模型 | 一个大型 Linux VM 托管所有容器 | 每个容器一个轻量 VM |
| 隔离性 | 进程级隔离（Linux namespace） | VM 级隔离（硬件虚拟化） |
| 资源开销 | 固定分配大量内存给 VM | 每个容器按需分配，更灵活 |
| 文件共享 | 需要预先挂载整个目录到 VM | 按需挂载 |
| 生态 | 成熟，支持 Compose/K8s | 早期阶段，功能还在完善 |

---

## 使用要求

- **硬件**：Apple Silicon Mac（M1/M2/M3/M4）
- **系统**：macOS 26 及以上（不支持更低版本）
- **构建**：Xcode 26+、Swift 工具链

---

## 安装与卸载

### 首次安装

```bash
# 从 Release 页面下载安装包后
sudo installer -pkg container-*.pkg -target /

# 启动系统服务
container system start
```

### 升级

```bash
container system stop
/usr/local/bin/update-container.sh
container system start
```

### 降级

```bash
container system stop
/usr/local/bin/uninstall-container.sh -k   # -k 保留用户数据
/usr/local/bin/update-container.sh -v 0.3.0
container system start
```

### 卸载

```bash
# 完全卸载（删除工具 + 用户数据）
/usr/local/bin/uninstall-container.sh -d

# 保留用户数据卸载
/usr/local/bin/uninstall-container.sh -k
```

---

## 快速上手

```bash
# 启动服务
container system start

# 运行容器（端口映射）
container run -p 8080:80 nginx

# 构建镜像
container build -t my-image .

# 推送镜像
container push my-image

# 管理持久化 VM（新特性）
container machine create my-vm --image ubuntu:22.04
container machine run my-vm
```

---

## 当前限制

1. **仅支持 macOS 26+**（Apple Silicon），不维护旧版本
2. **内存 ballooning 不全**：容器内释放的内存不会归还给 macOS 宿主，需要偶尔重启容器
3. **macOS 15 上的限制**（如果运行在 15 上）：
   - 容器间网络隔离，无法互相通信
   - 不支持多网络
   - IP 地址可能冲突导致网络失败

---

## 项目状态

- **当前版本**：0.x（活跃开发阶段）
- **稳定性**：仅保证 patch 版本内兼容，小版本可能有 Breaking Change
- **1.0.0** 发布后才会保证版本兼容性
- **许可证**：Apache 2.0
- **贡献指南**：https://github.com/apple/containerization/blob/main/CONTRIBUTING.md

---

## 参考资源

| 资源 | 链接 |
|------|------|
| 入门教程 | https://github.com/apple/container/blob/main/docs/tutorials/start-here.md |
| 功能使用指南 | https://github.com/apple/container/blob/main/docs/how-to.md |
| 技术架构概览 | https://github.com/apple/container/blob/main/docs/technical-overview.md |
| 完整命令参考 | https://github.com/apple/container/blob/main/docs/command-reference.md |
| API 文档 | https://apple.github.io/container/documentation/ |
| containerization 仓库 | https://github.com/apple/containerization |
| GitHub Release | https://github.com/apple/container/releases |
