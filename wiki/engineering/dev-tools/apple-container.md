---
type: Tool
title: Apple Container
description: Apple's native container tool for Apple silicon Macs, which runs each container in its own lightweight VM instead of one shared Linux VM.
tags: [containers, macos, dev-tools]
sources:
  - id: apple-container
    resource: https://github.com/kelvinlee97/engineering/blob/main/apple/container/README.md
    title: Understanding Apple Container
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T05:15:00Z }
status: draft
---
apple/container is Apple's native container tool for macOS, written in Swift for Apple silicon. Where Docker Desktop runs all containers in one shared Linux VM, it gives each container its own lightweight VM.[^apple-container]

## Architecture

The `container` CLI talks to `container-apiserver`, a launchd service, which uses XPC helpers for images (`container-core-images`) and networking (`container-network-vmnet`) and runs one `container-runtime-linux` per container. It builds on Virtualization.framework, vmnet.framework, XPC, launchd, Keychain for registry credentials, and Unified Logging.[^apple-container] The apple/containerization Swift package underneath handles OCI images, registries, ext4 filesystems, lightweight VMs, and `vminitd`, an init process exposing gRPC over vsock.[^apple-container]

## Compared with Docker Desktop

| | Docker Desktop | apple/container |
| --- | --- | --- |
| VM model | One Linux VM for all containers | One lightweight VM per container |
| Isolation | Linux namespaces | Hardware virtualization |
| Memory | Limit on the shared VM | Per-VM, by workload |
| File sharing | Selected host directories shared with the VM | Only what each container needs |
| Ecosystem | Mature, Compose and Kubernetes | Early stage |

As compared in the source.[^apple-container] It uses standard OCI images and runs `linux/amd64` containers through Rosetta 2.[^apple-container]

## Limits at the time of writing

- Needs an Apple silicon Mac; macOS 26 is supported, and macOS 15 works with limitations (containers cannot talk to each other, no multiple networks, possible IP conflicts).[^apple-container]
- Memory freed inside a container is not returned to macOS, so containers may need occasional restarts.[^apple-container]
- Version 0.x: compatibility is guaranteed only within patch releases until 1.0.0.[^apple-container]

## Related

- Source: [Understanding Apple Container](../../sources/apple-container.md)

[^apple-container]: Understanding Apple Container
