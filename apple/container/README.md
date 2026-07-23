# Understanding Apple Container

Chinese version: [README_ZH.md](README_ZH.md)

## Project Overview

**apple/container** is Apple's official **native container tool for macOS**. It is written in Swift and optimized for Apple silicon.

**Core idea:** Instead of running one shared Linux VM to host all containers, as Docker Desktop does, **each container runs inside its own lightweight virtual machine**.

---

## Architecture

```
┌─────────────────────────────────────────────┐
│          container CLI (Swift)              │
│                   │                         │
│         container-apiserver (launchd)       │
│              ┌────┴────┐                    │
│   container-core-images  container-network  │
│   (image XPC helper)     (network XPC helper)│
└─────────────────────────────────────────────┘
         │                    │
    ┌────▼────┐        ┌────▼────┐
    │Container│        │Container│
    │ VM 1    │        │ VM 2    │
    │(light VM)│       │(light VM)│
    └─────────┘        └─────────┘
```

### Core Components

| Component | Responsibility |
|-----------|----------------|
| `container` CLI | Command-line interface for managing containers, images, and networks |
| `container-apiserver` | A launchd-managed service process that provides the client API |
| `container-core-images` | XPC helper that manages images and local content storage |
| `container-network-vmnet` | XPC helper that manages virtual networking |
| `container-runtime-linux` | One instance per container, responsible for that container's runtime API |

### Key Technologies

- **Virtualization.framework** — Manages Linux VMs and attached devices
- **vmnet.framework** — Manages virtual networking
- **XPC** — Provides interprocess communication
- **launchd** — Manages services
- **Keychain** — Stores registry credentials
- **Unified Logging** — Provides application logging

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Strong isolation** | Each container runs in a separate VM, providing isolation equivalent to a full virtual machine |
| **Privacy** | Only the required data is mounted into each VM instead of sharing everything |
| **Fast startup** | A customized, optimized Linux kernel and minimal root filesystem enable subsecond startup |
| **OCI compatibility** | Consumes and produces standard OCI images that interoperate with OCI registries and compatible tools |
| **Rosetta 2** | Supports running `linux/amd64` containers on Apple silicon |

---

## Project Structure

### apple/container

The command-line tool used directly by users.

**Installation:**

```bash
# Download the .pkg from the Releases page, then install it
sudo installer -pkg container-*.pkg -target /

# Start the service
container system start
```

**Main commands:**

```bash
container run              # Run a container
container build            # Build an image
container image pull       # Pull an image
container image push       # Push an image
container machine          # Manage persistent Linux VMs
container network          # Manage virtual networks
container system           # Start or stop system services
```

### apple/containerization

The underlying Swift package that provides the core APIs:

1. **OCI image management** — Creates, reads, and modifies OCI-compliant images
2. **Remote registry interaction** — Supports Docker Hub and private registries
3. **Filesystem creation** — Creates and populates ext4 filesystems
4. **Lightweight VM management** — Creates lightweight VMs and manages container runtime environments
5. **Container process interaction** — Starts and interacts with containerized processes
6. **vminitd** — A built-in lightweight init system that runs as the VM's initial process and exposes a gRPC API over vsock

---

## Key Differences from Docker Desktop

| Dimension | Docker Desktop | apple/container |
|-----------|----------------|-----------------|
| VM model | One large Linux VM hosts all containers | Each container has its own lightweight VM |
| Isolation | Process-level isolation through Linux namespaces | VM-level isolation through hardware virtualization |
| Resource model | A configurable memory limit applies to the shared Linux VM | Each lightweight VM uses memory according to its container workload |
| File sharing | Selected host directories are shared with the Linux VM | Only the host data required by each container is mounted into its VM |
| Ecosystem | Mature, with Compose and Kubernetes support | Early-stage, with features still being developed |

---

## Requirements

- **Hardware:** An Apple silicon Mac
- **Official support:** macOS 26; macOS 15 can run the tool with documented limitations, but issues specific to older macOS versions are not maintained
- **Building from source:** macOS 15 minimum, macOS 26 recommended, and Xcode 26 as the active developer directory

---

## Installation and Removal

### First Installation

```bash
# Download the installer package from the Releases page
sudo installer -pkg container-*.pkg -target /

# Start the system service
container system start
```

### Upgrade

```bash
container system stop
/usr/local/bin/update-container.sh
container system start
```

### Downgrade

```bash
container system stop
/usr/local/bin/uninstall-container.sh -k   # -k preserves user data
/usr/local/bin/update-container.sh -v 0.3.0
container system start
```

### Uninstall

```bash
# Completely uninstall the tools and user data
/usr/local/bin/uninstall-container.sh -d

# Uninstall while preserving user data
/usr/local/bin/uninstall-container.sh -k
```

---

## Quick Start

```bash
# Start the service
container system start

# Run a container with port forwarding
container run -p 8080:80 nginx

# Build an image
container build -t my-image .

# Push an image
container image push my-image

# Manage a persistent VM
container machine create ubuntu:22.04 --name my-vm
container machine run --name my-vm
```

---

## Current Limitations

1. **macOS 26 is the supported release.** The tool can run on macOS 15 with limitations, but issues that cannot be reproduced on macOS 26 are generally not addressed
2. **Incomplete memory ballooning:** Memory released inside a container is not returned to the macOS host, so containers may need to be restarted occasionally
3. **Limitations on macOS 15** if the tool is run there:
   - Containers are isolated from one another and cannot communicate
   - Multiple networks are not supported
   - IP address conflicts may cause network failures

---

## Project Status

- **Current version:** 0.x, under active development
- **Stability:** Compatibility is guaranteed only within patch releases; minor releases may contain breaking changes
- Version compatibility will be guaranteed after the 1.0.0 release
- **License:** Apache 2.0
- **Contribution guide:** https://github.com/apple/containerization/blob/main/CONTRIBUTING.md

---

## References

| Resource | Link |
|----------|------|
| Getting started tutorial | https://github.com/apple/container/blob/main/docs/tutorials/start-here.md |
| How-to guides | https://github.com/apple/container/blob/main/docs/how-to.md |
| Technical overview | https://github.com/apple/container/blob/main/docs/technical-overview.md |
| Complete command reference | https://github.com/apple/container/blob/main/docs/command-reference.md |
| API documentation | https://apple.github.io/container/documentation/ |
| containerization repository | https://github.com/apple/containerization |
| GitHub Releases | https://github.com/apple/container/releases |
