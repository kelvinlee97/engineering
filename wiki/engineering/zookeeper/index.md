# Playbook

* [ZooKeeper production deployment](production-deployment.md) - Build and operate a three-member ZooKeeper 3.9.5 ensemble with mutual TLS, systemd, JMX metrics, and one-member-at-a-time changes.
* [ZooKeeper quorum-loss restore](quorum-loss-restore.md) - Restore a three-member ZooKeeper ensemble that lost quorum by loading the same approved snapshot into every member, one at a time, through a temporary loopback-only admin endpoint.
* [ZooKeeper single-member recovery](single-member-recovery.md) - Rebuild one ZooKeeper member whose transaction log a full disk truncated, by moving its data aside and letting it resync from a healthy quorum.

# Service

* [ZooKeeper](zookeeper.md) - A distributed coordination service that keeps a small, consistently replicated tree of data for leader election, membership, and configuration notification.
