# Amazon QLDB - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon Quantum Ledger Database (Amazon QLDB) was a fully managed ledger database with an append-only journal, cryptographic verification, and PartiQL queries. **Amazon QLDB reached end of support on July 31, 2025.** Existing customers were guided to migrate QLDB ledgers to Amazon Aurora PostgreSQL. Do not build new systems on QLDB.

## Key concepts (for migration context)

- **Ledger**: the QLDB database resource holding an immutable, append-only journal.
- **Journal**: a cryptographically chained log of all changes to the ledger.
- **Digest and verification**: hash-based integrity checks proving the journal was not modified.
- **PartiQL**: the SQL-compatible query language used to read and write documents.
- **Migration path**: Amazon Aurora PostgreSQL with an append-only/audit design is the documented replacement for ledger workloads.

## Common operations (for existing ledgers)

```bash
# List and describe existing ledgers
aws qldb list-ledgers
aws qldb describe-ledger --name my-ledger

# Export ledger contents to S3 before decommissioning
aws qldb export-journal-to-s3 --name my-ledger \
  --inclusive-start-time 2025-01-01T00:00:00Z \
  --exclusive-end-time 2026-08-19T00:00:00Z \
  --s3-export-configuration Bucket=export-bucket,Prefix=qldb/

# Delete an existing ledger
aws qldb delete-ledger --name my-ledger
```

## Best practices

- Do not start new projects on QLDB; it is end-of-life. Evaluate Amazon Aurora PostgreSQL or an alternative ledger/audit architecture.
- If you operate existing QLDB ledgers, plan and execute the migration to Aurora PostgreSQL before decommissioning.
- Export journal contents to S3 as a retention record before deletion.
- Keep an inventory of ledgers and IAM permissions so unused ledgers are removed cleanly.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Cannot create a new ledger | Expected: the service is end-of-life; new deployments are no longer supported. |
| Migration questions | Follow the official guide for migrating QLDB ledgers to Amazon Aurora PostgreSQL. |
| Decommissioning | Export journals to S3, then delete ledgers and remove associated IAM roles/policies. |

## Limits

The service is end-of-life (support ended July 31, 2025). Existing capacity limits no longer apply to new usage; plan decommissioning and migration.

## Official references

- [Amazon QLDB developer guide (end-of-support notice)](https://docs.aws.amazon.com/qldb/latest/developerguide/what-is.html)
- [Migrating Amazon QLDB ledgers to Amazon Aurora PostgreSQL](https://docs.aws.amazon.com/qldb/latest/developerguide/migrate-to-aurora-postgresql.html)
- [AWS CLI: qldb commands](https://docs.aws.amazon.com/cli/latest/reference/qldb/)
