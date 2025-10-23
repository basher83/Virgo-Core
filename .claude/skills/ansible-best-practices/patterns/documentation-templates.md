# Documentation Templates

**Source:** geerlingguy.security (analyzed 2025-10-23)

**Repository:** https://github.com/geerlingguy/ansible-role-security

## Overview

This document captures documentation patterns from the geerlingguy.security role, demonstrating how to create clear, comprehensive README files that help users understand and use the role effectively.

## README Structure

### Pattern: Comprehensive README Template

**Description:** A well-structured README that follows a consistent format, providing all necessary information for users to understand and use the role.

**File Path:** `README.md`

**Standard README Sections:**

1. Title and badges
2. Caveat/Warning (if applicable)
3. Role description
4. Requirements
5. Role Variables
6. Dependencies
7. Example Playbook
8. License
9. Author Information

### Section 1: Title and Badges

**Example Code:**

```markdown
# Ansible Role: Security (Basics)

[![CI](https://github.com/geerlingguy/ansible-role-security/actions/workflows/ci.yml/badge.svg)](https://github.com/geerlingguy/ansible-role-security/actions/workflows/ci.yml)
```

**Key Elements:**

1. **Clear title** - Role name with descriptive subtitle
2. **CI badge** - Shows test status (builds confidence)
3. **Badge links to CI** - Users can see test results

**When to Use:**

- Always include clear role title
- Add CI badge if you have automated testing
- Link badges to their status pages
- Consider adding Galaxy badge, version badge, downloads badge

**Badge Examples:**

```markdown
[![CI](https://github.com/user/repo/workflows/ci.yml/badge.svg)](https://github.com/user/repo/actions)
[![Ansible Galaxy](https://img.shields.io/badge/galaxy-user.rolename-blue.svg)](https://galaxy.ansible.com/user/rolename)
[![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)
```

**Anti-pattern:**

- Don't skip the title (obvious but happens)
- Avoid outdated or broken badges
- Don't add badges that don't provide value

### Section 2: Caveat/Warning (Optional)

**Example Code:**

```markdown
**First, a major, MAJOR caveat**: the security of your servers is YOUR
responsibility. If you think simply including this role and adding a firewall
makes a server secure, then you're mistaken. Read up on Linux, network, and
application security, and know that no matter how much you know, you can
always make every part of your stack more secure.

That being said, this role performs some basic security configuration on
RedHat and Debian-based linux systems. It attempts to:

  - Install software to monitor bad SSH access (fail2ban)
  - Configure SSH to be more secure (disabling root login, requiring
    key-based authentication, and allowing a custom SSH port to be set)
  - Set up automatic updates (if configured to do so)

There are a few other things you may or may not want to do (which are not
included in this role) to make sure your servers are more secure, like:

  - Use logwatch or a centralized logging server to analyze and monitor
    log files
  - Securely configure user accounts and SSH keys (this role assumes you're
    not using password authentication or logging in as root)
  - Have a well-configured firewall (check out the `geerlingguy.firewall`
    role on Ansible Galaxy for a flexible example)

Again: Your servers' security is *your* responsibility.
```

**Key Elements:**

1. **Prominent warning** - Sets expectations clearly
2. **Scope definition** - What the role does and doesn't do
3. **Additional recommendations** - Points to complementary practices
4. **Emphasis** - Bold, italics, repetition for important points

**When to Use:**

- Security-related roles (critical warnings)
- Roles that could cause service disruption
- Roles with common misunderstandings
- Complex roles with limited scope

**Anti-pattern:**

- Don't add warnings for routine roles
- Avoid legal disclaimers (that's what LICENSE is for)
- Don't be condescending

### Section 3: Requirements

**Example Code:**

```markdown
## Requirements

For obvious reasons, `sudo` must be installed if you want to manage the
sudoers file with this role.

On RedHat/CentOS systems, make sure you have the EPEL repository installed
(you can include the `geerlingguy.repo-epel` role to get it installed).

No special requirements for Debian/Ubuntu systems.
```

**Key Elements:**

1. **System requirements** - Software that must be pre-installed
2. **OS-specific requirements** - Different requirements per platform
3. **How to meet requirements** - Links to other roles or instructions
4. **Explicit "no requirements" statement** - Clarity when none exist

**When to Use:**

- List any software that must be installed first
- Document repository requirements (EPEL, PPAs)
- Mention privilege requirements (become/sudo)
- Note Python library dependencies
- State "None" if no requirements (clear communication)

**Anti-pattern:**

- Don't assume users know about EPEL or special repos
- Avoid listing Ansible itself (assumed)
- Don't skip this section (at least say "None")

### Section 4: Role Variables

**Example Code:**

```markdown
## Role Variables

Available variables are listed below, along with default values (see
`defaults/main.yml`):

    security_ssh_port: 22

The port through which you'd like SSH to be accessible. The default is port
22, but if you're operating a server on the open internet, and have no
firewall blocking access to port 22, you'll quickly find that thousands of
login attempts per day are not uncommon. You can change the port to a
nonstandard port (e.g. 2849) if you want to avoid these thousands of
automated penetration attempts.

    security_ssh_password_authentication: "no"
    security_ssh_permit_root_login: "no"
    security_ssh_usedns: "no"
    security_ssh_permit_empty_password: "no"
    security_ssh_challenge_response_auth: "no"
    security_ssh_gss_api_authentication: "no"
    security_ssh_x11_forwarding: "no"

Security settings for SSH authentication. It's best to leave these set to
`"no"`, but there are times (especially during initial server configuration
or when you don't have key-based authentication in place) when one or all
may be safely set to `'yes'`. **NOTE: It is _very_ important that you quote
the 'yes' or 'no' values. Failure to do so may lock you out of your server.**

    security_ssh_allowed_users: []
    # - alice
    # - bob
    # - charlie

A list of users allowed to connect to the host over SSH.  If no user is
defined in the list, the task will be skipped.

    security_sudoers_passwordless: []
    security_sudoers_passworded: []

A list of users who should be added to the sudoers file so they can run any
command as root (via `sudo`) either without a password or requiring a
password for each command, respectively.

    security_autoupdate_enabled: true

Whether to install/enable `yum-cron` (RedHat-based systems) or
`unattended-upgrades` (Debian-based systems). System restarts will not
happen automatically in any case, and automatic upgrades are no excuse for
sloppy patch and package management, but automatic updates can be helpful
as yet another security measure.

    security_fail2ban_enabled: true

Whether to install/enable `fail2ban`. You might not want to use fail2ban if
you're already using some other service for login and intrusion detection
(e.g. [ConfigServer](http://configserver.com/cp/csf.html)).
```

**Documentation Pattern:**

For each variable:

1. **Show default value** - Code-formatted with actual default
2. **Description** - What it does, when to use it
3. **Context** - Why you might change it
4. **Examples** - Show different values for lists/dicts
5. **Warnings** - Important notes (quoting, locking out, etc.)

**Formatting Guidelines:**

- Use 4-space indentation for default values
- Group related variables together
- Add blank lines between variable groups
- Use inline code formatting for values
- Bold important warnings
- Comment out example list items

**When to Use:**

- Document ALL variables from defaults/main.yml
- Group related variables (ssh_*, autoupdate_*, etc.)
- Provide context, not just description
- Include warnings for dangerous settings
- Show example values for complex structures

**Anti-pattern:**

- Don't just list variables without explanation
- Avoid documenting vars/ (internal implementation)
- Don't skip context (users need to know WHY)
- Avoid stale documentation (keep in sync with defaults/)

### Pattern: Variable Table Format (Alternative)

**Description:** Some roles use a table format for variable documentation. While geerlingguy.security doesn't use this, it's a valid alternative pattern.

**Example Table Format:**

```markdown
## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `security_ssh_port` | `22` | SSH port number |
| `security_ssh_password_authentication` | `"no"` | Enable password authentication |
| `security_fail2ban_enabled` | `true` | Install and configure fail2ban |
```

**When to Use:**

- Roles with many simple variables
- When brief descriptions are sufficient
- For quick reference guides

**Comparison:**

| Format | Best For | Pros | Cons |
|--------|----------|------|------|
| Text with examples | Complex variables, detailed context | Detailed explanations, examples | More verbose |
| Table | Simple variables, quick reference | Concise, scannable | Limited detail space |

**Virgo-Core Preference:**

Use text format with examples (matches geerlingguy pattern) for main documentation, optionally add table for quick reference.

### Section 5: Dependencies

**Example Code:**

```markdown
## Dependencies

None.
```

**When Dependencies Exist:**

```markdown
## Dependencies

This role depends on:

- `geerlingguy.repo-epel` (for RedHat/CentOS systems)
- `geerlingguy.firewall` (recommended but optional)

The role will automatically install required dependencies from Ansible Galaxy.
```

**Key Elements:**

1. **Explicit "None"** - Clear when no dependencies
2. **List dependencies** - With context about why needed
3. **Distinguish required vs optional** - Important for users
4. **Note automatic installation** - Reduces confusion

**When to Use:**

- Always include this section
- List role dependencies from meta/main.yml
- Note recommended complementary roles
- State "None" if no dependencies

**Anti-pattern:**

- Don't skip this section
- Avoid listing collection dependencies here (put in Requirements)

### Section 6: Example Playbook

**Example Code:**

```markdown
## Example Playbook

    - hosts: servers
      vars_files:
        - vars/main.yml
      roles:
        - geerlingguy.security

*Inside `vars/main.yml`*:

    security_sudoers_passworded:
      - johndoe
      - deployacct
```

**Key Elements:**

1. **Minimal working example** - Shows basic usage
2. **Variable override example** - Demonstrates customization
3. **Multiple files** - Shows playbook and vars file
4. **Real-world example** - Not generic foo/bar examples
5. **Indentation** - 4 spaces for YAML, maintains readability

**Enhanced Example Pattern:**

```markdown
## Example Playbook

### Basic Usage

    - hosts: all
      roles:
        - geerlingguy.security

### Custom Configuration

    - hosts: webservers
      vars:
        security_ssh_port: 2222
        security_fail2ban_enabled: true
        security_autoupdate_enabled: true
      roles:
        - geerlingguy.security

### Advanced Example with Sudoers

    - hosts: appservers
      vars:
        security_sudoers_passwordless:
          - deploy
        security_sudoers_passworded:
          - developer
          - operator
      roles:
        - geerlingguy.security
```

**When to Use:**

- Always include at least one example
- Show basic usage first
- Add advanced examples for complex features
- Use realistic variable values
- Include multiple scenarios if role has distinct use cases

**Anti-pattern:**

- Don't use only generic examples (foo, bar, example.com)
- Avoid incomplete examples (missing required vars)
- Don't show every possible variable (overwhelming)

### Section 7: License and Author

**Example Code:**

```markdown
## License

MIT (Expat) / BSD

## Author Information

This role was created in 2014 by [Jeff Geerling](https://www.jeffgeerling.com/),
author of [Ansible for DevOps](https://www.ansiblefordevops.com/).
```

**Key Elements:**

1. **License name** - Clear license statement
2. **Author information** - Who created/maintains it
3. **Links** - Author website, book, company
4. **Year created** - Provides context

**When to Use:**

- Always include license (required for Galaxy)
- Add author name and contact
- Link to LICENSE file for full text
- Keep it brief

**Anti-pattern:**

- Don't include full license text in README (use LICENSE file)
- Avoid complex author information

## Additional Documentation Patterns

### Pattern: Troubleshooting Section

**Description:** While geerlingguy.security doesn't include a troubleshooting section, more complex roles should include one.

**Example Troubleshooting Section:**

```markdown
## Troubleshooting

### SSH Connection Refused After Running Role

If you lose SSH connectivity after running this role, you may have:

1. Changed the SSH port without updating your firewall rules
2. Disabled password authentication without setting up SSH keys
3. Set `security_ssh_allowed_users` without including your username

**Solution:** Access the server via console and check `/etc/ssh/sshd_config`.

### Fail2ban Not Starting

If fail2ban fails to start, check that the log files it monitors exist:

    ls -la /var/log/auth.log

On some minimal systems, these log files may not exist until a service
writes to them.

**Solution:** Create empty log files or disable fail2ban temporarily.
```

**When to Use:**

- Roles that modify critical services (SSH, networking)
- Roles with common configuration mistakes
- Roles with tricky OS-specific issues
- Complex roles with multiple failure modes

**Anti-pattern:**

- Don't include troubleshooting for roles that are straightforward
- Avoid listing every possible error (focus on common issues)

### Pattern: Inline Code and Formatting

**Formatting Patterns from README:**

1. **Inline code** - Use backticks: `fail2ban`, `sudo`, `/etc/ssh/sshd_config`
2. **File paths** - Always use inline code: `defaults/main.yml`
3. **Commands** - Inline code for short commands: `sudo systemctl restart ssh`
4. **Variable names** - Inline code: `security_ssh_port`
5. **Code blocks** - Use 4-space indentation for YAML/code examples
6. **Emphasis** - Bold for **important warnings**, italics for *emphasis*
7. **Lists** - Use `-` for unordered, numbers for ordered

**Example:**

```markdown
To configure SSH port, set `security_ssh_port` in your playbook variables.
The configuration is written to `/etc/ssh/sshd_config` and validated with
`sshd -T -f %s` before applying. **WARNING**: Changing the SSH port without
updating firewall rules will lock you out.
```

## Comparison to Virgo-Core Roles

### system_user Role

**README Analysis:**

**Matches:**

- ✅ Has clear title
- ✅ Good role description
- ✅ Documents variables
- ✅ Includes example playbook
- ✅ Has license and author sections

**Gaps:**

- ❌ No CI badge (no CI yet)
- ⚠️  Variable documentation less detailed (could add more context)
- ⚠️  Could add troubleshooting section (SSH key issues common)
- ⚠️  No table of contents (nice-to-have for longer docs)

**Priority Actions:**

1. **Important:** Enhance variable documentation with usage context (30 min)
2. **Important:** Add troubleshooting section (1 hour)
3. **Nice-to-have:** Add CI badge after implementing CI (5 min)

### proxmox_access Role

**README Analysis:**

**Matches:**

- ✅ Comprehensive variable documentation
- ✅ Good examples
- ✅ Security warnings included

**Gaps:**

- ❌ No CI badge
- ⚠️  Could add more example playbooks (different scenarios)
- ⚠️  Troubleshooting section would help (token creation failures)

**Priority Actions:**

1. **Important:** Add troubleshooting for common token issues (1 hour)
2. **Important:** Add more example scenarios (30 min)
3. **Nice-to-have:** Add requirements section (15 min)

### proxmox_network Role

**README Analysis:**

**Matches:**

- ✅ Good structure
- ✅ Clear variable documentation
- ✅ Network architecture context

**Gaps:**

- ❌ No CI badge
- ⚠️  Network troubleshooting section would be valuable
- ⚠️  Could add verification examples (how to check it worked)

**Priority Actions:**

1. **Important:** Add network troubleshooting section (1 hour)
2. **Important:** Add verification examples (30 min)
3. **Nice-to-have:** Add network topology diagram (1 hour)

## Template: Complete README Structure

```markdown
# Ansible Role: [Role Name]

[![CI](badge-url)](ci-url)
[![Ansible Galaxy](badge-url)](galaxy-url)

[Brief role description - what it does, key features]

[Optional: Warning/caveat section for critical roles]

## Requirements

[List prerequisites, or "None"]

## Role Variables

Available variables are listed below, along with default values (see
`defaults/main.yml`):

    variable_name: default_value

[Description of variable, when to change it, usage examples]

    another_variable: []
    # - example1
    # - example2

[Description with examples]

## Dependencies

[List role dependencies, or "None"]

## Example Playbook

### Basic Usage

    - hosts: all
      roles:
        - rolename

### Custom Configuration

    - hosts: servers
      vars:
        variable_name: custom_value
      roles:
        - rolename

## Troubleshooting

[Optional: Common issues and solutions]

## License

MIT / BSD / Apache 2.0

## Author Information

This role was created by [Author Name](link), [additional context].
```

## Summary

**Universal Patterns Identified:**

1. Consistent README structure (title → requirements → variables → examples → license)
2. CI badges for test status
3. Comprehensive variable documentation with defaults and context
4. Multiple example playbooks (basic → advanced)
5. Explicit "None" statements for empty sections
6. Inline code formatting for variables, files, commands
7. Bold warnings for critical information
8. Commented examples for list variables

**Key Takeaways:**

- Variable documentation should include defaults AND context
- Examples should progress from simple to complex
- Warnings prevent common mistakes
- Consistent formatting improves readability
- Explicit "None" is better than omitting sections
- Troubleshooting saves support time

**Next Steps:**

Enhance Virgo-Core role READMEs with:
1. More detailed variable context
2. Troubleshooting sections
3. CI badges (after implementing testing)
4. Additional example scenarios
