# Documentation Audit Report

Generated: 2026-05-05 | Commit: `1d24515`

## Executive Summary

| Metric | Count |
|---|---:|
| Documentation scopes audited | 6 |
| Documents scanned | 38 |
| False claim groups | 97 |
| Source docs edited | 0 |

This audit used parallel `documentation-audit` subagents with pass-1 claim extraction/verification and pass-2 pattern expansion. The first parallel run had two child transport failures; one had already written findings, and the missing scope was rerun successfully in a second parallel run.

## Highest-priority drift patterns

| Pattern | Affected areas | Why it matters |
|---|---|---|
| Broken/stale doc paths | `README.md`, `documentation/README.md`, Ansible/scripts/Terraform docs | Readers are routed to missing or archived docs. |
| Missing playbook/task references | Ansible role docs, getting-started docs, README | Operational commands fail as written. |
| Role variable schema drift | `system_user`, `proxmox_access`, `proxmox_ceph`, getting-started network config | Examples won't drive the current roles correctly. |
| CEPH capacity/replication mismatch | Core docs, getting-started docs, generated role docs | Docs claim ~12TB usable while code uses replication `size: 3` (~8TB from 24TB raw). |
| Planned vs implemented NetBox/PowerDNS | Core architecture docs | Target architecture is presented as current implementation. |
| Terraform local-module drift | Terraform examples and generated docs | Examples reference missing `../../../modules/vm` / `vm-cluster` trees. |
| Tool-version prose drift | README/getting-started/Ansible docs | Docs should not track managed tool versions; `.mise.toml` is canonical truth for pins. |

## Documentation versioning rule

Managed tool versions must not be duplicated in prose docs. Refer readers to `.mise.toml` for pinned tool versions, and only document compatibility constraints when they come from an authoritative config file such as `pyproject.toml`.

## Source artifact handling

The temporary subagent findings were folded into this report and the `tmp/` working artifacts were removed.

## Detailed Findings


---

#### Core Documentation Audit Findings

Generated: 2026-05-05 | Commit: `1d24515`

#### Docs scanned

12 current user-facing docs:

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/diagrams/infrastructure-overview.md`
- `docs/diagrams/switch-topology.md`
- `docs/decisions/README.md`
- `docs/decisions/0001-powerdns-over-unifi-dns.md`
- `docs/decisions/0002-quantum-as-infrastructure-cluster.md`
- `documentation/README.md`
- `documentation/core/goals.md`
- `documentation/core/infrastructure.md`
- `documentation/core/netbox-powerdns.md`
- `documentation/core/references.md`

#### False claims requiring fixes

| Doc line | Claim | Reality / evidence | Suggested fix |
|---|---|---|---|
| `README.md:38`, `docs/ARCHITECTURE.md:188`, `docs/ARCHITECTURE.md:494`, `docs/diagrams/infrastructure-overview.md:138` | Matrix CEPH is `24TB raw / 12TB usable`; Architecture says this is with replication factor 3. | Code configures CEPH pools with `size: 3` in `ansible/playbooks/initialize-matrix-cluster.yml:78-90`; 24TB raw with size 3 is ~8TB usable, not 12TB. | Change usable capacity to ~8TB for replication factor 3, or change the intended pool replication in code/docs consistently. |
| `documentation/core/infrastructure.md:130` | `Usable Capacity: ~12TB (with CEPH replication factor 2)`. | Same pool evidence: `initialize-matrix-cluster.yml:82-90` sets `size: 3`; `docs/ARCHITECTURE.md:488-489` also documents replication factor 3. | Update to replication factor 3 and ~8TB usable, or explicitly document any intended factor-2 exception. |
| `README.md:44`, `README.md:57` | OpenTofu is `v1.10.x` / `1.10.x` managed via Mise. | Tool versions are intentionally managed in `.mise.toml` (`opentofu` currently pinned there); prose version claims drift when Renovate updates the canonical file. | Remove hardcoded OpenTofu versions from README and point readers to `.mise.toml` as the canonical source of truth. |
| `README.md:86-88` | `CLUSTER=matrix_cluster mise run ansible-ping` tests a specific cluster. | `.mise.toml:74-77` defines `ansible-ping` as `uv run ansible all -m ansible.builtin.ping`; it ignores `CLUSTER`. | Either document `mise run ansible-ping` as all-host only, or change the task to pass `--limit ${CLUSTER:-all}`. |
| `README.md:143-147` | Project tree lists `docs/infrastructure.md`, `docs/goals.md`, `docs/ansible-migration-plan.md`, `docs/ansible-migration-completion.md`, `docs/netbox-powerdns.md`. | Those paths do not exist. Current equivalents are under `documentation/core/` and `docs/archive/2025-11-v1.0/`. | Replace the tree with `documentation/core/{infrastructure,goals,netbox-powerdns}.md` and archive paths. |
| `README.md:206` | `TEMPLATE_NAME=... IMAGE_URL=... mise run ansible:build-template` builds a VM template. | `.mise.toml:137-145` points the task at missing `ansible/playbooks/proxmox-build-template.yml`; current playbooks include `ansible/playbooks/create-template.yml` and deprecated `.deprecated/proxmox-build-template.yml`. | Fix the task to use the current playbook or update docs to the current template command. |
| `README.md:22`, `docs/ARCHITECTURE.md:473`, `docs/ARCHITECTURE.md:593-596`, `documentation/core/goals.md:21`, `documentation/core/infrastructure.md:238`, `documentation/core/netbox-powerdns.md:22`, `documentation/core/netbox-powerdns.md:148` | NetBox + PowerDNS automated DNS/IPAM sync is presented as current/working. | Repository search found no PowerDNS deployment role/playbook/config and no NetBox plugin implementation in Ansible requirements; only docs/research and Terraform NetBox VM/template scaffolding exist. `docs/diagrams/infrastructure-overview.md:98-101` marks NetBox and PowerDNS as planned. | Mark this as planned/in-progress until implementation exists, or add the missing PowerDNS/NetBox sync automation. |
| `docs/ARCHITECTURE.md:42`, `docs/ARCHITECTURE.md:96`, `docs/ARCHITECTURE.md:672-676` | `group_vars/all.yml`, `group_vars/proxmox_clusters.yml`, and per-cluster `group_vars/*.yml` are referenced as paths. | Literal paths do not exist from repo root or `docs/`; actual files are `ansible/inventory/group_vars/*.yml`. | Prefix these references with `ansible/inventory/`. |
| `docs/ARCHITECTURE.md:636` | Collections are `community.proxmox`, `infisical.vault`, `ansible.posix`, `geerlingguy.docker`. | `ansible/requirements.yml:4-25`: `geerlingguy.docker` is a role, not a collection; actual collections also include `community.general`, `ansible.utils`, and `community.docker`. | Split roles vs collections and list the actual requirements. |
| `documentation/README.md:45-48`, `documentation/README.md:81-94`, `documentation/README.md:133-149`, `documentation/README.md:171-187` | `brainstorming/` and `archive/` live under `documentation/`. | These links/paths are broken. Actual directories are `docs/brainstorming/` and `docs/archive/`; there is no `documentation/brainstorming/` or `documentation/archive/`. | Point links to `../docs/brainstorming/...` and `../docs/archive/...`, or move the directories. |
| `documentation/README.md:101-112`, `documentation/README.md:135`, `documentation/README.md:147`, `documentation/README.md:172` | A `mintlify/` directory contains the documentation site source. | No `documentation/mintlify/` directory exists. Mintlify source appears to be `documentation/docs.json`, `documentation/index.mdx`, and content directories directly under `documentation/`. | Replace `mintlify/` references with the actual `documentation/` Mintlify layout. |
| `documentation/README.md:151-162` | Current state: 9 active docs, 3 Ansible design docs, 2 active planning docs, 12 archive docs. | Current counts: `documentation/` has 19 markdown files; `documentation/design/` has 4 markdown files; `docs/brainstorming/` has 3; `docs/archive/` has 13. | Refresh counts or remove brittle counts. |
| `documentation/core/goals.md:47`, `documentation/core/infrastructure.md:250` | Link to `ansible-migration-plan.md`. | Broken relative link; `documentation/core/ansible-migration-plan.md` does not exist. Actual file is `docs/archive/2025-11-v1.0/ansible-migration-plan.md`. | Update link to `../../docs/archive/2025-11-v1.0/ansible-migration-plan.md` or remove from current docs. |

#### Pattern expansion summary

| Pattern | Findings | Root cause |
|---|---:|---|
| CEPH usable-capacity drift | 5 lines across 4 docs | Pool replication changed/standardized to size 3, but capacity text was not updated consistently. |
| Documentation path relocation drift | 20+ broken/misleading refs in `README.md` and `documentation/README.md` | Content moved between `docs/`, `documentation/`, and archives without updating index/tree docs. |
| Planned vs implemented NetBox/PowerDNS | 7 current-tense claims across 5 docs | Architecture/research docs describe target state as current state. |
| Tool/task drift | 3 README claims | Docs duplicate managed tool versions and task behavior instead of deferring to `.mise.toml` as canonical truth. |
| Role inventory drift | Core docs list 6 roles while repo has 9 role directories | New roles were added after v1.0 docs. |

#### Human review queue

- [ ] `docs/diagrams/switch-topology.md`: MAC addresses, switch ports, VLANs, and link speeds need live UniFi/source-of-truth verification; repo has no authoritative switch inventory.
- [ ] Matrix management speed is inconsistent: `README.md:39` says 2.5GbE management, while `docs/diagrams/infrastructure-overview.md:44` and switch topology show 1G Matrix management links. Decide whether docs should state NIC capability or active link speed.
- [ ] Proxmox version target is inconsistent: `ansible/inventory/group_vars/proxmox_clusters.yml:10` says `8.x`, but Matrix docs and `ansible/playbooks/initialize-matrix-cluster.yml:94`/`ansible/roles/proxmox_repository/defaults/main.yml:4` target `9.0`.
- [ ] Hardware, NFS size, PBS reachability, and workload-state claims are mostly mirrored in comments/group vars but need live Proxmox/TrueNAS/PBS validation.
- [ ] ADR currentness: ADR-0002 says Quantum runs NetBox/PowerDNS, while diagram docs mark those services planned. Decide if ADR wording should be future-tense/decision-only.

#### Gap-detection notes

- Actual Ansible roles: `proxmox_repository`, `proxmox_template`, `proxmox_network`, `proxmox_access`, `proxmox_cluster`, `system_user`, `proxmox_ceph`, `proxmox_tuning`, `proxmox_lxc`. Core docs and `documentation/roles/` only cover/list the original 6; `proxmox_lxc`, `proxmox_template`, and `proxmox_tuning` are undocumented in this core set.
- Inventory split: docs emphasize `ansible/inventory/proxmox.yml` with `nexus_cluster`, `quantum_cluster`, and `matrix_cluster`; Mise tasks use `ansible/inventory/hosts.yml`, which still has `doggos_cluster` and standalone `alpha`/`bravo`. This may cause operational docs to diverge from executed tasks.
- NetBox exists as Terraform VM/template scaffolding (`terraform/netbox-vm`, `terraform/netbox-template`), but no corresponding PowerDNS deployment/sync automation was found in Ansible roles, playbooks, or requirements.

---

#### Getting Started Documentation Audit Findings

Generated: 2026-05-05 | Commit: `1d24515`

#### Docs scanned

- `documentation/getting-started/prerequisites.md`
- `documentation/getting-started/installation.md`
- `documentation/getting-started/first-deployment.md`

#### False claims requiring fixes

| Doc line | Claim | Reality / evidence | Suggested fix |
|---|---|---|---|
| `prerequisites.md:50`, `:67`, `:70`; `installation.md:154-162`; `first-deployment.md:58-65`, `:146`, `:150`, `:154`, `:200`, `:282`, `:315`, `:323`, `:331`, `:339` | Matrix/getting-started nodes use `192.168.3.11-.13` and CEPH public IP `192.168.5.11`. | Current Matrix inventory/config uses node ids/IP suffixes `5`, `6`, `7`: `ansible/inventory/hosts.yml:8-16`, `ansible/inventory/proxmox.yml:21-28`, `ansible/inventory/group_vars/matrix_cluster.yml:18,26,32`, and `ansible/playbooks/initialize-matrix-cluster.yml:20-34`. | Update examples and SSH/ping commands to `192.168.3.5-.7` / `192.168.5.5-.7`, or label `.11-.13` as a user-supplied example unrelated to Matrix. |
| `installation.md:16-22`, `:72-84` | The installation guide / `mise run setup` installs the Infisical CLI. | Infisical is not in `.mise.toml` `[tools]` (`.mise.toml:14-27`). `setup` runs `hooks-install`, which calls `infisical scan install` and therefore assumes the CLI already exists (`.mise.toml:32-35`, `:197-200`). `prerequisites.md:87` also lists Infisical CLI as already installed. | Move Infisical CLI install before `mise run setup`, add Infisical to managed tools, or say setup assumes Infisical CLI is installed. |
| `installation.md:103-112` | Expected versions are Python `3.13.x` and OpenTofu `1.10.x`. | Tool versions are canonical in `.mise.toml`; compatibility constraints belong in authoritative metadata such as `pyproject.toml:6` (`requires-python = ">=3.13"`). Prose version pins drift when Renovate updates `.mise.toml`. | Remove hardcoded Python/OpenTofu version expectations from the guide. Say tools are installed via mise and link to `.mise.toml`; keep only compatibility constraints from authoritative config files. |
| `first-deployment.md:43` | `ansible/inventory/proxmox.yml.example` exists and should be copied. | No `ansible/inventory/proxmox.yml.example` exists; current inventories are `ansible/inventory/proxmox.yml` and `ansible/inventory/hosts.yml`. | Remove the copy step, add the example file, or copy from an existing template path. |
| `first-deployment.md:70-83` | Cluster variables should be configured via `network_config`. | Current network role/playbook expects `proxmox_bridges` or `proxmox_vlans` (`ansible/playbooks/configure-network.yml:44-49`); Matrix config uses `proxmox_bridges`/`proxmox_vlans` in `ansible/inventory/group_vars/matrix_cluster.yml:14-41`. `network_config` is not consumed by the current playbook path. | Replace this snippet with the current `proxmox_bridges`/`proxmox_vlans` schema. |
| `first-deployment.md:88` | `uv run ansible-inventory --list` validates the inventory from repo root. | The only `ansible.cfg` is under `ansible/` and sets `inventory = inventory` (`ansible/ansible.cfg:1-3`); `.mise` Ansible tasks run from `ansible/` with explicit `inventory/hosts.yml` (`.mise.toml:109-117`). | Use `cd ansible && uv run ansible-inventory -i inventory/hosts.yml --list` or `-i ansible/inventory/hosts.yml` from repo root. |
| `first-deployment.md:166-177`, `:238-250` | `mise run ansible:init-cluster` only forms the cluster, then a separate `mise run ansible:deploy-ceph` deploys CEPH. | `.mise.toml:128-135` maps `ansible:init-cluster` to `playbooks/initialize-matrix-cluster.yml`; that playbook includes repository, cluster, and CEPH roles in one run (`ansible/playbooks/initialize-matrix-cluster.yml:121-134`). There is no `ansible:deploy-ceph` task and no `ansible/playbooks/deploy-ceph.yml`. | Either document one combined initialization command, or add a separate deploy-CEPH task/playbook and adjust `init-cluster` scope. |
| `first-deployment.md:23`, `:300`, `:358` | CEPH provides `12TB` / `12 TiB` usable capacity. | Matrix CEPH pool replication is `size: 3` (`ansible/playbooks/initialize-matrix-cluster.yml:78-90`). With 24TB raw (2×4TB×3 nodes), usable capacity is roughly 8TB, not 12TB. | Change usable capacity to ~8TB for replication factor 3, or change the intended replication/capacity model consistently. |
| `first-deployment.md:368` | `troubleshooting-basics.md` exists. | `documentation/getting-started/troubleshooting-basics.md` is missing. | Add the troubleshooting page or link to an existing troubleshooting section/doc. |
| `prerequisites.md:148`, `installation.md:12`, `installation.md:178` | Relative links use `documentation/getting-started/...` from inside `documentation/getting-started/`. | As Markdown-relative links, these resolve to nested non-existent paths such as `documentation/getting-started/documentation/getting-started/installation`; sibling links in `first-deployment.md:14-15` correctly use `prerequisites.md` / `installation.md`. | Change to sibling links (`installation.md`, `prerequisites.md`, `first-deployment.md`) or root-absolute Mintlify routes if supported. |

#### Pattern expansion summary

| Pattern | Findings | Root cause |
|---|---:|---|
| Stale Matrix node addressing | Repeated `.11-.13` / `.5.11` examples across all three getting-started docs | Matrix node IDs/IPs changed to suffixes `5`, `6`, `7`, but onboarding examples were not refreshed. |
| Missing artifact references | Missing `proxmox.yml.example`, missing `troubleshooting-basics.md`, missing `ansible:deploy-ceph` task/playbook | Getting-started docs appear generated from a planned flow that was not fully implemented. |
| Combined-vs-split deployment drift | Cluster and CEPH are documented as separate phases, but current `initialize-matrix-cluster.yml` runs both | Playbook consolidation was not reflected in the tutorial. |
| Tool/version drift | Python/OpenTofu expected versions and Infisical install flow are stale | Docs should not track managed tool versions; `.mise.toml` is canonical for pins, while Infisical remains an external prerequisite unless added there. |
| Variable schema drift | `network_config` snippet does not match current `proxmox_network` role variables | Network role now uses `proxmox_bridges`/`proxmox_vlans`. |

#### Human review queue

- [ ] `prerequisites.md:12-21`: Hardware minimums/recommendations should be validated against actual deployment policy and Proxmox/CEPH sizing guidance.
- [ ] `prerequisites.md:55-59`, `first-deployment.md:105-106`, `:149-155`, `:350`: MTU 9000/jumbo-frame claims require live switch and node verification.
- [ ] `first-deployment.md:6-10`, `:28-34`, `:140`, `:195`, `:277`: Deployment duration claims need current run logs on Matrix hardware.
- [ ] `first-deployment.md:171`: “No service disruption expected” during cluster formation should be reviewed against live Proxmox behavior and operational risk tolerance.
- [ ] Infisical CLI commands (`infisical secrets`, `infisical login --token`) should be checked against the currently installed CLI version/help output.

#### Gap-detection notes

- Getting-started docs do not mention that `mise run setup` installs pre-commit hooks and runs `infisical scan install --pre-commit-hook`, which can fail before Infisical is configured.
- The tutorial does not document the current canonical inventory choice: `.mise.toml` tasks use `ansible/inventory/hosts.yml`, while some docs point at `ansible/inventory/proxmox.yml`.
- No getting-started troubleshooting page exists despite the first-deployment next link.
- There is no standalone getting-started path for running only CEPH after networking/cluster if the combined `initialize-matrix-cluster.yml` has already been partially run.

---

#### Ansible/Scripts Documentation Audit Findings

Generated: 2026-05-05 | Commit: `1d24515`

#### Docs scanned

- `ansible/README.md`
- `scripts/README.md`
- `scripts/firecrawl_sdk_research.py.README.md`

#### False claims requiring fixes

| Doc line | Claim | Reality / evidence | Suggested fix |
|---|---|---|---|
| `ansible/README.md:16`, `:53` | Ansible code/roles have zero ansible-lint violations under the **production** profile. | `ansible/.ansible-lint` sets `profile: moderate`, not production. Current docs do not cite a current production-profile run. | Say `moderate` profile, or switch config/CI to production profile and publish current passing output. |
| `ansible/README.md:18`, `:39-45`, `:55-62` | Available/complete role docs list all roles. | Repo has 9 role dirs: `proxmox_access`, `proxmox_ceph`, `proxmox_cluster`, `proxmox_lxc`, `proxmox_network`, `proxmox_repository`, `proxmox_template`, `proxmox_tuning`, `system_user`; README lists only 6 and omits LXC/template/tuning. | Add the 3 missing roles to the tree/table, or label the table as a legacy/core subset. |
| `ansible/README.md:21`, `:344` | Link `../docs/ansible-migration-completion.md` exists. | Target `docs/ansible-migration-completion.md` is missing; actual archived file is `docs/archive/2025-11-v1.0/ansible-migration-completion.md`. | Update link to archive path or remove from current docs. |
| `ansible/README.md:75` | Playbook `playbooks/proxmox-build-template.yml` is available. | `ansible/playbooks/proxmox-build-template.yml` is missing; only deprecated `ansible/playbooks/.deprecated/proxmox-build-template.yml` and current `create-template*.yml` playbooks exist. | Replace with `create-template.yml`/`create-template-doggos.yml`, or restore the playbook. |
| `ansible/README.md:282`, `:345` | Link `../docs/ansible-philosophy.md` exists. | Target is missing; current file is `documentation/design/ansible-philosophy.md`. | Update relative link to `../documentation/design/ansible-philosophy.md`. |
| `ansible/README.md:346` | Link `../docs/testing-validation-results.md` exists. | Target is missing; archived file is `docs/archive/2025-11-v1.0/testing-validation-results.md`. | Update link to archive path or remove stale reference. |
| `ansible/README.md:347` | Link `../docs/infrastructure.md` exists. | Target is missing; current infrastructure doc is `documentation/core/infrastructure.md`. | Update link to `../documentation/core/infrastructure.md`. |
| `ansible/README.md:351` | Link `../.claude/skills/ansible-best-practices/` exists. | No `.claude/skills/ansible-best-practices/` directory exists in this repo. | Remove the link or point to an existing skill/rule location. |
| `scripts/README.md:31` | All scripts require Python 3.11 or higher. | Script-level metadata differs: `scripts/validator.py:3` declares `requires-python = ">=3.10"`, `scripts/firecrawl_sdk_research.py:3` declares `>=3.11`, and root `pyproject.toml:6` requires `>=3.13`. Managed runtime pins belong in `.mise.toml`, not prose. | Avoid a single hardcoded prose Python version. State that script requirements are defined by each script's metadata/root `pyproject.toml`, and that local tool pins come from `.mise.toml`. |
| `scripts/README.md:122-132` | Running root `./conductor-setup.sh` after cloning initializes the environment. | `conductor-setup.sh:20` and `:27` read `$CONDUCTOR_ROOT_PATH` under `set -u`; without that environment variable, direct execution can fail before setup. | Document the required Conductor environment variable, or default it to the repo root in the script. |
| `scripts/README.md:267` | Link `../docs/infrastructure.md` exists. | Target is missing; current infrastructure doc is `documentation/core/infrastructure.md`. | Update link to `../documentation/core/infrastructure.md`. |
| `scripts/firecrawl_sdk_research.py.README.md:112-113`, `:122-123`, `:237` | Category values are documented as `GitHub`/`GitHub,research`. | Code/help uses lowercase examples/help (`github`, `research`, `pdf`) and does not normalize category case: `scripts/firecrawl_sdk_research.py:466-500`; `uv run ... --help` prints lowercase. | Make docs consistently lowercase or normalize category values before calling Firecrawl. |
| `scripts/firecrawl_sdk_research.py.README.md:175-179` | Results are filtered to exclude low-quality domains. | `filter_quality()` excludes short content and error pages, but does not exclude domains; unknown domains are kept with lower/no score (`scripts/firecrawl_sdk_research.py:207-282`). | Rephrase to “trusted domains receive a score boost,” or implement a domain deny/allow filter. |
| `scripts/firecrawl_sdk_research.py.README.md:195` | If combined search+scrape fails, the script falls back to separate operations. | `research()` always calls `search_and_scrape(... scrape_options=...)`; if that call raises after retries, there is no try/except fallback. Separate scraping only happens when the search succeeds but returns no markdown (`scripts/firecrawl_sdk_research.py:400-427`). | Add a real fallback search without `scrape_options`, or remove the failure-fallback claim. |

#### Pattern expansion summary

| Pattern | Findings | Root cause |
|---|---:|---|
| Broken relocated documentation links | 8 broken links in `ansible/README.md`, 1 in `scripts/README.md` | Docs moved from `docs/` to `documentation/` or `docs/archive/2025-11-v1.0/` without updating README links. |
| Inventory drift in Ansible overview | README lists 6 roles and one missing playbook while repo has 9 roles and 13 current playbooks | README predates later LXC/template/tuning roles and playbook renames. |
| Script behavior/API drift | Firecrawl README overstates fallback behavior and low-quality-domain filtering; category case differs from code help | CLI docs were not regenerated after implementation details settled. |

#### Human review queue

- [ ] `ansible/README.md:14`, `:17`, `:190-200`, `:280`: idempotency/test-coverage claims need current integration or CI run evidence, especially on live Proxmox/API tasks.
- [ ] `ansible/README.md:8`: Proxmox target version needs product decision; repo contains both PVE 9.0 defaults and `ansible/inventory/group_vars/proxmox_clusters.yml` with `proxmox_target_version: "8.x"`.
- [ ] `scripts/firecrawl_sdk_research.py.README.md:198-210`: Firecrawl credit/cost claims depend on external Firecrawl pricing and should be checked against current provider docs.
- [ ] Firecrawl category semantics (`github`, `research`, `pdf`) should be verified against current Firecrawl API behavior; repository code passes strings through without local validation.

#### Gap-detection notes

- `scripts/validator.py` is an actual user-facing utility with CLI help and inline dependencies, but `scripts/README.md` only lists `firecrawl_sdk_research.py` under Available Scripts.
- `ansible/README.md` omits current playbooks including `add-file-to-host.yml`, `create-ansible-user.yml`, `create-template.yml`, `create-template-doggos.yml`, `deploy-omni-provider.yml`, `destroy-osds.yml`, and `system-upgrade.yml`.
- `ansible/README.md` still points readers to historical validation/migration docs via old paths; current docs are split between `documentation/` and `docs/archive/2025-11-v1.0/`.

---

#### Documentation Audit Findings: Generated Role Docs

Generated: 2026-05-05 | Commit: `1d24515`

#### Docs scanned

6 docs scanned:

- `documentation/roles/proxmox_access.md`
- `documentation/roles/proxmox_ceph.md`
- `documentation/roles/proxmox_cluster.md`
- `documentation/roles/proxmox_network.md`
- `documentation/roles/proxmox_repository.md`
- `documentation/roles/system_user.md`

#### False claims requiring fixes

| Doc line(s) | Claim | Reality / evidence | Suggested fix |
|---|---|---|---|
| `proxmox_access.md:22`, `:131`, `:249-269` | Role manages users in both PAM and PVE realms; API-only `@pve` user example is supported. | `ansible/roles/proxmox_access/tasks/users.yml:11-20` only creates users when `"@pam" in item.userid`; there is no task path for creating `@pve` users. | Document PAM-only user creation, or implement `@pve` user creation. Remove/fix API-only example until supported. |
| `proxmox_access.md:106` | `proxmox_roles[].state` supports `present` or `absent`. | `ansible/roles/proxmox_access/tasks/roles.yml:10-17` only creates missing roles; no removal branch and no `state` check. | Remove `absent` from role state docs or add role deletion support. |
| `proxmox_access.md:140` | Token `privsep` default is `false`. | `ansible/roles/proxmox_access/tasks/tokens.yml:17` uses `item.item.privsep \\| default(true)`, so omitted `privsep` results in `-privsep 1`. | Change documented default to `true`, or change role default to `false`. |
| `proxmox_access.md:229-232` | `system_user` example uses `username` and `sudo: nopasswd`. | `system_user` role expects `name` and `sudo_nopasswd`/`sudo_rules`: see `ansible/roles/system_user/tasks/create_users.yml:3-9`, `tasks/main.yml:49-52`, `templates/sudoers.j2:7-15`. | Update example to `name: terraform` and `sudo_nopasswd: true` or `sudo_rules`. |
| `proxmox_access.md:432` | See Also link `[system_user](documentation/roles/system_user)`. | From `documentation/roles/proxmox_access.md`, that relative path resolves to `documentation/roles/documentation/roles/system_user`, not the existing `documentation/roles/system_user.md`. | Change link to `system_user.md`. |
| `proxmox_ceph.md:12` | Role dependencies: requires `proxmox_repository`, `proxmox_cluster`, `proxmox_network`. | Role metadata declares no dependencies: `ansible/roles/proxmox_ceph/meta/main.yml:16` `dependencies: []`. | Rephrase as prerequisites/recommended run order, or encode dependencies in metadata. |
| `proxmox_ceph.md:26`, `:143`, `:322` | Role manages/uses CRUSH rules for pool placement; `ceph_pools[].crush_rule` is a required pool field. | Pool tasks never reference `crush_rule`: `ansible/roles/proxmox_ceph/tasks/pools.yml:6-77` creates pools, sets size/min_size/application/compression only. | Remove CRUSH-rule claims/field, or implement CRUSH rule creation/assignment. |
| `proxmox_ceph.md:47-92`, `:165-229`, `:247-291` | Example OSD deployments will create OSDs as shown. | OSD preparation asserts `ceph_wipe_disks` or `ceph_allow_zap_devices` must be true before disk operations: `ansible/roles/proxmox_ceph/tasks/osd_prepare.yml:2-12`. Examples omit both flags, so they fail before OSD creation. | Add explicit safety flag examples and warning, e.g. `ceph_allow_zap_devices: true` or `ceph_wipe_disks: true`. |
| `proxmox_ceph.md:106-107` | `ceph_network` and `ceph_cluster_network` are required. | Defaults exist: `ansible/roles/proxmox_ceph/defaults/main.yml:6-7` set `192.168.5.0/24` and `192.168.7.0/24`. | Mark as optional with defaults, or remove defaults if truly required. |
| `proxmox_ceph.md:124`, `:127` | OSD `partitions` and `crush_device_class` are required. | `partitions` defaults to `1` in `tasks/osd_create.yml:16,32`; `crush_device_class` is only used if defined in `tasks/osd_create.yml:26,69`. | Mark both optional; document default `partitions: 1`. |
| `proxmox_ceph.md:138-143` | Pool `pg_num`, `pgp_num`, `size`, `min_size`, `application`, and `crush_rule` are required. | `pg_num`, `pgp_num`, `size`, `min_size`, and `application` have task defaults in `tasks/pools.yml:8,19,32,45`; `crush_rule` is unused. | Mark task-defaulted fields optional; remove or implement `crush_rule`. |
| `proxmox_ceph.md:89`, `:350`, `:383`, `:694`, `:833`, `:840`, `:847` | Commands use `playbooks/deploy-ceph.yml`. | File is missing. Actual related playbook is `ansible/playbooks/initialize-matrix-cluster.yml`; `ansible/playbooks/deploy-ceph.yml` does not exist. | Point to existing playbook or add `deploy-ceph.yml`. |
| `proxmox_ceph.md:764`, `:774`, `:786-787` | Split playbooks `playbooks/01-cluster-setup.yml` and `playbooks/02-storage-setup.yml` exist/run. | Both files are missing from `ansible/playbooks/`. | Label as illustrative filenames or add those playbooks. |
| `proxmox_ceph.md:637` | “full idempotency achieved” after fixes. | `ansible/roles/proxmox_ceph/tasks/verify.yml:23-30` accepts both `HEALTH_OK` and `HEALTH_WARN` when `expected_health_status == "HEALTH_OK"`; claim needs runtime evidence and may overstate health/idempotency. | Either cite reproducible test output/current commit, or soften and move to human-verified notes. |
| `proxmox_cluster.md:12` | Role dependencies: requires `proxmox_repository` and `proxmox_network`. | Role metadata declares no dependencies: `ansible/roles/proxmox_cluster/meta/main.yml:16` `dependencies: []`. | Rephrase as prerequisites/recommended run order, or encode dependencies in metadata. |
| `proxmox_cluster.md:107` | `expected_votes` default is `3`. | Default is dynamic: `ansible/roles/proxmox_cluster/defaults/main.yml:28` sets `expected_votes: "{{ groups[cluster_group] | length }}"`. | Document the dynamic default. |
| `proxmox_cluster.md:64`, `:241`, `:249`, `:257`, `:482`, `:590`, `:597`, `:604` | Commands use `playbooks/initialize-cluster.yml`. | File is missing. Actual related playbook is `ansible/playbooks/initialize-matrix-cluster.yml`. | Point to existing playbook or add `initialize-cluster.yml`. |
| `proxmox_cluster.md:532`, `:540`, `:552-553` | Split playbooks `playbooks/01-configure-network.yml` and `playbooks/02-initialize-cluster.yml` exist/run. | Both files are missing from `ansible/playbooks/`. | Label as illustrative filenames or add those playbooks. |
| `proxmox_network.md:312` | Tag `reload` is available for network reload only. | No `reload` tag exists in role tasks. Tags are `proxmox_network`, `prerequisites`, `bridges`, `vlans`, `verify`; `debug` only appears on one prereq debug task. Evidence: `ansible/roles/proxmox_network/tasks/main.yml:3-23`, `tasks/prerequisites.yml:39-48`. | Remove `reload` tag or add a tagged reload task. |
| `proxmox_network.md:357` | Dry-run mode “shows what would change.” | Role skips bridge/VLAN/verify tasks when `proxmox_network_dry_run` is true: `ansible/roles/proxmox_network/tasks/main.yml:8-22`; it does not compute/display pending interface changes. | Rephrase to “skips configuration changes,” or add explicit dry-run diff/report tasks. |
| `proxmox_repository.md:24` | Old kernels are removed automatically. | Cleanup only runs when `auto_remove_old_kernels` is true; default is false: `ansible/roles/proxmox_repository/defaults/main.yml:20`, `tasks/main.yml:19-21`. | Say “optionally remove old kernels.” |
| `proxmox_repository.md:75` | `ceph_repo_enabled` default is `true`. | Actual default is `false`: `ansible/roles/proxmox_repository/defaults/main.yml:11` (`# Let pveceph install manage CEPH repos`). | Update default to `false` and explain when to enable. |
| `proxmox_repository.md:49`, `:232`, `:235`, `:238`, `:333`, `:336`, `:339`, `:342`, `:476` | Commands use `playbooks/configure-repositories.yml`. | File is missing from `ansible/playbooks/`. | Point to an existing playbook or add `configure-repositories.yml`. |
| `proxmox_repository.md:232`, `:235` | Repository playbook supports `--tags cache` and `--tags repos`. | `ansible/roles/proxmox_repository/tasks/*.yml` contain no task tags; `grep` found no role task tags. | Add tags to repository tasks or remove selective-execution claims. |
| `proxmox_repository.md:289` | Upgrade command uses `playbooks/upgrade-proxmox.yml`. | File is missing; existing related playbook is `ansible/playbooks/system-upgrade.yml`. | Change command to `playbooks/system-upgrade.yml` or add `upgrade-proxmox.yml`. |
| `system_user.md:20`, `:61-64`, `:72-88` | Role creates users with specific UID/GID and supports `uid`, `gid`, `home`. | `ansible/roles/system_user/tasks/create_users.yml:3-9` passes only `name`, `comment`, `shell`, `groups`, `create_home`, `state`; no `uid`, `gid`, or `home`. | Remove unsupported fields or implement them in the role. |
| `system_user.md:37`, `:59`, `:74`, `:106`, `:129` | User variable is `username`. | Role uses `user_item.name`: `tasks/create_users.yml:3-5`, `tasks/main.yml:19,37,48`; defaults examples also use `name`: `defaults/main.yml:10,26,36,48`. | Replace `username` with `name` throughout. |
| `system_user.md:42`, `:66`, `:83`, `:108`, `:169` | Sudo access is configured with `sudo: nopasswd/password`. | Role uses `sudo_nopasswd` and/or `sudo_rules`, not `sudo`: `tasks/main.yml:49-52`, `templates/sudoers.j2:7-15`. No password-prompt sudo mode is implemented. | Replace with `sudo_nopasswd: true` or `sudo_rules`; remove `password` mode or implement it. |
| `system_user.md:48` | Run `uv run ansible-playbook create-automation-user.yml`. | `create-automation-user.yml` is missing at repo root and under `ansible/playbooks/`. Existing related playbooks: `create-admin-user.yml`, `create-ansible-user.yml`, `setup-terraform-automation.yml`. | Point to an existing playbook or add `create-automation-user.yml`. |
| `system_user.md:51` | Quick Start creates Terraform user with SSH key and sudo access. | The snippet uses unsupported `username`/`sudo`; role would not create the intended user because `name` is required and sudo condition ignores `sudo`. Evidence above. | Fix snippet with `name: terraform` and supported sudo keys. |
| `system_user.md:115-117` | `proxmox_access` token keys are `user`, `name`, `privilege_separation`. | `proxmox_access` expects `userid`, `tokenid`, `privsep`: `ansible/roles/proxmox_access/tasks/tokens.yml:7,17,65`. | Change integration example to `userid`, `tokenid`, `privsep`. |

#### Pattern expansion summary

| Pattern | Count / scope | Root cause |
|---|---:|---|
| Missing generated playbook references | 37 line hits across `proxmox_ceph.md`, `proxmox_cluster.md`, `proxmox_repository.md`, `system_user.md` | Docs refer to generic/generated playbook names that do not exist in `ansible/playbooks/`; repo has `configure-network.yml`, `initialize-matrix-cluster.yml`, `setup-terraform-automation.yml`, `system-upgrade.yml`, etc. |
| Role variable schema drift | Broad in `system_user.md`; also `proxmox_access` token defaults and integration examples | Generated docs use older/friendlier API names (`username`, `sudo`, `user`, `name`, `privilege_separation`) instead of role task/default variable names (`name`, `sudo_nopasswd`, `sudo_rules`, `userid`, `tokenid`, `privsep`). |
| Required-vs-default mismatch | `proxmox_ceph.md`, `proxmox_cluster.md`, `proxmox_repository.md` | Docs mark defaulted variables as required or cite static defaults that changed in role defaults. |
| Unsupported selective tags | `proxmox_repository.md`, one `proxmox_network.md` tag | Docs advertise tags not present on role tasks. |
| CEPH safety gate omitted from examples | `proxmox_ceph.md` examples | Role now requires explicit destructive-operation flags; generated examples predate that guardrail. |

#### Human review queue

- [ ] `proxmox_access.md:14`, `proxmox_ceph.md:14`, `proxmox_cluster.md:14`, `proxmox_network.md:14`, `proxmox_repository.md:14`, `system_user.md:14`: “Battle-Tested” Matrix cluster production/idempotency claims need external run logs or deployment records.
- [ ] `proxmox_ceph.md:14`, `:229`: 12 OSD / 24TB raw / 8TB usable capacity claims need inventory/hardware confirmation outside role code.
- [ ] `proxmox_ceph.md:109`, `:541-545`, `:643-682`: performance best-practice claims (10GbE minimum, MTU 9000 benefits, device-class performance) are plausible but external/operational rather than repo-verifiable.
- [ ] `proxmox_cluster.md:487-491`: “cannot remove nodes without data loss” / “breaking cluster destroys shared storage access” should be reviewed for accuracy/wording against Proxmox operational docs.
- [ ] `proxmox_network.md:320-321`: exact backup filename shape and “subsequent changes skip backup” depends on `community.general.interfaces_file` backup behavior at runtime.
- [ ] `proxmox_ceph.md:637`: idempotency result should be linked to reproducible test output for the current commit, not historical commit `d4af18b` alone.

#### Gap-detection notes

- `proxmox_ceph.md` omits documented defaults/controls present in role defaults: `ceph_repository`, `ceph_allow_zap_devices`, `ceph_wipe_disks`, `ceph_mon_group`, `ceph_mgr_group`, and `expected_health_status` (`ansible/roles/proxmox_ceph/defaults/main.yml`).
- `proxmox_repository.md` omits newer controls in defaults: `run_system_upgrade`, `system_upgrade_auto_reboot`, `validate_certs`, `remove_subscription_banner`, `pigz_enabled`, `pigz_compression_level`.
- `system_user.md` omits supported controls `name`, `create_home`, `sudo_nopasswd`, and `sudo_rules`, while documenting unsupported `username`, `uid`, `gid`, `home`, and `sudo`.
- `proxmox_access.md` does not clearly document direct credential requirements (`proxmox_api_user`, `proxmox_api_password`) used by API module tasks when Infisical is not used; it also omits optional `firstname`, `lastname`, and token `expire` fields supported by tasks.
- Selected docs do not cover generated/current role docs for other roles present in `ansible/roles/` such as `proxmox_lxc`, `proxmox_template`, and `proxmox_tuning` (outside requested scope, but visible inventory gap if this docs set is meant to be complete).

---

#### Ansible Role README Documentation Audit Findings

Generated: 2026-05-05 | Commit: `1d24515`

#### Scope

Docs scanned: 9

- `ansible/roles/proxmox_access/README.md`
- `ansible/roles/proxmox_ceph/README.md`
- `ansible/roles/proxmox_cluster/README.md`
- `ansible/roles/proxmox_lxc/README.md`
- `ansible/roles/proxmox_network/README.md`
- `ansible/roles/proxmox_repository/README.md`
- `ansible/roles/proxmox_template/README.md`
- `ansible/roles/proxmox_tuning/README.md`
- `ansible/roles/system_user/README.md`

Verification covered file refs, config defaults, CLI/playbook commands, version claims, and behavior claims against each role's `defaults/`, `tasks/`, `handlers/`, `templates/`, and `meta/` files. Pass 2 pattern expansion checked repeated missing-playbook references, default mismatches, and unsupported-feature families.

#### False Claims Requiring Fixes

| Doc line | Claim | Reality / evidence | Suggested fix |
|---|---|---|---|
| `proxmox_access/README.md:11` | Role "Creates and manages Proxmox users in PAM and PVE realms". | `tasks/users.yml` only creates users when `"'@pam' in item.userid"`; there is no creation path for `@pve` users. | Change claim to PAM-user creation only, or implement `@pve` user creation. |
| `proxmox_access/README.md:17` | Role supports creation and removal via `state` parameter. | `tasks/roles.yml` only runs `pveum role add`; it never checks `item.state` or removes roles. State is supported for groups/users/tokens/ACLs, not custom roles. | Clarify state support excludes `proxmox_roles`, or add role deletion/update handling. |
| `proxmox_access/README.md:220-243` | API-only PVE realm example implies `proxmox_users: userid: api_user@pve` will be created by the role. | Same evidence: `tasks/users.yml` skips non-`@pam` users on creation; token creation will fail unless `api_user@pve` already exists. | Mark the PVE user as pre-existing, or implement `@pve` creation. |
| `proxmox_ceph/README.md:15` | Role "Configures CRUSH rules". | `tasks/pools.yml` creates pools and sets size/min_size/application/compression, but never creates CRUSH rules or applies `item.crush_rule`. | Remove the feature claim or add CRUSH rule configuration tasks. |
| `proxmox_ceph/README.md:101` | `crush_rule: replicated_rule` is shown as a pool setting. | `tasks/pools.yml` does not read or apply `crush_rule`; grep found only README/default comments, no task usage. | Remove from documented variables or wire it into pool creation/configuration. |
| `proxmox_ceph/README.md:103-108` | `ceph_pools` default/sample block includes `vm_containers`. | Actual `defaults/main.yml` defines only one default pool: `vm_ssd`; no `vm_containers` default. | Either add `vm_containers` to defaults or label it clearly as an example-only extra pool. |
| `proxmox_ceph/README.md:246,250,254` | Testing commands use `playbooks/deploy-ceph.yml`. | `ansible/playbooks/deploy-ceph.yml` does not exist. Available related playbooks include `destroy-osds.yml` but no deploy-ceph playbook. | Add the playbook or update commands to the actual orchestration entrypoint. |
| `proxmox_cluster/README.md:53` | `expected_votes: 3` shown as the role variable default. | Actual `defaults/main.yml`: `expected_votes: "{{ groups[cluster_group] | length }}"`. | Change documented default to the Jinja expression, or mark `3` as an example value. |
| `proxmox_cluster/README.md:140,143,146` | Testing commands use `playbooks/initialize-cluster.yml`. | `ansible/playbooks/initialize-cluster.yml` does not exist; repository has `initialize-matrix-cluster.yml`. | Update commands to `playbooks/initialize-matrix-cluster.yml` or add the generic playbook. |
| `proxmox_repository/README.md:36` | `ceph_repo_enabled: true` default enables CEPH repository. | Actual `defaults/main.yml`: `ceph_repo_enabled: false  # Let pveceph install manage CEPH repos`. | Change documented default to `false` and explain when to enable. |
| `proxmox_repository/README.md:92,95,98` | Testing commands use `playbooks/configure-repositories.yml`. | `ansible/playbooks/configure-repositories.yml` does not exist. | Add this playbook or point to the actual repository/system-upgrade playbook. |
| `system_user/README.md:309` | Related doc link `../../../docs/ansible-migration-plan.md`. | Target resolves to `docs/ansible-migration-plan.md`, which does not exist; matching content appears under `docs/archive/2025-11-v1.0/ansible-migration-plan.md`. | Update link to archive path or remove stale reference. |
| `system_user/README.md:310` | Related doc link `.claude/skills/ansible-best-practices/`. | Relative to the README, `ansible/roles/system_user/.claude/skills/ansible-best-practices/` does not exist; no matching repo-root skill directory was found either. | Remove or correct the link. |

#### Pass 2 Pattern Summary

| Pattern expanded | Findings |
|---|---|
| Missing playbook commands | Found repeated missing playbook references in role READMEs: `deploy-ceph.yml`, `initialize-cluster.yml`, and `configure-repositories.yml`. Existing playbook refs for `setup-terraform-automation.yml`, `configure-network.yml`, `create-template.yml`, and `create-admin-user.yml` resolved correctly. Placeholder `playbooks/your-playbook.yml` in `proxmox_lxc` was treated as non-claim/example placeholder. |
| Config default mismatch | Confirmed mismatches for `ceph_repo_enabled`, `expected_votes`, and the extra `vm_containers` pool. Other sampled defaults in LXC, network, template, tuning, and system_user matched role defaults/tasks. |
| Unsupported feature family | `proxmox_access` PVE-user creation/state support and `proxmox_ceph` CRUSH-rule support are documented but not implemented. |
| Dead related docs | `system_user` related-documentation links include two stale/missing targets. |

#### Human Review Queue

- [ ] `proxmox_access/README.md:437-442` idempotency claims are broadly supported by task guards, but full second-run behavior depends on live Proxmox/API module behavior.
- [ ] `proxmox_ceph/README.md:278-283` historical idempotency test results and commit `d4af18b` were not re-run or verified in git history during this pass.
- [ ] `proxmox_repository/README.md:19-21` plus role metadata/defaults mix PVE 9.x, Debian Bookworm, and `proxmox_version: "9.0"`; review desired PVE/Debian support matrix.
- [ ] Runtime behavior claims requiring live hosts (network reload interruption, CEPH quorum/health, template boot behavior, actual sudo/SSH access) need integration testing on Proxmox nodes.

#### Gap-Detection Notes

- `proxmox_ceph/defaults/main.yml` includes important undocumented controls: `ceph_mon_group`, `ceph_mgr_group`, `ceph_allow_zap_devices`, `ceph_wipe_disks`, `ceph_repository`, and `expected_health_status`.
- `proxmox_repository/defaults/main.yml` includes undocumented controls: `run_system_upgrade`, `system_upgrade_auto_reboot`, and `validate_certs`.
- `proxmox_template/defaults/main.yml` includes undocumented `proxmox_template_os_type`.
- `proxmox_tuning/defaults/main.yml` exposes many network tuning variables (`net_core_*`, `net_ipv4_tcp_*`) not listed under "All Available Variables" despite `proxmox_tuning_network_enabled` being documented.
- No edits were made to audited documentation.

---

#### Terraform Documentation Audit Findings

Generated: 2026-05-05 | Commit: `1d24515`

#### Docs scanned

- `terraform/README.md`
- `terraform/netbox-template/README.md`
- `terraform/netbox-vm/README.md`
- `terraform/examples/microk8s-cluster/README.md`
- `terraform/examples/template-with-custom-cloudinit/README.md`

#### False claims requiring fixes

| Doc line | Claim | Reality / evidence | Suggested fix |
|---|---|---|---|
| `terraform/README.md:23` | “All configurations use the external module from `github.com/basher83/Triangulum-Prime//terraform-bgp-vm`” | Top-level `netbox-*` configs do, but examples do not: `terraform/examples/microk8s-cluster/main.tf:87` and `terraform/examples/template-with-custom-cloudinit/main.tf:43` use `../../../modules/vm`; no `modules/vm` or `terraform/modules/vm` directory exists. | Say top-level configs use the external module, and fix example module sources or document that examples are currently stale. |
| `terraform/README.md:80` | `netbox-vm/README.md` is a “comprehensive 557-line guide” | Actual line count is 636 (`wc -l terraform/netbox-vm/README.md`). | Remove the line-count claim or update it. |
| `terraform/README.md:335` | Link to `../docs/infrastructure.md` | Target does not exist; current infrastructure doc is `documentation/core/infrastructure.md`. | Change to `../documentation/core/infrastructure.md`. |
| `terraform/README.md:336` | Link to `../docs/goals.md` | Target does not exist; current goals doc is `documentation/core/goals.md`. | Change to `../documentation/core/goals.md`. |
| `terraform/netbox-template/README.md:550` | Link to `../../docs/infrastructure.md` | Target does not exist; current infrastructure doc is `documentation/core/infrastructure.md`. | Change to `../../documentation/core/infrastructure.md`. |
| `terraform/netbox-vm/README.md:14`, `:148`, `:254-285`, `:484`, `:619` | Lifecycle / `prevent_destroy` / boot-order examples are supported by this VM config | `terraform/netbox-vm/variables.tf` has no `prevent_destroy`, `boot_order`, `boot_up_delay`, or `boot_down_delay`; `variables.tf:274` explicitly says boot-delay variables were removed. | Remove these examples/claims or reintroduce supported variables and wire them into `main.tf`. |
| `terraform/netbox-vm/README.md:218` | `cpu_type = "host"` is configurable in this example | `terraform/netbox-vm/variables.tf` has no `cpu_type`; `main.tf:39` says CPU type defaults to host and is not specified. `terraform.tfvars.example:35` also contains this stale variable. | Remove `cpu_type` from README and example tfvars, or add and wire a `cpu_type` variable. |
| `terraform/netbox-vm/README.md:45-49` | Copying `terraform.tfvars.example` gives a valid customization base | The copied example includes stale variables not declared by `variables.tf`: `cpu_type`, `boot_order`, `boot_up_delay`, `boot_down_delay` (`terraform/netbox-vm/terraform.tfvars.example:35,81-83`). | Clean up `terraform.tfvars.example`; then the README quick start is accurate. |
| `terraform/netbox-vm/README.md:592` | Link/use “vm-cluster module” at `../microk8s-cluster/` | Link target from this doc does not exist; actual example is `terraform/examples/microk8s-cluster/`. No `modules/vm-cluster` exists. | Change link to `../examples/microk8s-cluster/` and describe it as a `for_each` example, not a module. |
| `terraform/netbox-vm/README.md:597`, `:602`, `:609-610` | Local module docs/sources `../../../modules/vm` and `../../../modules/vm-cluster` exist | No repository `modules/vm` or `modules/vm-cluster` exists. Current working configs use external `github.com/basher83/Triangulum-Prime//terraform-bgp-vm?ref=v1.0.0`. | Replace with the external module source/docs or remove local-module references. |
| `terraform/netbox-vm/README.md:611-612` | Links to `../../../../docs/terraform/proxmox-vm-provisioning-guide.md` and `../../../../CLAUDE.md` | Both resolve outside this repo / do not exist from `terraform/netbox-vm`. `CLAUDE.md` is `../../CLAUDE.md`. No `docs/terraform/proxmox-vm-provisioning-guide.md` exists. | Fix CLAUDE link to `../../CLAUDE.md`; remove or replace the missing Proxmox guide link. |
| `terraform/examples/microk8s-cluster/README.md:47`, `:392`, `:417` | Example/module docs use `../../../modules/vm` | `terraform/examples/microk8s-cluster/main.tf:87` also uses this path, but no target exists. | Update example source to the external module (`github.com/basher83/Triangulum-Prime//terraform-bgp-vm?ref=v1.0.0`) and regenerate docs. |
| `terraform/examples/microk8s-cluster/README.md:72`, `:133-150`, `:248-260`, `:317`, `:320`, `:335` | Commands/prereq use `terraform` | Project root explicitly requires OpenTofu commands: `terraform/README.md:5-12` and best practice at `:349` say use `tofu`, not `terraform`. Tool version pins are canonical in `.mise.toml`. | Replace command examples with `tofu ...`; avoid hardcoded OpenTofu version claims and point tool installation/version details to `.mise.toml`. |
| `terraform/examples/microk8s-cluster/README.md:317`, `:320`, `:326-327` | Ansible export path `../../../../ansible/...`, `cd ../../../../ansible`, and playbook `playbooks/microk8s-deploy.yml` | From the example directory, `../../../../ansible` resolves outside the repo. Repo path should be `../../../ansible`; also no `ansible/playbooks/microk8s-deploy.yml` exists. | Use `../../../ansible/...` paths and either add/document the real MicroK8s playbook or remove the playbook command. |
| `terraform/examples/microk8s-cluster/README.md:393` | Link to `../../../../docs/terraform/proxmox-vm-provisioning-guide.md` | Target does not exist. | Remove or replace with an existing Terraform/root doc. |
| `terraform/examples/template-with-custom-cloudinit/README.md:61` | Module source is `../../../modules/vm` | README reflects `main.tf:43`, but that source path is broken because no local module exists. | Update example source to the external module and regenerate terraform-docs. |

#### Human review queue

- Verify external module default claims (`vm_bios = ovmf`, `vm_machine = q35`, `vm_os = l26`, agent timeout/trim, serial defaults) against the remote Triangulum-Prime module/`DEFAULTS.md`; those defaults are not vendored in this repo.
- Operational Proxmox claims need environment validation: template “cloud icon,” non-startable templates, SSH import behavior, cross-node cloning, guest-agent IP fallback, and datastore restrictions.

#### Gap-detection / pattern notes

- **Stale local-module pattern:** README and generated docs still reference `../../../modules/vm`, `../../../modules/vm-cluster`, and `terraform/modules/vm/DEFAULTS.md`, but there is no local module tree. Top-level configs were migrated to the external Triangulum-Prime module; examples were not.
- **OpenTofu command drift:** Only `terraform/examples/microk8s-cluster/README.md` still uses `terraform` commands; the other Terraform docs use `tofu`.
- **Missing doc-link pattern:** `docs/infrastructure.md`, `docs/goals.md`, and `docs/terraform/proxmox-vm-provisioning-guide.md` links are stale. Current core docs live under `documentation/core/`.
- **Unsupported variable pattern:** `netbox-vm` docs and `terraform.tfvars.example` mention removed knobs (`cpu_type`, `prevent_destroy`, boot order/delays). These should either be reintroduced in code or removed from docs/examples.
