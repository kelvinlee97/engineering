# Ubuntu APT 运维常用命令

English version: [README.md](README.md)

面向需要在 Ubuntu 主机上安装、更新、检查和排障软件包的运维人员。原则是：先刷新索引并查看计划，再执行会改变系统的操作。

本文以 Ubuntu 24.04 LTS 的路径和行为为主要示例；其他版本先确认本机的软件源配置。`apt` 面向交互式操作，脚本应优先使用 `apt-get`，因为 `apt` 的交互输出和默认行为可能随版本调整。

## 目录

- [安全更新流程](#安全更新流程)
- [升级后的验证](#升级后的验证)
- [查询软件包](#查询软件包)
- [安装、更新和删除](#安装更新和删除)
- [版本锁定和回滚](#版本锁定和回滚)
- [依赖和缓存维护](#依赖和缓存维护)
- [自动更新与锁冲突](#自动更新与锁冲突)
- [dpkg 低层检查](#dpkg-低层检查)
- [软件源和日志](#软件源和日志)
- [常见排障路径](#常见排障路径)
- [高风险操作边界](#高风险操作边界)
- [每日最小命令集](#每日最小命令集)

## 安全更新流程

~~~bash
# 1. 更新本机的软件包索引；不会安装更新
sudo apt update

# 2. 查看有哪些包可更新
apt list --upgradable

# 3. 先模拟，确认变更范围
sudo apt-get -s upgrade

# 4. 执行常规升级
sudo apt upgrade
~~~

apt upgrade 通常不会为了完成升级而删除已安装的软件包。需要允许新增或删除依赖时才考虑 full-upgrade，并先阅读 APT 给出的变更计划：

~~~bash
sudo apt-get -s full-upgrade
sudo apt full-upgrade
~~~

服务器发布窗口内，建议记录 apt 输出，并在升级后检查服务状态、应用健康检查和待重启提示。

## 升级后的验证

升级完成后，确认没有未完成的包配置、失败的 systemd 单元或待重启状态：

~~~bash
apt list --upgradable
dpkg --audit
systemctl --failed --no-pager

if test -e /run/reboot-required; then
  cat /run/reboot-required
  cat /run/reboot-required.pkgs 2>/dev/null || true
fi
~~~

`systemctl --failed` 只适用于使用 systemd 的主机；此外仍需按变更清单检查关键服务和应用健康检查。

## 查询软件包

| 目的 | 命令 |
| --- | --- |
| 搜索包名或描述 | apt search <keyword> |
| 查看包版本、来源和描述 | apt show <package> |
| 查看已安装版本和候选版本 | apt policy <package> |
| 列出已安装的软件包 | apt list --installed |
| 查看可更新的软件包 | apt list --upgradable |
| 判断是否已安装 | dpkg -s <package> |
| 检查未完成或损坏的包状态 | dpkg --audit |

示例：

~~~bash
apt policy nginx
apt show nginx
dpkg -s nginx
~~~

## 安装、更新和删除

~~~bash
# 安装一个或多个包
sudo apt install <package> [<package>...]

# 重新安装
sudo apt install --reinstall <package>

# 只删除程序，通常保留系统级配置文件
sudo apt remove <package>

# 删除程序及其由包管理器管理的配置文件
sudo apt purge <package>

# 安装本地 .deb，并自动解析仓库中的依赖
sudo apt install ./package.deb
~~~

remove 和 purge 不会自动删除用户目录中的配置或数据；应用是否清理 ~/.config、~/.local/share 等目录，要按应用文档单独确认。

### 暂时锁定版本

~~~bash
apt-mark showhold
sudo apt-mark hold <package>
sudo apt-mark unhold <package>
~~~

锁定前要记录原因和解除条件，避免长期漏掉安全更新。

## 依赖和缓存维护

~~~bash
# 修复未完成的配置步骤
sudo dpkg --configure -a

# 修复缺失或损坏的依赖
sudo apt --fix-broken install

# 检查依赖问题；不安装或删除包，但可能更新本地缓存
apt-get check

# 删除不再需要的自动安装依赖；执行前检查清单
sudo apt autoremove

# 同时清理被移除包留下的配置文件；谨慎使用
sudo apt autoremove --purge

# 清理下载的软件包缓存
sudo apt clean

# 只清理已不能下载的旧缓存
sudo apt autoclean
~~~

排障时先保存错误输出；不要把删除 APT 或 dpkg 锁文件作为常规修复手段。

## 版本锁定和回滚

先确认仓库中是否仍有目标版本，再模拟安装；不要假设任意旧版本都可以安全降级：

~~~bash
apt-cache policy <package>
sudo apt-get -s install <package>=<version>
sudo apt install <package>=<version>
~~~

如果目标版本已从镜像移除，使用经过验证的仓库快照或备份恢复，而不是随意添加旧软件源。Ubuntu 24.04 LTS 及以后版本可参考 [Ubuntu Snapshot Service](https://ubuntu.com/server/docs/how-to/software/snapshot-service/)。

大版本升级不是普通的 APT 包升级；服务器应使用 `do-release-upgrade`，并遵循官方的[发行版升级检查清单](https://ubuntu.com/server/docs/how-to/software/upgrade-your-release/)。

## 自动更新与锁冲突

Ubuntu Server 通常会通过 `unattended-upgrades` 和 `apt-daily` 定时任务自动处理更新。执行人工操作前先确认是否有任务正在运行：

~~~bash
systemctl list-timers apt-daily.timer apt-daily-upgrade.timer --no-pager
systemctl status apt-daily.service apt-daily-upgrade.service unattended-upgrades.service --no-pager
ps -ef | grep -E '[a]pt|[d]pkg'
sudo fuser -v /var/lib/dpkg/lock-frontend /var/lib/dpkg/lock /var/lib/apt/lists/lock /var/cache/apt/archives/lock
~~~

如果有 APT 或 dpkg 进程，等待它完成后再重试；不要直接杀进程或删除锁文件。若确认操作被中断，再按顺序执行 `sudo dpkg --configure -a` 和 `sudo apt --fix-broken install`。

自动更新的配置和日志常见于 `/etc/apt/apt.conf.d/20auto-upgrades`、`/etc/apt/apt.conf.d/50unattended-upgrades` 和 `/var/log/unattended-upgrades/`。不要为了方便人工操作而长期关闭安全更新。

## dpkg 低层检查

~~~bash
# 列出包数据库中的状态
dpkg -l <package>

# 查看包的详细状态
dpkg -s <package>

# 查看某个包安装了哪些文件
dpkg -L <package>

# 反查某个文件属于哪个包
dpkg -S /path/to/file

# 查看本地 deb 的元数据，不安装
dpkg-deb -I ./package.deb
~~~

APT 负责依赖解析和仓库交互；dpkg 直接操作单个 Debian 包，不能自动下载并安装依赖。

## 软件源和日志

Ubuntu 24.04 LTS 默认使用 deb822 格式的源配置，常见位置是 `/etc/apt/sources.list.d/ubuntu.sources`；其他版本可能使用 `/etc/apt/sources.list`。先查看，不要盲目添加第三方源：

~~~bash
apt policy
find /etc/apt -maxdepth 2 -type f \( -name 'sources.list' -o -name '*.list' -o -name '*.sources' \) -print
grep -R --line-number -E '^(Types|URIs|Suites|Components|Signed-By):|^deb ' /etc/apt/sources.list /etc/apt/sources.list.d 2>/dev/null
~~~

第三方源必须确认发行方、签名和维护责任。应将未由软件包管理的 keyring 放在 `/etc/apt/keyrings/`，并在源配置中用 `Signed-By` 限定它的作用域；不要使用已弃用的 `apt-key`，也不要使用 `--allow-unauthenticated` 绕过签名验证。参考：[apt-key 手册](https://manpages.ubuntu.com/manpages/noble/man8/apt-key.8.html)。

APT 和 dpkg 的操作记录通常在：

~~~bash
less /var/log/apt/history.log
less /var/log/apt/term.log
less /var/log/dpkg.log
less /var/log/unattended-upgrades/unattended-upgrades.log
~~~

## 常见排障路径

### 更新被延迟或保留

`apt upgrade` 显示 kept back 或 deferred 不一定是故障，可能是 phased updates 或依赖变更。先查看候选版本和来源，不要为了强行升级而绕过保护：

~~~bash
apt list --upgradable
apt policy <package>
sudo apt-get -s upgrade
~~~

Ubuntu 会分阶段推送部分更新；等待下一阶段或按变更窗口处理，只有在明确理解影响时才选择其他升级策略。参考：[phased updates](https://ubuntu.com/server/docs/about-apt-upgrade-and-phased-updates/)。

### 典型错误分类

| 现象 | 先检查 | 边界 |
| --- | --- | --- |
| Could not get lock / Lock held | 自动更新定时器、APT/dpkg 进程和锁的占用者 | 等待当前操作结束；不要删除锁文件 |
| NO_PUBKEY / repository is not signed | 软件源 URL、`Signed-By` 和 keyring 来源 | 不要使用 `--allow-unauthenticated`；先验证发行方 |
| 404 / Release file expired | 发行版代号、源是否支持该版本、系统是否 EOL | 不要盲目把源代号替换成另一个版本 |
| dpkg was interrupted | `dpkg --audit` 和待配置包 | 先 `sudo dpkg --configure -a`，再修复依赖 |

对网络问题先确认 DNS 和出口连通性；修复软件源后重新运行 `sudo apt update`，不要用删除索引或锁文件来掩盖错误。

## 高风险操作边界

- apt update 只刷新索引；它不等于升级系统。
- full-upgrade 可能删除软件包；先运行 sudo apt-get -s full-upgrade。
- 模拟命令也要使用 sudo，以读取与真实执行一致的配置。
- purge 会删除包管理器管理的配置，执行前确认不需要回滚。
- autoremove 会删除被判断为不再需要的自动依赖；先运行 sudo apt-get -s autoremove --purge 并审阅列表。
- 不要为了“解锁”而直接删除 /var/lib/dpkg/lock* 或 /var/lib/apt/lists/lock。
- 不要使用 apt-key 或 --allow-unauthenticated 绕过软件源签名验证。
- 第三方软件源会扩大供应链和升级风险；确认来源、签名和维护责任。
- `full-upgrade` 不等于 Ubuntu 大版本升级；大版本升级使用 `do-release-upgrade` 并执行备份和回滚准备。

## 每日最小命令集

~~~bash
sudo apt update
apt list --upgradable
sudo apt-get -s upgrade
sudo apt upgrade
apt list --upgradable
dpkg --audit
~~~

官方参考：[Ubuntu 软件包管理](https://ubuntu.com/server/docs/package-management/)、[apt-get 手册](https://manpages.ubuntu.com/manpages/noble/man8/apt-get.8.html)、[自动更新](https://ubuntu.com/server/docs/how-to/software/automatic-updates/)、[发行版升级](https://ubuntu.com/server/docs/how-to/software/upgrade-your-release/)。
