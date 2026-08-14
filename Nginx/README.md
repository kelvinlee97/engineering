# Nginx and OpenResty Operations

Chinese version: [README_ZH.md](README_ZH.md)

This module contains beginner-friendly production deployment and operations guides for Nginx and OpenResty on Ubuntu 24.04 LTS. They are separate server choices: OpenResty is an Nginx-based distribution with LuaJIT and Lua modules, not a plugin to run alongside a system Nginx.

Do not run both guides on one host at the same time. Both examples bind TCP ports `80` and `443`.

For a Node.js BFF upstream managed by PM2, see [Node.js / Express BFF Operations](../Nodejs/README.md).

## Guides

| Guide | Description |
| --- | --- |
| [Nginx production deployment](guides/nginx-production-deployment/README.md) | Static-site and reverse-proxy deployment with systemd and HTTPS. |
| [OpenResty production deployment](guides/openresty-production-deployment/README.md) | Lua health endpoint and reverse-proxy deployment with systemd and HTTPS. |
