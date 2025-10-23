# Role Structure Standards

**Sources:**
- geerlingguy.security (analyzed 2025-10-23)
- geerlingguy.github-users (analyzed 2025-10-23)

**Repositories:**
- https://github.com/geerlingguy/ansible-role-security
- https://github.com/geerlingguy/ansible-role-github-users

## Pattern Confidence Levels

Analyzed 2 geerlingguy roles: security, github-users

**Universal Patterns (Both roles use identical approach):**

1. ✅ **Standard directory structure** - Both follow defaults/, tasks/, meta/, molecule/, .github/ structure
2. ✅ **Role-prefixed variable names** - security_*, github_users_* (prevents conflicts)
3. ✅ **Descriptive task names** - Action verb + object pattern ("Ensure...", "Add...", "Update...")
4. ✅ **defaults/ for user configuration** - All user-overridable values in defaults/main.yml
5. ✅ **Snake_case naming** - Consistent variable naming convention
6. ✅ **Inline validation** - validate parameter for critical config files
7. ✅ **File permissions** - Explicit mode settings on all files
8. ✅ **Quality control files** - .ansible-lint, .yamllint, .gitignore present

**Contextual Patterns (Varies by role complexity):**

1. ⚠️  **Task file organization** - security splits tasks (ssh.yml, fail2ban.yml), github-users keeps single main.yml (role is simpler)
2. ⚠️  **vars/ directory** - security has OS-specific vars files, github-users doesn't need them
3. ⚠️  **templates/ usage** - security uses templates for fail2ban config, github-users has no templates
4. ⚠️  **handlers/** - security has 3 handlers (services to restart), github-users has none (no services managed)
5. ⚠️  **Conditional task execution** - security uses OS-family conditionals, github-users is OS-agnostic

**Key Finding:** Simple roles (like github-users) can keep all tasks in main.yml. Complex roles (like security) should split into feature-based files when tasks exceed ~30-40 lines.

## Overview

This document captures role structure and organization patterns from production-grade Ansible roles, demonstrating how to organize tasks, variables, handlers, and templates for maintainability and clarity.

## Directory Organization

### Pattern: Standard Ansible Role Structure

**Description:** Follow the standard Ansible role directory structure for consistency and Galaxy compatibility.

**Directory Tree:**

```
ansible-role-security/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── release.yml
│       └── stale.yml
├── defaults/
│   └── main.yml
├── handlers/
│   └── main.yml
├── meta/
│   └── main.yml
├── molecule/
│   └── default/
│       ├── converge.yml
│       └── molecule.yml
├── tasks/
│   ├── main.yml
│   ├── ssh.yml
│   ├── fail2ban.yml
│   ├── autoupdate-RedHat.yml
│   └── autoupdate-Debian.yml
├── templates/
│   └── jail.local.j2
├── vars/
│   ├── Debian.yml
│   └── RedHat.yml
├── .ansible-lint
├── .gitignore
├── .yamllint
├── LICENSE
└── README.md
```

**Directory Purposes:**

- **defaults/** - User-overridable default values (lowest precedence)
- **vars/** - OS-specific or internal variables (high precedence)
- **tasks/** - Ansible tasks organized into logical files
- **handlers/** - Event-triggered tasks (service restarts, reloads)
- **templates/** - Jinja2 templates for configuration files
- **meta/** - Role metadata (Galaxy info, dependencies)
- **molecule/** - Testing scenarios and configurations
- **.github/workflows/** - CI/CD automation
- **files/** - Static files (not used in this role, but common)

**When to Use:**

- Always create this base structure for new roles
- Omit directories you don't need (files/, templates/ if unused)
- Add molecule/ for all production roles
- Include .github/workflows/ for open source or team roles

**Anti-pattern:**

- Don't create directories you won't use (empty dirs confuse users)
- Avoid non-standard directory names
- Don't mix role content with playbooks in same directory

## Task Organization

### Pattern: Main Task File as Router

**Description:** Use tasks/main.yml as a routing file that includes other task files based on conditions. This keeps the main file simple and delegates work to focused task files.

**File Path:** `tasks/main.yml`

**Example Code:**

```yaml
---
- name: Include OS-specific variables.
  include_vars: "{{ ansible_os_family }}.yml"

# Fail2Ban
- include_tasks: fail2ban.yml
  when: security_fail2ban_enabled | bool

# SSH
- include_tasks: ssh.yml

# Autoupdate
- include_tasks: autoupdate-RedHat.yml
  when:
    - ansible_os_family == 'RedHat'
    - security_autoupdate_enabled | bool

- include_tasks: autoupdate-Debian.yml
  when:
    - ansible_os_family == 'Debian'
    - security_autoupdate_enabled | bool
```

**Key Elements:**

1. **include_vars at top** - Load OS-specific variables first
2. **Logical grouping** - Each include_tasks represents a feature
3. **Conditional includes** - Only run tasks when needed
4. **Comments as section headers** - Improve readability
5. **Boolean filter** - `| bool` ensures proper boolean evaluation
6. **Multi-line conditions** - Use list format for multiple when clauses

**Task File Organization Strategy:**

- **Feature-based:** ssh.yml, fail2ban.yml (grouped by functionality)
- **OS-specific:** autoupdate-RedHat.yml, autoupdate-Debian.yml (split by platform)

**When to Use:**

- Split tasks into separate files when >30-40 lines
- Create OS-specific task files for platform differences
- Use conditional includes for optional features
- Keep main.yml under 50 lines as a routing file

**Anti-pattern:**

- Don't put all tasks in main.yml (hard to maintain)
- Avoid deep nesting of include_tasks (max 2 levels)
- Don't split too granularly (each file should have 10+ lines)

### Pattern: Feature-Specific Task Files

**Description:** Create focused task files for specific features, with clear names that describe their purpose.

**File Path:** `tasks/ssh.yml`

**Example Code:**

```yaml
---
- name: Ensure SSH daemon is running.
  service:
    name: "{{ security_sshd_name }}"
    state: "{{ security_sshd_state }}"

- name: Update SSH configuration to be more secure.
  lineinfile:
    dest: "{{ security_ssh_config_path }}"
    regexp: "{{ item.regexp }}"
    line: "{{ item.line }}"
    state: present
    validate: 'sshd -T -f %s'
    mode: 0644
  with_items:
    - regexp: "^PasswordAuthentication"
      line: "PasswordAuthentication {{ security_ssh_password_authentication }}"
    - regexp: "^PermitRootLogin"
      line: "PermitRootLogin {{ security_ssh_permit_root_login }}"
    - regexp: "^Port"
      line: "Port {{ security_ssh_port }}"
    - regexp: "^UseDNS"
      line: "UseDNS {{ security_ssh_usedns }}"
    - regexp: "^PermitEmptyPasswords"
      line: "PermitEmptyPasswords {{ security_ssh_permit_empty_password }}"
    - regexp: "^ChallengeResponseAuthentication"
      line: "ChallengeResponseAuthentication {{ security_ssh_challenge_response_auth }}"
    - regexp: "^GSSAPIAuthentication"
      line: "GSSAPIAuthentication {{ security_ssh_gss_api_authentication }}"
    - regexp: "^X11Forwarding"
      line: "X11Forwarding {{ security_ssh_x11_forwarding }}"
  notify:
    - reload systemd
    - restart ssh

- name: Add configured users allowed to connect over ssh
  lineinfile:
    dest: "{{ security_ssh_config_path }}"
    regexp: '^AllowUsers'
    line: "AllowUsers {{ security_ssh_allowed_users | join(' ') }}"
    state: present
    create: true
    validate: 'sshd -T -f %s'
    mode: 0644
  when: security_ssh_allowed_users | length > 0
  notify: restart ssh

- name: Add configured user accounts to passwordless sudoers.
  lineinfile:
    dest: /etc/sudoers
    regexp: '^{{ item }}'
    line: '{{ item }} ALL=(ALL) NOPASSWD: ALL'
    state: present
    validate: 'visudo -cf %s'
    mode: 0440
  with_items: "{{ security_sudoers_passwordless }}"
  when: security_sudoers_passwordless | length > 0
```

**Key Patterns:**

1. **Validation parameters:**
   - `validate: 'sshd -T -f %s'` - Test SSH config before applying
   - `validate: 'visudo -cf %s'` - Validate sudoers syntax
   - Prevents breaking critical system files

2. **Idempotent configuration:**
   - lineinfile with regexp - Updates or adds lines
   - state: present - Ensures line exists
   - Anchored regexps (^) - Match start of line

3. **Conditional execution:**
   - `when: security_ssh_allowed_users | length > 0` - Skip if empty list
   - Prevents unnecessary file modifications

4. **Handler notifications:**
   - `notify: restart ssh` - Trigger service restart on changes
   - Multiple handlers can be notified
   - Handlers run once at end, even if notified multiple times

5. **File permissions:**
   - `mode: 0644` for SSH config (readable by all)
   - `mode: 0440` for sudoers (read-only, no world access)

**When to Use:**

- Always validate critical config files (SSH, sudoers, etc.)
- Use lineinfile for simple config changes
- Notify handlers instead of inline service restarts
- Set explicit file permissions on security-sensitive files
- Use conditional execution to skip unnecessary tasks

**Anti-pattern:**

- Don't modify critical files without validation
- Avoid command/shell when modules exist (lineinfile vs sed)
- Don't restart services directly in tasks (use handlers)
- Avoid hardcoded paths (use variables for OS differences)

## Naming Conventions

### Pattern: Descriptive Variable Names with Role Prefix

**Description:** Prefix all role variables with the role name to avoid conflicts with other roles or playbook variables.

**File Path:** `defaults/main.yml`

**Example Code:**

```yaml
---
security_ssh_port: 22
security_ssh_password_authentication: "no"
security_ssh_permit_root_login: "no"
security_ssh_usedns: "no"
security_ssh_permit_empty_password: "no"
security_ssh_challenge_response_auth: "no"
security_ssh_gss_api_authentication: "no"
security_ssh_x11_forwarding: "no"
security_sshd_state: started
security_ssh_restart_handler_state: restarted
security_ssh_allowed_users: []
security_ssh_allowed_groups: []

security_sudoers_passwordless: []
security_sudoers_passworded: []

security_autoupdate_enabled: true
security_autoupdate_blacklist: []
security_autoupdate_additional_origins: []

security_autoupdate_reboot: "false"
security_autoupdate_reboot_time: "03:00"
security_autoupdate_mail_to: ""
security_autoupdate_mail_on_error: true

security_fail2ban_enabled: true
security_fail2ban_custom_configuration_template: "jail.local.j2"
```

**Naming Pattern:**

```
{role_name}_{feature}_{attribute}
```

Examples:
- `security_ssh_port` - Role: security, Feature: ssh, Attribute: port
- `security_fail2ban_enabled` - Role: security, Feature: fail2ban, Attribute: enabled
- `security_autoupdate_reboot_time` - Role: security, Feature: autoupdate, Attribute: reboot_time

**Key Elements:**

1. **Role prefix** - All variables start with "security_"
2. **Feature grouping** - Related variables have common prefix (security_ssh_, security_fail2ban_)
3. **Descriptive names** - Full words, not abbreviations
4. **Underscore separation** - snake_case, not camelCase
5. **Boolean as strings** - "yes"/"no" for SSH config (preserves YAML booleans elsewhere)

**When to Use:**

- Always prefix variables with role name
- Group related variables with feature prefix
- Use descriptive names (avoid abbreviations)
- Choose meaningful defaults
- Quote string values that look like booleans ("yes", "no", "true", "false")

**Anti-pattern:**

- Don't use generic variable names (port, enabled, config_path)
- Avoid abbreviations (ssh_cfg instead of ssh_config)
- Don't mix naming styles (snake_case vs camelCase)
- Avoid unquoted yes/no/true/false strings (YAML interprets as booleans)

### Pattern: Task Naming Convention

**Description:** Write task names that are descriptive, actionable, and follow a consistent format.

**Task Name Pattern:**

```
[Action verb] [object] [additional context]
```

Examples from the role:

- "Ensure SSH daemon is running" - State verification
- "Update SSH configuration to be more secure" - Modification action
- "Add configured users allowed to connect over ssh" - Addition action
- "Install fail2ban" - Installation action

**Guidelines:**

1. **Start with action verb** - Ensure, Update, Add, Install, Configure, Remove
2. **Be specific** - "SSH daemon" not just "daemon"
3. **Add context** - "to be more secure" explains why
4. **Use present tense** - "Ensure" not "Ensuring"
5. **Capitalize first word** - "Ensure SSH..." not "ensure ssh..."

**When to Use:**

- Every task should have a clear name
- Name describes the desired state, not the implementation
- Use consistent verbs across the role

**Anti-pattern:**

- Don't use vague names ("Configure SSH", "Setup system")
- Avoid implementation details ("Run lineinfile on sshd_config")
- Don't use all caps or weird capitalization

## File Placement Decisions

### Pattern: defaults/ vs vars/ Usage

**Description:** Use defaults/ for user-overridable values and vars/ for internal/OS-specific values.

**File Paths:**

- `defaults/main.yml` - User-facing configuration
- `vars/Debian.yml` - Debian-specific internal values
- `vars/RedHat.yml` - RedHat-specific internal values

**defaults/main.yml Example:**

```yaml
---
# User-configurable values (low precedence)
security_ssh_port: 22
security_ssh_password_authentication: "no"
security_fail2ban_enabled: true
security_autoupdate_enabled: true
```

**vars/Debian.yml Example:**

```yaml
---
# Internal OS-specific values (high precedence)
security_ssh_config_path: /etc/ssh/sshd_config
security_sshd_name: ssh
```

**vars/RedHat.yml Example (inferred structure):**

```yaml
---
# Internal OS-specific values (high precedence)
security_ssh_config_path: /etc/ssh/sshd_config
security_sshd_name: sshd
```

**Decision Matrix:**

| Variable Type | Location | Precedence | Use Case |
|--------------|----------|------------|----------|
| User configuration | defaults/ | Low (easily overridden) | Settings users customize |
| OS-specific paths | vars/ | High (shouldn't override) | File paths, service names |
| Internal logic | vars/ | High | Values role needs to work |
| Feature toggles | defaults/ | Low | Enable/disable features |

**When to Use:**

- **defaults/** - Any value users might want to change
- **vars/** - OS-specific values, internal constants
- Load vars/ files conditionally by OS family
- Use include_vars to load appropriate vars file

**Anti-pattern:**

- Don't put user-facing config in vars/ (can't be overridden easily)
- Don't put OS-specific paths in defaults/ (users shouldn't change)
- Avoid duplicating values between defaults/ and vars/

### Pattern: OS-Specific Variable Files

**Description:** Create separate variable files for each OS family to handle platform differences.

**File Path:** `vars/Debian.yml`, `vars/RedHat.yml`

**Loading Pattern:**

```yaml
- name: Include OS-specific variables.
  include_vars: "{{ ansible_os_family }}.yml"
```

**Common OS-Specific Variables:**

- Service names (ssh vs sshd)
- Configuration file paths
- Package names
- Default directories

**When to Use:**

- Different service names across OS families
- Different file paths or package names
- OS-specific configuration options
- Load at start of tasks/main.yml

**Anti-pattern:**

- Don't use when: conditionals for every OS difference
- Avoid complex variable resolution logic
- Don't hardcode OS-specific values in tasks

## Handler Organization

### Pattern: Simple Handler Definitions

**Description:** Define handlers with clear names and simple actions. Handlers should do one thing well.

**File Path:** `handlers/main.yml`

**Example Code:**

```yaml
---
- name: reload systemd
  systemd_service:
    daemon_reload: true

- name: restart ssh
  service:
    name: "{{ security_sshd_name }}"
    state: "{{ security_ssh_restart_handler_state }}"

- name: reload fail2ban
  service:
    name: fail2ban
    state: reloaded
```

**Key Elements:**

1. **Descriptive names** - Action + service (restart ssh, reload fail2ban)
2. **Single responsibility** - Each handler does one thing
3. **Configurable state** - Uses variable for restart/reload state
4. **Lowercase names** - "reload systemd" not "Reload Systemd"
5. **Service vs systemd_service** - Use appropriate module

**Handler Naming Pattern:**

```
[action] [service/component]
```

Examples:
- "restart ssh" - Restart SSH service
- "reload systemd" - Reload systemd daemon
- "reload fail2ban" - Reload fail2ban configuration

**When to Use:**

- Create one handler per service/action combination
- Use simple, action-oriented names
- Make handler behavior configurable via variables
- Use reload instead of restart when possible (less disruptive)

**Anti-pattern:**

- Don't combine multiple actions in one handler
- Avoid complex logic in handlers
- Don't use handlers for non-idempotent actions

## Comparison to Virgo-Core Roles

### system_user Role

**Structure Analysis:**

```
system_user/
├── defaults/
│   └── main.yml ✅
├── handlers/
│   └── main.yml (empty - appropriate, no services)
├── meta/
│   └── main.yml ✅
├── tasks/
│   └── main.yml ✅ (single file appropriate for scope)
├── templates/
│   └── sudoers.j2 ✅
└── README.md ✅
```

**Matches:**

- ✅ Proper defaults/ usage
- ✅ Appropriate task organization (role is simple enough for single file)
- ✅ Variable naming with role prefix (system_user_*)
- ✅ Clear task names

**Gaps:**

- ⚠️  No vars/ directory for OS-specific values (may not be needed)
- ❌ No molecule/ testing directory
- ❌ No .github/workflows/ for CI

**Priority Actions:**

1. **Nice-to-have:** Add vars/ files if supporting multiple OS families (30 min)
2. **Critical:** Add molecule/ directory (covered in testing-comprehensive.md)

### proxmox_access Role

**Structure Analysis:**

```
proxmox_access/
├── defaults/
│   └── main.yml ✅
├── handlers/
│   └── main.yml ✅ (appropriate handlers defined)
├── meta/
│   └── main.yml ✅
├── tasks/
│   ├── main.yml ✅ (good routing pattern)
│   ├── roles.yml ✅
│   ├── groups.yml ✅
│   ├── users.yml ✅
│   ├── tokens.yml ✅
│   └── acls.yml ✅
├── templates/
│   └── terraform_env.sh.j2 ✅
└── README.md ✅
```

**Matches:**

- ✅ Excellent task organization (main.yml as router)
- ✅ Feature-based task files
- ✅ Proper variable naming (proxmox_access_*)
- ✅ Good handler usage

**Gaps:**

- ❌ No molecule/ testing directory
- ❌ No .github/workflows/ for CI
- ⚠️  No vars/ directory (but tasks include OS detection)

**Priority Actions:**

1. **Critical:** Add molecule/ directory (covered in testing-comprehensive.md)
2. **Nice-to-have:** Add vars/ files for Proxmox-specific paths (1 hour)

### proxmox_network Role

**Structure Analysis:**

```
proxmox_network/
├── defaults/
│   └── main.yml ✅
├── handlers/
│   └── main.yml ✅ (network reload handler)
├── meta/
│   └── main.yml ✅
├── tasks/
│   ├── main.yml ✅
│   ├── bridges.yml ✅
│   ├── vlans.yml ✅
│   └── verify.yml ✅ (excellent - verification tasks)
└── README.md ✅
```

**Matches:**

- ✅ Good task organization
- ✅ Verification tasks (verify.yml) - advanced pattern
- ✅ Proper handlers for network changes
- ✅ Variable naming conventions

**Gaps:**

- ❌ No molecule/ testing directory
- ❌ No .github/workflows/ for CI
- ⚠️  No templates/ directory (uses lineinfile, which is fine)

**Priority Actions:**

1. **Critical:** Add molecule/ directory with network verification (covered in testing-comprehensive.md)

## Summary

**Universal Patterns Identified:**

1. Standard Ansible role directory structure
2. tasks/main.yml as router with include_tasks
3. Feature-based task file organization
4. Role-prefixed variable names (rolename_feature_attribute)
5. defaults/ for user config, vars/ for internal/OS-specific values
6. OS-specific variable files loaded dynamically
7. Simple, single-purpose handlers
8. Descriptive task names starting with action verbs
9. Configuration file validation before applying

**Key Takeaways:**

- Directory structure is standardized and well-understood
- Task organization improves maintainability
- Naming conventions prevent variable conflicts
- Proper defaults/ vs vars/ usage prevents confusion
- Handlers should be simple and focused
- Task files should be feature-based, not too granular

**Next Steps:**

All three Virgo-Core roles follow good structure patterns. Primary gaps are testing infrastructure (covered in testing-comprehensive.md) and CI/CD automation.
