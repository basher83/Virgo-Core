## [unreleased]

### 🚀 Features

- *(skills)* Major enhancement to Claude Code skills with 10,000+ lines of automation content
- *(skills)* Complete Tier 1 improvements for skill library
- *(terraform)* Add comprehensive OpenTofu deployment examples

### 🐛 Bug Fixes

- Resolve 18 CodeRabbit issues across documentation, code quality, and security
- *(security)* Resolve command injection vulnerabilities and improve validation
- Use correct negative index syntax for last CLI argument
- Mark validation invalid when shebang missing in strict mode
- Add UTF-8 encoding and UnicodeDecodeError handling to file reading
- Improve metadata block extraction for cross-platform compatibility
- Correct example link to check_cluster_health_enhanced.py
- Correct relative link path to ansible-best-practices
- Add default fallback to all cluster_group variable references
- Fix CEPH manager list to use proper list membership test
- Use strict majority for CEPH monitor quorum check
- Add exit code to JSON output path in check_ceph_health.py
- Add timeout and improve error handling in check_ceph_health.py
- Add rollback on IP creation failure and remove unnecessary f-strings
- Harden get_netbox_client with specific exception handling
- Materialize pynetbox iterators once to avoid re-fetching
- Improve CEPH OSD count validation with robust Jinja pipeline
- Add safe defaults and local fact for is_ceph_first_node variable
- Use explicit monitor count for quorum validation
- Improve OSD creation with ceph-volume probe and NVMe path handling
- Make CEPH pool configuration truly idempotent
- Update mise dependencies to latest versions
- Remove cosign dependency from mise configuration
- Address CodeRabbit code quality findings
- *(docs)* Correct Jinja2 pipeline in CEPH automation pattern
- *(skills)* Improve error handling and fix CEPH automation pattern

### 🚜 Refactor

- *(validate-script)* Improve validation robustness and flexibility
- *(netbox)* Improve error handling in IPAM query tool
- *(netbox)* Improve error handling in VM creation tool
- *(netbox)* [**breaking**] Migrate to new Infisical SDK with Universal Auth
- *(skills)* Synchronize netbox_ipam_query with canonical implementation

### 📚 Documentation

- Update CHANGELOG for v0.5.0 release
- Create placeholder files for all python-uv-scripts SKILL.md links
- *(skills)* Mark common-mistakes documentation as ready
- *(anti-patterns)* Update common mistakes documentation with examples
- Add Ansible design philosophy and migration plan
- *(ansible)* Address CodeRabbit feedback for design documents

### ⚙️ Miscellaneous Tasks

- Add Python cache files to gitignore
- *(devcontainer)* Add devcontainer config with mise
- *(git)* Add ignore for *.pyc
## [0.5.0] - 2025-10-20

### 🚀 Features

- *(terraform)* Add Proxmox VM provisioning with NetBox integration
- *(ansible)* Add Proxmox configuration and system management playbooks
- *(claude)* Add Claude Code meta-infrastructure and automation tools
- *(skills)* Add Proxmox Infrastructure Management skill
- *(skills)* Add NetBox PowerDNS Integration skill
- *(skills)* Add Ansible Best Practices skill
- *(skills)* Add MCP Builder and Skill Creator meta-skills

### 📚 Documentation

- Add CHANGELOG.md with skills release notes
- *(skills)* Finalize skills with validation and documentation

### ⚙️ Miscellaneous Tasks

- Add project infrastructure and development tooling
