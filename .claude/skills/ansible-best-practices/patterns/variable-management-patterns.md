# Variable Management Patterns

**Sources:**
- geerlingguy.security (analyzed 2025-10-23)
- geerlingguy.github-users (analyzed 2025-10-23)

**Repositories:**
- https://github.com/geerlingguy/ansible-role-security
- https://github.com/geerlingguy/ansible-role-github-users

## Pattern Confidence Levels

Analyzed 2 geerlingguy roles: security, github-users

**Universal Patterns (Both roles use identical approach):**

1. ✅ **Role-prefixed variable names** - All variables start with role name (security_*, github_users_*)
2. ✅ **Snake_case naming** - Consistent use of underscores, never camelCase
3. ✅ **Feature grouping** - Related variables share prefix (security_ssh_*, github_users_authorized_keys_*)
4. ✅ **Empty lists as defaults** - Default to `[]` for list variables, not undefined
5. ✅ **Boolean defaults** - Use lowercase `true`/`false` for Ansible booleans
6. ✅ **String booleans for configs** - Quote yes/no when they're config values (e.g., `"no"` for SSH config)
7. ✅ **Descriptive full names** - No abbreviations (security_ssh_port, not security_ssh_prt)
8. ✅ **defaults/ for user config** - All user-overridable values in defaults/main.yml
9. ✅ **Inline variable documentation** - Comments in defaults/ file with examples

**Contextual Patterns (Varies by role requirements):**

1. ⚠️  **vars/ for OS-specific values** - security uses vars/{Debian,RedHat}.yml, github-users doesn't need OS-specific vars
2. ⚠️  **Complex variable structures** - security has simple scalars/lists, github-users uses list of strings OR dicts pattern
3. ⚠️  **Variable count** - security has ~20 variables (complex role), github-users has 4 (simple role)
4. ⚠️  **Default URL patterns** - github-users has configurable URL (github_url), security doesn't need this pattern

**Key Finding:** Variable management is highly consistent. The role name prefix pattern prevents ALL variable conflicts in complex playbooks.

## Overview

This document captures variable management patterns from production-grade Ansible roles, demonstrating how to organize, name, and document variables for clarity and maintainability.

## Pattern: defaults/ vs vars/ Usage

### Description

Use **defaults/** for user-configurable values (low precedence, easily overridden) and **vars/** for internal/OS-specific values (high precedence, should not be overridden).

### File Paths

- `defaults/main.yml` - User-facing configuration
- `vars/Debian.yml` - Debian-specific internal values (optional)
- `vars/RedHat.yml` - RedHat-specific internal values (optional)

### defaults/main.yml Pattern

**geerlingguy.security example:**

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

security_fail2ban_enabled: true
security_fail2ban_custom_configuration_template: "jail.local.j2"
```

**geerlingguy.github-users example:**

```yaml
---
github_users: []
# You can specify an object with 'name' (required) and 'groups' (optional):
# - name: geerlingguy
#   groups: www-data,sudo

# Or you can specify a GitHub username directly:
# - geerlingguy

github_users_absent: []
# You can specify an object with 'name' (required):
# - name: geerlingguy

# Or you can specify a GitHub username directly:
# - geerlingguy

github_users_authorized_keys_exclusive: true

github_url: https://github.com
```

**Key Elements:**

1. **Role prefix** - Every variable starts with role name
2. **Feature grouping** - ssh variables together, autoupdate together, etc.
3. **Inline comments** - Examples shown as comments
4. **Default values** - Sensible defaults that work out-of-box
5. **Empty lists** - Default to [] not undefined
6. **Quoted strings** - "no", "yes" for SSH config values (prevents YAML boolean interpretation)

### vars/ OS-Specific Pattern

**geerlingguy.security vars/Debian.yml:**

```yaml
---
security_ssh_config_path: /etc/ssh/sshd_config
security_sshd_name: ssh
```

**geerlingguy.security vars/RedHat.yml:**

```yaml
---
security_ssh_config_path: /etc/ssh/sshd_config
security_sshd_name: sshd
```

**Loading Pattern in tasks/main.yml:**

```yaml
- name: Include OS-specific variables.
  include_vars: "{{ ansible_os_family }}.yml"
```

### Decision Matrix

| Variable Type | Location | Precedence | Use Case | Override |
|--------------|----------|------------|----------|----------|
| User configuration | defaults/ | Low | Settings users customize | Easily overridden in playbook |
| OS-specific paths | vars/ | High | File paths, service names | Should not be overridden |
| Feature toggles | defaults/ | Low | Enable/disable features | User choice |
| Internal constants | vars/ | High | Values role needs to work | Role implementation detail |

### When to Use

**defaults/ - Use for:**
- Port numbers users might change
- Feature enable/disable flags
- List of items users configure
- Behavioral options
- Template paths users might override

**vars/ - Use for:**
- Service names that differ by OS (ssh vs sshd)
- Configuration file paths
- Package names that vary by OS
- Internal role constants
- Values that should rarely/never be overridden

### Anti-pattern

- ❌ Don't put user-facing config in vars/ (can't be easily overridden)
- ❌ Don't put OS-specific paths in defaults/ (users shouldn't need to change)
- ❌ Avoid duplicating values between defaults/ and vars/
- ❌ Don't use vars/ for what should be defaults/ (breaks override mechanism)

## Pattern: Variable Naming Conventions

### Description

Use a consistent, hierarchical naming pattern: `{role_name}_{feature}_{attribute}`

### Naming Pattern Structure

```
{role_name}_{feature}_{attribute}_{sub_attribute}
```

### Examples from security role

- `security_ssh_port` - Role: security, Feature: ssh, Attribute: port
- `security_ssh_password_authentication` - Role: security, Feature: ssh, Attribute: password_authentication
- `security_fail2ban_enabled` - Role: security, Feature: fail2ban, Attribute: enabled
- `security_autoupdate_reboot_time` - Role: security, Feature: autoupdate, Attribute: reboot_time
- `security_ssh_restart_handler_state` - Role: security, Feature: ssh, Attribute: restart_handler_state

### Examples from github-users role

- `github_users` - Role: github-users (shortened to github), Feature: users (implicit)
- `github_users_absent` - Role: github, Feature: users, Attribute: absent
- `github_users_authorized_keys_exclusive` - Role: github, Feature: users, Attribute: authorized_keys_exclusive
- `github_url` - Role: github, Feature: url (API endpoint)

### Naming Guidelines

1. **Always use role prefix** - Prevents variable name collisions
2. **Use full words** - No abbreviations (password not pwd, configuration not cfg)
3. **Snake_case only** - Underscores, never camelCase or kebab-case
4. **Feature grouping** - Related vars share feature prefix for logical grouping
5. **Hierarchical structure** - General to specific (ssh → password → authentication)
6. **Boolean naming** - Use `_enabled`, `_disabled`, or descriptive names (not just `_flag`)
7. **Descriptive, not cryptic** - Variable name should explain purpose

### When to Use

- All role variables without exception
- Internal variables (loop vars, registered results) can skip prefix if scope is limited
- Consistently apply pattern across all variables in the role

### Anti-pattern

- ❌ Generic names: `port`, `enabled`, `users` (conflicts in complex playbooks)
- ❌ Abbreviations: `cfg`, `pwd`, `usr` (harder to read)
- ❌ camelCase: `githubUsersAbsent` (not Ansible convention)
- ❌ Inconsistent prefixes: Some vars with prefix, some without
- ❌ Overly long names: `security_ssh_configuration_password_authentication_setting` (be descriptive, not verbose)

## Pattern: Boolean vs String Values

### Description

Distinguish between Ansible booleans and configuration file string values. Quote strings that look like booleans.

### Ansible Booleans (unquoted)

**Use for feature flags, task conditions, role logic:**

```yaml
security_fail2ban_enabled: true
security_autoupdate_enabled: true
github_users_authorized_keys_exclusive: true
```

**Valid Ansible boolean values:**
- `true` / `false` (preferred)
- `yes` / `no`
- `on` / `off`
- `1` / `0`

### Configuration Strings (quoted)

**Use for values written to config files:**

```yaml
security_ssh_password_authentication: "no"
security_ssh_permit_root_login: "no"
security_ssh_usedns: "no"
security_autoupdate_reboot: "false"
```

**Rationale:**

When Ansible sees `no` or `false` without quotes, it converts to boolean. When this boolean is then written to a config file (via lineinfile or template), it becomes `False` or `false`, which might not match the config file's expected format (e.g., SSH expects `no`/`yes`).

### Pattern from security role

```yaml
# Ansible boolean (role logic)
security_fail2ban_enabled: true  # Controls whether to install fail2ban

# Config string (written to /etc/ssh/sshd_config)
security_ssh_password_authentication: "no"  # Literal string "no" for SSH
```

### When to Use

**Unquoted booleans:**
- Feature enable/disable flags (`role_feature_enabled`)
- Task conditionals (`when:` clauses)
- Handler behavior
- Internal role logic

**Quoted strings:**
- Values written to config files
- Values that must preserve exact format
- Values that look like booleans but aren't

### Anti-pattern

- ❌ Unquoted yes/no for config values (becomes `True`/`False` in file)
- ❌ Quoted booleans for feature flags (unnecessarily complex)
- ❌ Inconsistent quoting across similar variables

## Pattern: List and Dictionary Structures

### Description

Use flexible data structures that support both simple and complex use cases.

### Simple List Pattern

**github-users simple list:**

```yaml
github_users:
  - geerlingguy
  - fabpot
  - johndoe
```

**security simple list:**

```yaml
security_sudoers_passwordless:
  - deployuser
  - admin

security_ssh_allowed_users:
  - alice
  - bob
```

### List of Dictionaries Pattern

**github-users complex pattern:**

```yaml
github_users:
  - name: geerlingguy
    groups: www-data,sudo
  - name: fabpot
    groups: developers
  - johndoe  # Still supports simple string
```

**Task handling both patterns:**

```yaml
- name: Ensure GitHub user accounts are present.
  user:
    name: "{{ item.name | default(item) }}"  # Handles both dict and string
    groups: "{{ item.groups | default(omit) }}"  # Optional attribute
```

**Key technique:** `{{ item.name | default(item) }}`
- If item is a dict with 'name' key → use item.name
- If item is a string → default to item itself
- Supports both simple and complex usage

### Dictionary Pattern

**security dictionary example (inferred, not in role):**

```yaml
security_ssh_config:
  port: 22
  password_auth: "no"
  permit_root: "no"
```

This pattern is less common in geerlingguy roles (flat variables preferred for simplicity).

### When to Use

**Simple lists:**
- When each item needs only one value
- User management (simple usernames)
- Package lists
- Simple configuration items

**List of dicts:**
- When items have multiple optional attributes
- Users with groups, shells, home directories
- Complex configuration items
- When backwards compatibility with simple list is needed

**Flat variables:**
- When configuration is not deeply nested
- When clarity is more important than brevity
- When users need to override individual values

### Anti-pattern

- ❌ Deep nesting (3+ levels) - Hard to override, hard to document
- ❌ Inconsistent structure - Some items as strings, others as dicts without handling
- ❌ Required attributes in complex structures without defaults
- ❌ Over-engineering simple use cases

## Pattern: Default Value Strategies

### Description

Choose appropriate default values that balance security, usability, and least surprise.

### Empty List Defaults

```yaml
github_users: []
github_users_absent: []
security_ssh_allowed_users: []
security_sudoers_passwordless: []
```

**Rationale:**
- Safe default (no users created/removed)
- Allows conditional logic: `when: github_users | length > 0`
- Users must explicitly configure
- No surprising side effects

### Secure Defaults

```yaml
security_ssh_password_authentication: "no"
security_ssh_permit_root_login: "no"
github_users_authorized_keys_exclusive: true
```

**Rationale:**
- Security-first approach
- Users can relax security if needed
- Prevents accidental insecure configurations

### Service State Defaults

```yaml
security_sshd_state: started
security_ssh_restart_handler_state: restarted
```

**Rationale:**
- Explicit state management
- Allows users to override (e.g., for testing)
- Documents expected state

### Feature Toggles

```yaml
security_fail2ban_enabled: true
security_autoupdate_enabled: true
```

**Rationale:**
- Enable useful features by default
- Easy to disable if not wanted
- Clear intent

### Sensible Configuration Defaults

```yaml
security_ssh_port: 22
github_url: https://github.com
```

**Rationale:**
- Standard/expected values
- Users only change when needed
- Reduces configuration burden

### When to Use

- **Empty lists** - When no default action is safe
- **Secure defaults** - For security-sensitive settings
- **Enabled by default** - For beneficial features with no downsides
- **Standard values** - For well-known defaults (port 22, standard URLs)

### Anti-pattern

- ❌ Undefined defaults - Use `[]` or explicit `null`, not absent
- ❌ Insecure defaults - Don't default to `password_authentication: "yes"`
- ❌ Surprising defaults - Don't create users/change configs by default
- ❌ Missing defaults - Every variable in defaults/main.yml should have a value

## Comparison to Virgo-Core Roles

### system_user Role

**Variable Analysis:**

```yaml
# From system_user/defaults/main.yml
system_user_name: ""
system_user_groups: []
system_user_shell: /bin/bash
system_user_ssh_keys: []
system_user_sudo_access: "full"
system_user_sudo_commands: []
system_user_state: present
```

**Matches geerlingguy patterns:**
- ✅ Role prefix (system_user_*)
- ✅ Snake_case naming
- ✅ Empty list defaults
- ✅ Descriptive names
- ✅ All in defaults/main.yml

**Gaps:**
- ⚠️  No feature grouping (all variables are related to user management, so not needed)
- ⚠️  Could use string for sudo_access ("full", "commands", "none" vs full/limited)
- ✅ No vars/ directory needed (no OS-specific values)

**Pattern Match:** 95% - Excellent variable management

### proxmox_access Role

**Variable Analysis (sample):**

```yaml
# From proxmox_access/defaults/main.yml
proxmox_access_roles: []
proxmox_access_groups: []
proxmox_access_users: []
proxmox_access_tokens: []
proxmox_access_acls: []
proxmox_access_export_terraform_env: false
```

**Matches:**
- ✅ Role prefix (proxmox_access_*)
- ✅ Snake_case naming
- ✅ Empty list defaults
- ✅ Boolean flag for optional feature
- ✅ Feature grouping (access_roles, access_groups, access_users)

**Gaps:**
- ✅ No OS-specific vars needed (Proxmox-specific role)
- ✅ Good variable organization

**Pattern Match:** 100% - Perfect variable management

### proxmox_network Role

**Variable Analysis (sample):**

```yaml
# From proxmox_network/defaults/main.yml
proxmox_network_bridges: []
proxmox_network_vlans: []
proxmox_network_verify_connectivity: true
```

**Matches:**
- ✅ Role prefix (proxmox_network_*)
- ✅ Snake_case naming
- ✅ Empty list defaults
- ✅ Boolean flag
- ✅ Feature grouping

**Gaps:**
- ✅ Excellent pattern adherence

**Pattern Match:** 100% - Perfect variable management

## Summary

**Universal Variable Management Patterns:**

1. Role-prefixed variable names (prevents conflicts)
2. Snake_case naming convention
3. Feature grouping with shared prefixes
4. defaults/ for user configuration (low precedence)
5. vars/ for OS-specific values (high precedence)
6. Empty lists as safe defaults (`[]`)
7. Quoted string booleans for config files (`"no"`, `"yes"`)
8. Unquoted Ansible booleans for feature flags
9. Flexible list/dict patterns with `item.name | default(item)`
10. Descriptive full names, no abbreviations

**Key Takeaways:**

- Variable naming is not just convention - it prevents real bugs
- defaults/ vs vars/ distinction is critical for override behavior
- Quote config file values that look like booleans
- Support both simple and complex usage patterns when possible
- Default to secure, safe, empty values
- Feature grouping makes variable relationships clear

**Virgo-Core Assessment:**

All three Virgo-Core roles demonstrate excellent variable management practices. They follow geerlingguy patterns closely and have no critical gaps. Minor enhancements could include more inline documentation in defaults/ files.

**Next Steps:**

Apply these patterns rigorously in new roles. The variable management discipline in existing roles should be maintained and used as a template.
