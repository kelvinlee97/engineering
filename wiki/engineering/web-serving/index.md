# Concept

* [Backend for frontend](backend-for-frontend.md) - A backend that serves one browser-facing application: it enforces session and authorization rules, adapts requests, and calls downstream services.
* [Reverse proxy gateway](reverse-proxy-gateway.md) - A server such as Nginx or OpenResty that terminates HTTPS at the edge and forwards requests to an application listening only on a private address.

# Playbook

* [Express BFF deployment](express-bff-deployment.md) - Deploy an Express backend-for-frontend under PM2 cluster mode as an unprivileged user, with immutable releases and symlink rollback.
* [Express BFF incidents](express-bff-incidents.md) - Ten common failure modes of an Express BFF under PM2 cluster mode, each with first checks, recovery, and verification.
* [Nginx production deployment](nginx-production-deployment.md) - Deploy Nginx on one Ubuntu 24.04 VM to serve static files and reverse-proxy a loopback application, with Certbot HTTPS and layer-by-layer checks.
* [OpenResty production deployment](openresty-production-deployment.md) - Deploy OpenResty on one Ubuntu 24.04 VM with a Lua health endpoint, a loopback reverse proxy, and Certbot HTTPS.
