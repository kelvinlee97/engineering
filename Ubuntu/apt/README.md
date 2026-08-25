# Common Ubuntu APT Operations

Chinese version: [README_ZH.md](README_ZH.md)

This guide is for operators who need to install, update, inspect, and troubleshoot packages on Ubuntu hosts. The rule is simple: refresh the index and inspect the plan before making system changes.

This guide uses Ubuntu 24.04 LTS paths and behavior as its main example; confirm the local repository layout on other releases. `apt` is intended for interactive use; prefer `apt-get` in scripts because `apt`'s interactive output and defaults may change between versions.

## Contents

- [Safe update flow](#safe-update-flow)
- [Post-upgrade verification](#post-upgrade-verification)
- [Inspect packages](#inspect-packages)
- [Install, update, and remove](#install-update-and-remove)
- [Version holds and rollback](#version-holds-and-rollback)
- [Dependency and cache maintenance](#dependency-and-cache-maintenance)
- [Automatic updates and lock conflicts](#automatic-updates-and-lock-conflicts)
- [Low-level dpkg inspection](#low-level-dpkg-inspection)
- [Repositories and logs](#repositories-and-logs)
- [Common troubleshooting paths](#common-troubleshooting-paths)
- [High-risk operation boundaries](#high-risk-operation-boundaries)
- [Minimum daily command set](#minimum-daily-command-set)

## Safe update flow

~~~bash
# 1. Refresh the local package index; this does not install updates
sudo apt update

# 2. See which packages can be upgraded
apt list --upgradable

# 3. Simulate the change first
sudo apt-get -s upgrade

# 4. Apply ordinary upgrades
sudo apt upgrade
~~~

apt upgrade normally does not remove installed packages to complete an upgrade. Consider full-upgrade only when new or removed dependencies are acceptable, and read APT's change plan first:

~~~bash
sudo apt-get -s full-upgrade
sudo apt full-upgrade
~~~

During a server change window, retain the APT output and then check service status, application health checks, and reboot-required notices.

## Post-upgrade verification

After the upgrade, confirm that no package configuration, systemd unit, or reboot state is left incomplete:

~~~bash
apt list --upgradable
dpkg --audit
systemctl --failed --no-pager

if test -e /run/reboot-required; then
  cat /run/reboot-required
  cat /run/reboot-required.pkgs 2>/dev/null || true
fi
~~~

`systemctl --failed` applies only to systemd hosts. Also check critical services and application health checks from the change plan.

## Inspect packages

| Purpose | Command |
| --- | --- |
| Search package names or descriptions | apt search <keyword> |
| Show version, origin, and description | apt show <package> |
| Show installed and candidate versions | apt policy <package> |
| List installed packages | apt list --installed |
| List upgradeable packages | apt list --upgradable |
| Check whether a package is installed | dpkg -s <package> |
| Check for incomplete or broken package states | dpkg --audit |

Example:

~~~bash
apt policy nginx
apt show nginx
dpkg -s nginx
~~~

## Install, update, and remove

~~~bash
# Install one or more packages
sudo apt install <package> [<package>...]

# Reinstall a package
sudo apt install --reinstall <package>

# Remove the program; package-managed configuration is usually retained
sudo apt remove <package>

# Remove the program and its package-managed configuration files
sudo apt purge <package>

# Install a local .deb and resolve its repository dependencies
sudo apt install ./package.deb
~~~

remove and purge do not automatically delete user-directory data. Whether directories such as ~/.config and ~/.local/share should be removed depends on the application.

### Temporarily hold a package version

~~~bash
apt-mark showhold
sudo apt-mark hold <package>
sudo apt-mark unhold <package>
~~~

Record why a package is held and when the hold can be removed so security updates are not missed indefinitely.

## Dependency and cache maintenance

~~~bash
# Finish pending package configuration steps
sudo dpkg --configure -a

# Repair missing or broken dependencies
sudo apt --fix-broken install

# Check for dependency problems; installs or removes no packages, but may update the local cache
apt-get check

# Remove unused automatically installed dependencies; review the list first
sudo apt autoremove

# Also purge package-managed configuration for removed dependencies; use carefully
sudo apt autoremove --purge

# Remove downloaded package cache
sudo apt clean

# Remove only obsolete package-cache files
sudo apt autoclean
~~~

During troubleshooting, save the error output first. Do not treat deleting APT or dpkg lock files as a routine fix.

## Version holds and rollback

Confirm that the target version is still available from a configured repository, then simulate the install. Do not assume that any older version can be safely downgraded:

~~~bash
apt-cache policy <package>
sudo apt-get -s install <package>=<version>
sudo apt install <package>=<version>
~~~

If the target version has left the mirror, use a verified repository snapshot or restore from backup instead of adding an arbitrary old repository. For Ubuntu 24.04 LTS and later, see the [Ubuntu Snapshot Service](https://ubuntu.com/server/docs/how-to/software/snapshot-service/).

A major release upgrade is not an ordinary APT package upgrade. On servers, use `do-release-upgrade` and follow the official [release-upgrade checklist](https://ubuntu.com/server/docs/how-to/software/upgrade-your-release/).

## Automatic updates and lock conflicts

Ubuntu Server commonly uses `unattended-upgrades` and `apt-daily` timers for automatic updates. Before a manual operation, check whether one is running:

~~~bash
systemctl list-timers apt-daily.timer apt-daily-upgrade.timer --no-pager
systemctl status apt-daily.service apt-daily-upgrade.service unattended-upgrades.service --no-pager
ps -ef | grep -E '[a]pt|[d]pkg'
sudo fuser -v /var/lib/dpkg/lock-frontend /var/lib/dpkg/lock /var/lib/apt/lists/lock /var/cache/apt/archives/lock
~~~

If an APT or dpkg process is active, wait for it to finish and retry. Do not kill the process or delete lock files directly. If an operation was interrupted, run `sudo dpkg --configure -a` followed by `sudo apt --fix-broken install`.

Automatic-update configuration and logs are commonly found in `/etc/apt/apt.conf.d/20auto-upgrades`, `/etc/apt/apt.conf.d/50unattended-upgrades`, and `/var/log/unattended-upgrades/`. Do not permanently disable security updates just to make manual operations easier.

## Low-level dpkg inspection

~~~bash
# Show a package's database status
dpkg -l <package>

# Show detailed package status
dpkg -s <package>

# List files installed by a package
dpkg -L <package>

# Find which package owns a file
dpkg -S /path/to/file

# Inspect local deb metadata without installing it
dpkg-deb -I ./package.deb
~~~

APT handles dependency resolution and repository interaction. dpkg operates on individual Debian packages and does not automatically download and install dependencies.

## Repositories and logs

Ubuntu 24.04 LTS uses deb822 repository configuration by default; the common file is `/etc/apt/sources.list.d/ubuntu.sources`. Other releases may use `/etc/apt/sources.list`. Inspect before changing and do not add third-party repositories blindly:

~~~bash
apt policy
find /etc/apt -maxdepth 2 -type f \( -name 'sources.list' -o -name '*.list' -o -name '*.sources' \) -print
grep -R --line-number -E '^(Types|URIs|Suites|Components|Signed-By):|^deb ' /etc/apt/sources.list /etc/apt/sources.list.d 2>/dev/null
~~~

For third-party repositories, verify the owner, signing, and maintenance responsibility. Store keyrings not managed by packages in `/etc/apt/keyrings/` and scope them with `Signed-By` in the source entry. Do not use the deprecated `apt-key` command or bypass signature verification with `--allow-unauthenticated`. See the [apt-key manual](https://manpages.ubuntu.com/manpages/noble/man8/apt-key.8.html).

APT and dpkg operations are commonly recorded in:

~~~bash
less /var/log/apt/history.log
less /var/log/apt/term.log
less /var/log/dpkg.log
less /var/log/unattended-upgrades/unattended-upgrades.log
~~~

## Common troubleshooting paths

### Upgrades kept back or deferred

`apt upgrade` showing kept-back or deferred packages is not necessarily a failure; it may reflect phased updates or dependency changes. Inspect the candidate version and origin before forcing anything:

~~~bash
apt list --upgradable
apt policy <package>
sudo apt-get -s upgrade
~~~

Ubuntu rolls out some updates in phases. Wait for the next phase or handle the package during an approved change window; only choose another upgrade strategy when the impact is understood. See the [phased updates documentation](https://ubuntu.com/server/docs/about-apt-upgrade-and-phased-updates/).

### Common error categories

| Symptom | Check first | Boundary |
| --- | --- | --- |
| Could not get lock / Lock held | Automatic-update timers, APT/dpkg processes, and lock owners | Wait for the current operation; do not delete lock files |
| NO_PUBKEY / repository is not signed | Repository URL, `Signed-By`, and keyring origin | Do not use `--allow-unauthenticated`; verify the publisher first |
| 404 / Release file expired | Release codename, repository support, and whether the system is EOL | Do not blindly replace the repository codename |
| dpkg was interrupted | `dpkg --audit` and packages awaiting configuration | Run `sudo dpkg --configure -a`, then repair dependencies |

For network failures, verify DNS and outbound connectivity first. After correcting the repository, run `sudo apt update` again; do not hide the error by deleting indexes or lock files.

## High-risk operation boundaries

- apt update refreshes indexes only; it does not upgrade the system.
- full-upgrade can remove packages; run sudo apt-get -s full-upgrade first.
- Run simulations with sudo so they read the same configuration as the real operation.
- purge removes package-managed configuration; confirm rollback requirements first.
- autoremove removes dependencies judged no longer needed; run sudo apt-get -s autoremove --purge and review the list first.
- Do not delete /var/lib/dpkg/lock* or /var/lib/apt/lists/lock just to “unlock” APT.
- Do not use apt-key or --allow-unauthenticated to bypass repository signature verification.
- Third-party repositories increase supply-chain and upgrade risk; verify their origin, signing, and maintenance responsibility.
- full-upgrade is not a major Ubuntu release upgrade; use do-release-upgrade with backup and rollback preparation.

## Minimum daily command set

~~~bash
sudo apt update
apt list --upgradable
sudo apt-get -s upgrade
sudo apt upgrade
apt list --upgradable
dpkg --audit
~~~

Official references: [Ubuntu package management](https://ubuntu.com/server/docs/package-management/), the [apt-get manual](https://manpages.ubuntu.com/manpages/noble/man8/apt-get.8.html), [automatic updates](https://ubuntu.com/server/docs/how-to/software/automatic-updates/), and [release upgrades](https://ubuntu.com/server/docs/how-to/software/upgrade-your-release/).
