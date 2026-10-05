# Virgo-Core Wiki

Source-based guide to the repository, not a deployment runbook.

**Source revision:** `166734f0c4ad5169d7140b5177e315118edfa578`\
**Updated:** 2026-09-11\
**Content pages:** 7

## Start here

Start with [Task routing](task-routing.md) for a question or [Architecture](architecture.md) for orientation.

## Pages

- [[access-and-secrets]] — [SSH, automation accounts and secrets](./access-and-secrets.md)
- [[ansible-roles]] — [Ansible roles and workflows](./ansible-roles.md)
- [[architecture]] — [Architecture and ownership](./architecture.md)
- [[known-gaps]] — [Known gaps and source inconsistencies](./known-gaps.md)
- [[provisioning]] — [VM, template and LXC provisioning](./provisioning.md)
- [[task-routing]] — [Start from a task](./task-routing.md)
- [[validation-and-safety]] — [Validation, tooling and execution boundaries](./validation-and-safety.md)

## Evidence and maintenance

- [Schema](SCHEMA.md): source and maintenance rules.
- [Log](log.md): generation and validation record.
- [Source manifest](raw/source-manifest.json): pinned content hashes.
- [Validator](validate.py): local structural and source-drift checks.

No infrastructure was contacted for generation. No claim of CI success, deployment health or current credentials is made. Read known-gaps before copying procedures.
