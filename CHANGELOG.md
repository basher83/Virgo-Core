## [0.7.0] - 2025-11-12

### 🚀 Features

- *(ansible)* Complete Phase 1 migration - system_user role
- *(config)* Add markdownlint-cli2 integration with directory exclusions
- *(editorconfig)* Enhance configuration with additional file types and settings
- *(ansible)* Phase 2 Migration - proxmox_access Role (#14)
- *(conductor)* Add Conductor workspace configuration (#17)
- *(ansible)* Phase 3 Migration - proxmox_network Role (#15)
- *(ansible)* Complete Phase 4 - Production-Ready Proxmox Cluster Automation (#16)
- *(ansible)* Add production inventory and group_vars configuration
- *(skills)* Enhance ansible-best-practices with comprehensive patterns

### 🐛 Bug Fixes

- *(ansible)* Prevent shell injection in sudo verification command
- *(ansible)* Apply proxmox_network role fixes and complete cleanup

### 📚 Documentation

- *(ansible)* Clarify security requirements and verification behavior
- *(skills)* Add production repository research plan
- *(skills)* Enhance skills planning documentation with structured improvements
- *(ansible)* Add comprehensive testing validation results
- Add comprehensive infrastructure specification
- Update project documentation for testing completion

### ⚙️ Miscellaneous Tasks

- *(fix)* Adjust pre-commit to remove mise tf fmt, fix spacing on markdown file
- *(docs)* Add claude slash cmd
- Add testing scripts directory
- *(claude)* Remove deprecated skills and commands
- *(ansible)* Move deprecated playbooks to .deprecated directory
## [0.6.0] - 2025-10-22

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
- *(changelog)* Update CHANGELOG.md for unreleased changes
- *(release)* Prepare v0.6.0 release
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
