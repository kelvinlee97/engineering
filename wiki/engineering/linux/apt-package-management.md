---
type: Playbook
title: APT package management
description: Install, upgrade, hold, roll back, and troubleshoot Ubuntu packages safely by refreshing, simulating, and inspecting before applying.
tags: [ubuntu, apt, linux, runbook]
sources:
  - id: ubuntu-apt-guide
    resource: https://github.com/kelvinlee97/engineering/blob/main/Ubuntu/apt/README.md
    title: Common Ubuntu APT Operations
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T05:15:00Z }
status: draft
---
Every APT change follows one shape: refresh the index, simulate the change, inspect the plan, then apply it. Held versions, phased rollouts, unattended-upgrade timers, and dpkg locks can silently change what a plain install or upgrade does, so the simulation is what protects you. Use `apt` interactively and `apt-get` in scripts, because `apt`'s output and defaults may change between versions.[^ubuntu-apt-guide]

## Safe upgrade

1. `sudo apt update` refreshes the index only; it upgrades nothing.
2. `apt list --upgradable`, then simulate with `sudo apt-get -s upgrade` (run simulations with `sudo` so they read the same configuration).
3. `sudo apt upgrade`. Use `full-upgrade` only when adding or removing dependencies is acceptable, after simulating it: it can remove packages.
4. Verify: nothing left upgradable, `dpkg --audit` clean, `systemctl --failed` empty, and check `/run/reboot-required`.

A major release upgrade is not a package upgrade: use `do-release-upgrade` with backup and rollback preparation.[^ubuntu-apt-guide]

## Holds and rollback

`apt-mark hold` pins a package; record why and when to remove the hold so security updates are not missed indefinitely. To downgrade, confirm the version is still in a configured repository and simulate `apt-get -s install <package>=<version>`; if it has left the mirror, use a verified repository snapshot (the Ubuntu Snapshot Service, 24.04 and later) or a backup, not an arbitrary old repository.[^ubuntu-apt-guide]

## Troubleshooting

| Symptom | Check first | Boundary |
| --- | --- | --- |
| Could not get lock | `apt-daily` timers, `unattended-upgrades`, APT/dpkg processes, `fuser` on the lock files | Wait; never delete lock files or kill the process |
| `NO_PUBKEY` / unsigned repository | Repository URL, `Signed-By`, keyring origin | No `--allow-unauthenticated`, no `apt-key` |
| `404` / Release file expired | Codename, support status, EOL | Do not blindly change the codename |
| dpkg was interrupted | `dpkg --audit` | `sudo dpkg --configure -a`, then `sudo apt --fix-broken install` |
| Packages kept back or deferred | `apt policy`, simulation | Often phased updates, not a failure; do not force |

As listed in the guide. Third-party repositories need a verified owner and signing key stored in `/etc/apt/keyrings/` and referenced with `Signed-By`; Ubuntu 24.04 uses deb822 sources in `/etc/apt/sources.list.d/ubuntu.sources`.[^ubuntu-apt-guide]

## Related

- [Safe change procedure](../operations/incident-operations.md#safe-change-procedure)

[^ubuntu-apt-guide]: [Common Ubuntu APT Operations](../../sources/ubuntu-apt-guide.md), [original](https://github.com/kelvinlee97/engineering/blob/main/Ubuntu/apt/README.md)
