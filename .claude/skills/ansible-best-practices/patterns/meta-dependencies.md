# Meta and Dependencies Patterns

**Sources:**
- geerlingguy.security (analyzed 2025-10-23)
- geerlingguy.github-users (analyzed 2025-10-23)

**Repositories:**
- https://github.com/geerlingguy/ansible-role-security
- https://github.com/geerlingguy/ansible-role-github-users

## Pattern Confidence Levels

Analyzed 2 geerlingguy roles: security, github-users

**Universal Patterns (Both roles identical):**

1. ✅ **galaxy_info structure** - Complete metadata for Ansible Galaxy
2. ✅ **role_name specified** - Explicit role_name for Galaxy (not derived from repo)
3. ✅ **Comprehensive platform list** - Multiple OS families and versions
4. ✅ **Galaxy tags** - 5-7 descriptive tags for discoverability
5. ✅ **MIT license** - Permissive open source license
6. ✅ **min_ansible_version** - Specify minimum Ansible version
7. ✅ **dependencies: []** - Explicit empty list when no dependencies
8. ✅ **Author and company info** - Clear authorship

**Contextual Patterns (Varies by role scope):**

1. ⚠️  **Platform versions** - security specifies version ranges, github-users uses "all"
2. ⚠️  **Tag specificity** - security: security/ssh focused, github-users: user/github focused
3. ⚠️  **Dependency count** - Both have zero, but complex roles might have dependencies

**Key Finding:** meta/main.yml is critical for Galaxy publication and role discovery. The structure is standardized, but content varies based on role purpose and supported platforms.

## Overview

This document captures metadata and dependency patterns from production-grade Ansible roles, demonstrating how to properly configure meta/main.yml for Galaxy publication and role dependency management.

## Pattern: Complete galaxy_info Structure

### Description

Define comprehensive Galaxy metadata in meta/main.yml to enable Galaxy publication, support version constraints, and improve discoverability.

### Full galaxy_info Template

**geerlingguy.security example:**

```yaml
---
dependencies: []

galaxy_info:
  role_name: security
  author: geerlingguy
  description: Security configuration for Linux servers.
  company: "Midwestern Mac, LLC"
  license: "license (BSD, MIT)"
  min_ansible_version: '2.10'
  platforms:
    - name: EL
      versions:
        - 8
        - 9
    - name: Fedora
      versions:
        - all
    - name: Debian
      versions:
        - bullseye
        - bookworm
    - name: Ubuntu
      versions:
        - focal
        - jammy
  galaxy_tags:
    - security
    - system
    - ssh
    - fail2ban
    - autoupdate
```

**geerlingguy.github-users example:**

```yaml
---
dependencies: []

galaxy_info:
  role_name: github-users
  author: geerlingguy
  description: Create users based on GitHub accounts.
  company: "Midwestern Mac, LLC"
  license: "license (BSD, MIT)"
  min_ansible_version: 2.10
  platforms:
    - name: GenericUNIX
      versions:
        - all
    - name: Fedora
      versions:
        - all
    - name: opensuse
      versions:
        - all
    - name: GenericBSD
      versions:
        - all
    - name: FreeBSD
      versions:
        - all
    - name: Ubuntu
      versions:
        - all
    - name: SLES
      versions:
        - all
    - name: GenericLinux
      versions:
        - all
    - name: Debian
      versions:
        - all
  galaxy_tags:
    - system
    - user
    - security
    - ssh
    - accounts
    - pubkey
    - github
```

### galaxy_info Fields

#### Required Fields

**role_name** (string):
- Short, descriptive name for Galaxy
- No ansible-role- prefix (Galaxy adds it)
- Examples: `security`, `github-users`, `docker`

**author** (string):
- GitHub username or author name
- Used for Galaxy namespace (galaxy.ansible.com/author/role)

**description** (string):
- One-sentence role description
- Clear and specific
- Used in Galaxy search results

**license** (string):
- License identifier (MIT, BSD, Apache, etc.)
- Or "license (BSD, MIT)" for dual licensing
- Must match LICENSE file in repo

**min_ansible_version** (string or number):
- Minimum Ansible version required
- Examples: `'2.10'`, `'2.12'`, `2.10`
- Quote to prevent float interpretation

**platforms** (list):
- List of supported OS families and versions
- See Platform Specification section below

**galaxy_tags** (list):
- Keywords for Galaxy search
- 5-7 tags recommended
- See Tags section below

#### Optional Fields

**company** (string):
- Author's company or project
- Not required for personal roles

**issue_tracker_url** (string):
- GitHub issues URL
- Auto-derived from repo if not specified

**github_branch** (string):
- Default branch for imports
- Defaults to repository default branch

### When to Use

- **Always** include complete galaxy_info when publishing to Galaxy
- **Always** specify role_name explicitly (don't rely on auto-detection)
- **Always** list all supported platforms (users need to know compatibility)
- Include even if not publishing to Galaxy (documents compatibility)

### Anti-pattern

- ❌ Missing galaxy_info (role can't be published to Galaxy)
- ❌ Incomplete platform list (users assume role doesn't support their OS)
- ❌ Missing min_ansible_version (compatibility issues)
- ❌ No description (poor Galaxy search results)
- ❌ Generic or vague tags (reduces discoverability)

## Pattern: Platform Specification

### Description

Define supported operating systems and versions in the platforms list. Be as specific as necessary for accurate compatibility information.

### Platform Naming

**Major OS families:**

- `EL` - Enterprise Linux (RHEL, CentOS, Rocky, AlmaLinux)
- `Fedora` - Fedora Linux
- `Debian` - Debian GNU/Linux
- `Ubuntu` - Ubuntu
- `GenericLinux` - Any Linux (platform-agnostic roles)
- `GenericUNIX` - Any UNIX/Linux (very portable roles)
- `FreeBSD` - FreeBSD
- `GenericBSD` - Any BSD variant

**Full list:** https://galaxy.ansible.com/api/v1/platforms/

### Version Specification Strategies

**Strategy 1: Specific versions (security role pattern):**

```yaml
platforms:
  - name: EL
    versions:
      - 8
      - 9
  - name: Debian
    versions:
      - bullseye
      - bookworm
  - name: Ubuntu
    versions:
      - focal
      - jammy
```

**Use when:**
- Role has been tested on specific versions
- Different versions require different handling
- You want to signal explicit support/testing

**Strategy 2: All versions (github-users pattern):**

```yaml
platforms:
  - name: GenericUNIX
    versions:
      - all
  - name: GenericLinux
    versions:
      - all
```

**Use when:**
- Role is truly platform-agnostic
- No OS-specific code or dependencies
- Works on any UNIX-like system

**Strategy 3: Mixed approach:**

```yaml
platforms:
  - name: EL
    versions:
      - 8
      - 9
  - name: Ubuntu
    versions:
      - all
  - name: Debian
    versions:
      - all
```

**Use when:**
- Some platforms tested specifically
- Others likely to work but not tested

### Platform Specification Examples

**Service management role (OS-specific):**

```yaml
platforms:
  - name: EL
    versions:
      - 8
      - 9
  - name: Debian
    versions:
      - bullseye
      - bookworm
  - name: Ubuntu
    versions:
      - focal
      - jammy
      - noble
```

**User management role (generic):**

```yaml
platforms:
  - name: GenericLinux
    versions:
      - all
```

**Proxmox-specific role:**

```yaml
platforms:
  - name: Debian
    versions:
      - bullseye
      - bookworm
```

### When to Use

- List all platforms you've tested
- Use "all" only when truly platform-agnostic
- Be specific when you know version constraints
- Include both Debian and Ubuntu separately (different package versions)
- Use GenericLinux for user/file management roles

### Anti-pattern

- ❌ Claiming "all" when role has OS-specific code
- ❌ Overly broad claims (GenericUNIX for roles that need systemd)
- ❌ Missing common platforms you support
- ❌ Listing platforms you haven't tested

## Pattern: Galaxy Tags

### Description

Use descriptive, searchable tags to improve role discoverability on Ansible Galaxy.

### Tag Guidelines

1. **5-7 tags** - Enough for discovery, not too many
2. **Specific to function** - Describe what role does
3. **Common keywords** - Use terms users search for
4. **No redundancy** - Don't repeat words from role name
5. **Lowercase** - All tags lowercase

### Tag Categories

**System category tags:**
- `system` - System configuration
- `security` - Security hardening
- `networking` - Network configuration
- `database` - Database management
- `web` - Web server management

**Function category tags:**
- `user` - User management
- `account` - Account management
- `ssh` - SSH configuration
- `firewall` - Firewall rules
- `monitoring` - Monitoring/metrics

**Technology tags:**
- `docker` - Docker-related
- `kubernetes` - K8s-related
- `nginx` - Nginx web server
- `mysql` - MySQL database
- `proxmox` - Proxmox virtualization

**Action tags:**
- `installation` - Installs software
- `configuration` - Configures systems
- `deployment` - Deploys applications
- `hardening` - Security hardening

### Tag Examples

**geerlingguy.security tags:**

```yaml
galaxy_tags:
  - security
  - system
  - ssh
  - fail2ban
  - autoupdate
```

**Explanation:**
- `security` - Primary category
- `system` - System-level role
- `ssh` - SSH hardening feature
- `fail2ban` - Intrusion prevention feature
- `autoupdate` - Auto-update feature

**geerlingguy.github-users tags:**

```yaml
galaxy_tags:
  - system
  - user
  - security
  - ssh
  - accounts
  - pubkey
  - github
```

**Explanation:**
- `system` - System-level role
- `user` - User management
- `security` - SSH key security
- `ssh` - SSH access
- `accounts` - Account management
- `pubkey` - Public key management
- `github` - GitHub integration

### Tag Selection Strategy

1. **Start with primary category** - What domain? (system, security, networking)
2. **Add functional tags** - What does it do? (user, ssh, firewall)
3. **Add technology tags** - What tech? (nginx, docker, mysql)
4. **Add feature tags** - Key features? (fail2ban, autoupdate)
5. **Review search terms** - Would users search for these?

### When to Use

- Always add tags when publishing to Galaxy
- Think about user search terms
- Include role category and key features
- Don't exceed 7-8 tags (diminishing returns)

### Anti-pattern

- ❌ Too many tags (spam-like, reduces quality signal)
- ❌ Too few tags (poor discoverability)
- ❌ Generic tags only ("ansible", "role", "configuration")
- ❌ Redundant tags (role name + tags repeat same words)
- ❌ Misleading tags (tagging "docker" when role doesn't use Docker)

## Pattern: Role Dependencies

### Description

Define role dependencies in meta/main.yml when your role requires another role to function.

### Dependency Structure

**No dependencies (common):**

```yaml
---
dependencies: []
```

**With dependencies:**

```yaml
---
dependencies:
  - role: geerlingguy.repo-epel
    when: ansible_os_family == 'RedHat'
  - role: geerlingguy.firewall
```

### Dependency Specification

**Simple dependency:**

```yaml
dependencies:
  - role: namespace.rolename
```

**Conditional dependency:**

```yaml
dependencies:
  - role: geerlingguy.repo-epel
    when: ansible_os_family == 'RedHat'
```

**Dependency with variables:**

```yaml
dependencies:
  - role: geerlingguy.firewall
    vars:
      firewall_allowed_tcp_ports:
        - 22
        - 80
        - 443
```

### Dependency Behavior

1. **Dependencies run first** - Before role tasks
2. **Dependencies run once** - Even if multiple roles depend on same role
3. **Recursive dependencies** - Dependencies' dependencies also run
4. **Conditional dependencies** - Use `when:` for optional dependencies

### When to Use Dependencies

**Good use cases:**
- Required repository setup (EPEL for RedHat packages)
- Prerequisite software (Python, build tools)
- Common configuration (firewall rules before service)
- Shared components (common user accounts)

**Avoid dependencies for:**
- Optional features (use variables instead)
- Tightly coupling roles (reduces reusability)
- What playbooks should orchestrate (role order)

### Dependency vs Playbook Orchestration

**Use role dependency:**

```yaml
# meta/main.yml
dependencies:
  - role: geerlingguy.repo-epel
    when: ansible_os_family == 'RedHat'
```

**Use playbook orchestration:**

```yaml
# playbook.yml
- hosts: all
  roles:
    - geerlingguy.firewall
    - geerlingguy.security  # Assumes firewall is configured
```

**Decision matrix:**

| Scenario | Use Dependency? | Use Playbook? |
|----------|----------------|---------------|
| Role can't function without another role | ✅ Yes | ❌ No |
| Role order matters but roles are independent | ❌ No | ✅ Yes |
| Optional integration with another role | ❌ No | ✅ Yes |
| Shared prerequisite software | ✅ Yes | ❌ No |

### When to Use

- Role absolutely requires another role
- Prerequisite is always needed
- Dependency doesn't reduce role reusability
- Conditional dependencies (when: clause)

### Anti-pattern

- ❌ Too many dependencies (reduces role portability)
- ❌ Dependencies for orchestration (use playbooks)
- ❌ Circular dependencies (role A depends on B, B depends on A)
- ❌ Dependencies that should be playbook-level (nginx + database)

## Pattern: Explicit Empty Dependencies

### Description

Always include `dependencies: []` even when role has no dependencies. This makes intent explicit.

### Pattern from both roles

```yaml
---
dependencies: []

galaxy_info:
  role_name: security
  # ... rest of galaxy_info
```

### Why Explicit Empty List?

1. **Clarity** - Reader knows dependencies were considered
2. **Required by Galaxy** - Some Galaxy versions require this field
3. **Future-proof** - Easy to add dependencies later
4. **Standard format** - Consistent with roles that have dependencies

### When to Use

- Always include dependencies field
- Use empty list `[]` when no dependencies
- Place before galaxy_info for consistency

### Anti-pattern

- ❌ Omitting dependencies field entirely
- ❌ Using `dependencies: null` (use `[]`)
- ❌ Using `dependencies: ""` (use `[]`)

## Pattern: Minimum Ansible Version

### Description

Specify minimum Ansible version to prevent compatibility issues.

### Version Specification

**String format (recommended):**

```yaml
min_ansible_version: '2.10'
```

**Number format (works but avoid):**

```yaml
min_ansible_version: 2.10
```

### Version Selection Guidelines

**Conservative (oldest supported):**

```yaml
min_ansible_version: '2.10'  # Ansible 2.10+ (Oct 2020)
```

**Modern (recent features):**

```yaml
min_ansible_version: '2.12'  # Ansible 2.12+ (Nov 2021)
```

**Latest (cutting edge):**

```yaml
min_ansible_version: '2.15'  # Ansible 2.15+ (May 2023)
```

### Version Decision Factors

1. **Module requirements** - Modules you use
2. **Feature requirements** - Ansible features needed
3. **User base** - What versions do users have?
4. **Collection compatibility** - Collection requirements

### Common Version Breakpoints

- **2.10** - Collections architecture, ansible-base
- **2.11** - Multiple enhancements to modules
- **2.12** - Improved error messages, new modules
- **2.13** - Plugin improvements
- **2.14** - Enhanced fact gathering
- **2.15** - Modern Ansible (May 2023)

### When to Use

- Set to oldest Ansible version you've tested
- Test role against min_ansible_version
- Update min version when using newer features
- Document why specific version is needed

### Anti-pattern

- ❌ Setting min version too high (excludes users unnecessarily)
- ❌ Setting min version too low (users hit compatibility issues)
- ❌ Not testing against min version
- ❌ Using float (2.10 becomes 2.1) - always quote

## Comparison to Virgo-Core Roles

### system_user Role

**meta/main.yml Analysis:**

```yaml
---
dependencies: []

galaxy_info:
  role_name: system_user
  author: basher8383
  description: Manage Linux system users with SSH keys and sudo access
  license: MIT
  min_ansible_version: '2.10'
  platforms:
    - name: Debian
      versions:
        - bullseye
        - bookworm
    - name: Ubuntu
      versions:
        - focal
        - jammy
  galaxy_tags:
    - system
    - user
    - ssh
    - sudo
    - security
```

**Assessment:**

- ✅ Complete galaxy_info structure
- ✅ Explicit role_name
- ✅ Clear description
- ✅ Appropriate platforms (Debian/Ubuntu)
- ✅ Good galaxy_tags (5 tags)
- ✅ Empty dependencies list
- ✅ Quoted min_ansible_version
- ⚠️  Could add more platforms if tested (RHEL family)

**Pattern Match:** 95% - Excellent meta configuration

### proxmox_access Role

**meta/main.yml Analysis:**

```yaml
---
dependencies: []

galaxy_info:
  role_name: proxmox_access
  author: basher8383
  description: Manage Proxmox VE access control (roles, users, groups, tokens, ACLs)
  license: MIT
  min_ansible_version: '2.10'
  platforms:
    - name: Debian
      versions:
        - bullseye
        - bookworm
  galaxy_tags:
    - system
    - proxmox
    - virtualization
    - access-control
    - security
```

**Assessment:**

- ✅ Complete galaxy_info structure
- ✅ Excellent description (specific features)
- ✅ Correct platforms (Proxmox runs on Debian)
- ✅ Appropriate tags
- ✅ Hyphenated tag (access-control) is fine
- ✅ No dependencies (correct for this role)

**Pattern Match:** 100% - Perfect meta configuration

### proxmox_network Role

**meta/main.yml Analysis:**

```yaml
---
dependencies: []

galaxy_info:
  role_name: proxmox_network
  author: basher8383
  description: Configure Proxmox VE network infrastructure (bridges, VLANs, MTU)
  license: MIT
  min_ansible_version: '2.10'
  platforms:
    - name: Debian
      versions:
        - bullseye
        - bookworm
  galaxy_tags:
    - system
    - proxmox
    - networking
    - virtualization
    - infrastructure
```

**Assessment:**

- ✅ Complete galaxy_info structure
- ✅ Descriptive with feature list
- ✅ Correct platforms
- ✅ Good tags (networking, infrastructure)
- ✅ No dependencies (appropriate)

**Pattern Match:** 100% - Perfect meta configuration

## Summary

**Universal Meta Patterns:**

1. Complete galaxy_info in all roles
2. Explicit role_name (don't rely on auto-detection)
3. Clear, one-sentence description
4. Comprehensive platform list with version specificity
5. 5-7 descriptive galaxy_tags
6. Quoted min_ansible_version ('2.10')
7. Explicit `dependencies: []` when no dependencies
8. MIT or permissive license
9. Author and company information

**Key Takeaways:**

- meta/main.yml is required for Galaxy publication
- Platform specificity signals tested compatibility
- Tags are critical for role discoverability
- Dependencies should be rare and truly required
- Explicit empty dependencies is better than omitting field
- Quote min_ansible_version to prevent float issues
- Description and tags are user-facing (make them good)

**Virgo-Core Assessment:**

All three Virgo-Core roles have excellent meta/main.yml configuration:
- Complete galaxy_info structure
- Appropriate platform specifications
- Good tag selection
- No unnecessary dependencies
- Ready for Galaxy publication

No meta-related gaps identified. Roles follow best practices.

**Next Steps:**

1. Consider testing roles on RHEL/Rocky if applicable (expand platform list)
2. Maintain this quality in future roles
3. Update min_ansible_version if newer features are used
4. Review tags periodically (search terms change)
5. Document Galaxy publication process
