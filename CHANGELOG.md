## [0.6.0] - 2025-10-22

### 🚀 Features

-   _(skills)_ Major enhancement to Claude Code skills with 10,000+ lines of automation content
-   _(skills)_ Complete Tier 1 improvements for skill library
-   _(terraform)_ Add comprehensive OpenTofu deployment examples

### 🐛 Bug Fixes

-   Resolve 18 CodeRabbit issues across documentation, code quality, and security
-   _(security)_ Resolve command injection vulnerabilities and improve validation
-   Use correct negative index syntax for last CLI argument
-   Mark validation invalid when shebang missing in strict mode
-   Add UTF-8 encoding and UnicodeDecodeError handling to file reading
-   Improve metadata block extraction for cross-platform compatibility
-   Correct example link to check_cluster_health_enhanced.py
-   Correct relative link path to ansible-best-practices
-   Add default fallback to all cluster_group variable references
-   Fix CEPH manager list to use proper list membership test
-   Use strict majority for CEPH monitor quorum check
-   Add exit code to JSON output path in check_ceph_health.py
-   Add timeout and improve error handling in check_ceph_health.py
-   Add rollback on IP creation failure and remove unnecessary f-strings
-   Harden get_netbox_client with specific exception handling
-   Materialize pynetbox iterators once to avoid re-fetching
-   Improve CEPH OSD count validation with robust Jinja pipeline
-   Add safe defaults and local fact for is_ceph_first_node variable
-   Use explicit monitor count for quorum validation
-   Improve OSD creation with ceph-volume probe and NVMe path handling
-   Make CEPH pool configuration truly idempotent
-   Update mise dependencies to latest versions
-   Remove cosign dependency from mise configuration
-   Address CodeRabbit code quality findings
-   _(docs)_ Correct Jinja2 pipeline in CEPH automation pattern
-   _(skills)_ Improve error handling and fix CEPH automation pattern

### 🚜 Refactor

-   _(validate-script)_ Improve validation robustness and flexibility
-   _(netbox)_ Improve error handling in IPAM query tool
-   _(netbox)_ Improve error handling in VM creation tool
-   _(netbox)_ [**breaking**] Migrate to new Infisical SDK with Universal Auth
-   _(skills)_ Synchronize netbox_ipam_query with canonical implementation

### 📚 Documentation

-   Update CHANGELOG for v0.5.0 release
-   Create placeholder files for all python-uv-scripts SKILL.md links
-   _(skills)_ Mark common-mistakes documentation as ready
-   _(anti-patterns)_ Update common mistakes documentation with examples
-   Add Ansible design philosophy and migration plan
-   _(ansible)_ Address CodeRabbit feedback for design documents

### ⚙️ Miscellaneous Tasks

-   Add Python cache files to gitignore
-   _(devcontainer)_ Add devcontainer config with mise
-   _(git)_ Add ignore for \*.pyc

## [0.5.0] - 2025-10-20

### 🚀 Features

-   _(terraform)_ Add Proxmox VM provisioning with NetBox integration
-   _(ansible)_ Add Proxmox configuration and system management playbooks
-   _(claude)_ Add Claude Code meta-infrastructure and automation tools
-   _(skills)_ Add Proxmox Infrastructure Management skill
-   _(skills)_ Add NetBox PowerDNS Integration skill
-   _(skills)_ Add Ansible Best Practices skill
-   _(skills)_ Add MCP Builder and Skill Creator meta-skills

### 📚 Documentation

-   Add CHANGELOG.md with skills release notes
-   _(skills)_ Finalize skills with validation and documentation

### ⚙️ Miscellaneous Tasks

-   Add project infrastructure and development tooling
