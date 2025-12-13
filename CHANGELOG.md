## [unreleased]

### 🚀 Features

- *(docs)* Add Mintlify documentation configuration and assets
- *(ansible)* Add proxmox_tuning role for system optimization
- *(ansible)* Add subscription banner removal to proxmox_repository
- *(ansible)* Add CEPH-aware rolling system upgrade
- *(ansible)* Add TCP BBR congestion control to proxmox_tuning
- *(ansible)* Add KSM tuning to proxmox_tuning role
- *(ansible)* Add pigz backup acceleration to proxmox_repository
- *(ansible)* Add kexec fast reboot to proxmox_tuning role
- *(ansible)* Add haveged entropy daemon to proxmox_tuning role
- *(ansible)* Add network stack optimization to proxmox_tuning role
- Add comprehensive .github/copilot-instructions.md
- *(ansible)* Add proxmox_template role for VM template creation
- *(ansible)* Add ansible-workflows plugin with 8 skills, 4 commands, 4 agents

### 🐛 Bug Fixes

- *(mintlify)* Convert relative .md links to root-relative paths
- *(mintlify)* Remove leading slash from internal link paths
- *(ansible)* Make subscription banner removal idempotent
- *(ansible)* Address PR review feedback for proxmox_template role
- *(ansible)* Remove hardcoded paths from commands and agents
- *(ansible)* Use CLAUDE_PLUGIN_ROOT for script references
- *(ansible)* Correct hooks.json structure for Claude Code
- *(ansible)* Restore correct hooks.json wrapper structure

### 🚜 Refactor

- Move archive and brainstorming folders to docs/
- *(ansible)* Remove monolithic ansible-best-practices skill
- *(ansible)* Move references to skill-level directories

### 📚 Documentation

- Apply markdown formatting fixes across documentation
- Apply formatting fixes and finalize linting scope
- Fix Mintlify site issues and split philosophy doc
- *(research)* Add PowerDNS Ansible and setup research
- *(research)* Add NetBox PowerDNS integration research
- *(plans)* Add IPAM/DNS stack design document
- *(research)* Add PowerDNS Ansible GitHub research report
- *(mintlify)* Add frontmatter to all documentation pages
- Move documentation files to documentation/ directory
- Add proxmox_tuning role design document
- Add ProxMenux integration research tracking
- Deprioritize Fail2Ban for internal infrastructure
- *(ansible)* Update role READMEs and ProxMenux integration tracking
- Update changelog
- Add infrastructure diagrams and architecture decision records
- Remove DNS error warning from copilot instructions
- Update changelog
- *(ansible)* Add community.proxmox collection reference
- *(ansible)* Add Additional Resources sections to skills
- Update changelog

### 🎨 Styling

- *(ansible)* Use failed_when instead of ignore_errors
- *(ansible)* Remove second-person voice from skill files
- *(ansible)* Convert prescriptive language to imperative form in skills

### ⚙️ Miscellaneous Tasks

- Update linting configuration
- Migrate markdown linter from markdownlint-cli2 to rumdl
- *(claude)* Update agents and commands markdown formatting
- *(claude)* Fix research reports markdown formatting
- *(claude)* Fix scoring system markdown formatting
- *(claude)* Fix Ansible skills markdown formatting
- Expand rumdl exclude patterns for documentation
- *(agents)* Replace meta-agent with jina-search agent
- *(mise)* Remove markdownlint-cli2 from tool list
- *(github)* Add validate workflow for PR checks
- Add new hooks
- *(hookify)* Disable skill-forced-eval hook and update structure
- *(rumdl)* Update markdown linter configuration

## [1.1.0] - 2025-11-20

### 🚀 Features

- *(docs)* Add Mintlify documentation site configuration
- *(docs)* Add Mintlify documentation homepage

### 🐛 Bug Fixes

- *(docs)* Update Mintlify theme to valid value 'prism'
- *(docs)* Use correct Mintlify schema and restore linden theme
- *(docs)* Rename mint.json to docs.json for Mintlify compatibility
- *(docs)* Update navigation paths to match subdirectory structure
- *(docs)* Fix Quick Start section paths

### 🚜 Refactor

- *(docs)* Move docs/ to documentation/ for Mintlify integration
- *(docs)* Restructure docs.json to match official Mintlify schema
- *(docs)* Reorganize documentation into logical hierarchy
- *(ansible)* Reorganize inventory with group_vars and node_id templating

### 📚 Documentation

- *(goals)* Mark all core infrastructure goals as complete for v1.0.0
- Update next-features doc with inventory completion status
- Add documentation enhancement design
- Add comprehensive implementation plan
- Add battle-tested metrics to ansible-philosophy
- Update homepage Quick Links section
- Create getting-started directory structure
- Add comprehensive prerequisites checklist
- Add development environment installation guide
- Add first-deployment tutorial (part 1)
- Add first-deployment Phase 2 (network setup)
- Complete first-deployment tutorial (phases 3-5)
- Add getting-started pages to navigation
- Create roles directory for Phase 3
- Add enhanced system_user role documentation
- Add Ansible Roles navigation group
- Add enhanced proxmox_access role documentation
- Add enhanced proxmox_network role documentation
- Add enhanced proxmox_repository role documentation
- Add enhanced proxmox_cluster role documentation
- Add enhanced proxmox_ceph role documentation
- Add implementation completion summary

### ⚙️ Miscellaneous Tasks

- *(changelog)* Fix git-cliff template for markdownlint compliance
- *(release)* Update changelog for v1.1.0

## [1.0.0] - 2025-11-18

### 🚀 Features

- *(commands)* Add verify-claims slash command
- *(ansible-best-practices)* Add production patterns from geerlingguy role analysis (#18)
- *(ansible)* Phase 5 testing - fix check mode compatibility and create test infrastructure
- *(ansible)* Phase 5 testing continuation - fix proxmox_ceph and cluster init playbook
- *(ansible)* Phase 5 complete - enable proxmox_network and document all 6 roles tested
- *(mise)* Add Ansible playbook tasks for cluster automation

### 🐛 Bug Fixes

- *(ansible)* 10 critical execution bugs discovered via idempotency testing
- *(ansible)* Fix CEPH bootstrap keyring and implement ceph-volume for multiple OSDs per device
- *(ansible)* Bug #12 - Fix broken OSD counting and non-idempotent zap
- *(ansible)* Critical idempotency bugs in OSD zap and cluster quorum checks
- *(ansible)* Bug #15 - Add bootstrap keyring distribution for CEPH OSD creation
- *(pre-commit)* Configure markdownlint to only check staged files

### 📚 Documentation

- Add PR #21 after-action review
- Improve markdown formatting in verify-pr command
- Improve formatting and add quote to PR21 AAR
- *(proxmox_ceph)* Document Bug #13 and #14 idempotency fixes
- *(testing)* Add Test 6 idempotency validation results
- *(ansible)* Complete Phase 6 cleanup - READMEs, migration plan, completion summary
- Rewrite root README with comprehensive project documentation
- *(ansible,terraform)* Add comprehensive READMEs for both directories
- *(ansible)* Mark mise tasks complete in migration plan
- *(references)* Fix typo and expand bibliography from 6 to 89 lines
- *(terraform)* Add comprehensive template creation guide
- *(scripts)* Add comprehensive utility scripts reference
- *(terraform)* Add terraform-docs auto-generated sections to READMEs
- *(documentation)* Add comprehensive documentation index
- *(claude)* Add multi-agent orchestration patterns and learnings
- *(changelog)* Update changelog for v0.8.0

### ⚙️ Miscellaneous Tasks

- *(docs)* Archive old 2025-10-23 research documents
- *(lint)* Allow terraform-docs HTML elements and disable bare URL check

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
