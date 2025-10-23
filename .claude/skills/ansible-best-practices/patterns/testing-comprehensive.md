# Comprehensive Testing Patterns

**Source:** geerlingguy.security (analyzed 2025-10-23)

**Repository:** https://github.com/geerlingguy/ansible-role-security

## Overview

This document captures testing patterns extracted from the geerlingguy.security role, a production-grade Ansible role with comprehensive testing infrastructure. The role demonstrates industry-standard approaches to testing, CI/CD integration, and quality assurance.

## Molecule Configuration Structure

### Pattern: Default Scenario Structure

**Description:** Molecule uses a default scenario with a standardized directory structure for testing role convergence and idempotence.

**File Path:** `molecule/default/molecule.yml`

**Example Code:**

```yaml
---
role_name_check: 1
dependency:
  name: galaxy
  options:
    ignore-errors: true
driver:
  name: docker
platforms:
  - name: instance
    image: "geerlingguy/docker-${MOLECULE_DISTRO:-rockylinux9}-ansible:latest"
    command: ${MOLECULE_DOCKER_COMMAND:-""}
    volumes:
      - /sys/fs/cgroup:/sys/fs/cgroup:rw
    cgroupns_mode: host
    privileged: true
    pre_build_image: true
provisioner:
  name: ansible
  playbooks:
    converge: ${MOLECULE_PLAYBOOK:-converge.yml}
```

**Key Elements:**

1. **role_name_check: 1** - Validates role naming conventions
2. **dependency.name: galaxy** - Automatically installs Galaxy dependencies
3. **ignore-errors: true** - Prevents dependency failures from blocking tests
4. **driver.name: docker** - Uses Docker for fast, lightweight test instances
5. **Environment variable defaults** - `${MOLECULE_DISTRO:-rockylinux9}` provides defaults with override capability
6. **Privileged containers** - Required for systemd and service management testing
7. **cgroup mounting** - Enables systemd to function properly in containers

**When to Use:**

- All production roles should have a molecule/default scenario
- Use Docker driver for most role testing (fast, reproducible)
- Enable privileged mode when testing service management or systemd
- Use environment variables for flexible test matrix configuration

**Anti-pattern:**

- Don't hardcode distribution names (use MOLECULE_DISTRO variable)
- Don't skip role_name_check (helps catch galaxy naming issues)
- Avoid ignoring dependency errors in production (use only for specific cases)

### Pattern: Converge Playbook with Pre-Tasks

**Description:** The converge playbook includes pre-tasks to prepare the test environment before role execution, ensuring consistent test conditions across different distributions.

**File Path:** `molecule/default/converge.yml`

**Example Code:**

```yaml
---
- name: Converge
  hosts: all
  #become: true

  pre_tasks:
    - name: Update apt cache.
      package:
        update_cache: true
        cache_valid_time: 600
      when: ansible_os_family == 'Debian'

    - name: Ensure build dependencies are installed (RedHat).
      package:
        name:
          - openssh-server
          - openssh-clients
        state: present
      when: ansible_os_family == 'RedHat'

    - name: Ensure build dependencies are installed (Debian).
      package:
        name:
          - openssh-server
          - openssh-client
        state: present
      when: ansible_os_family == 'Debian'

  roles:
    - role: geerlingguy.security
```

**Key Elements:**

1. **Distribution-specific setup** - Different package names for RedHat vs Debian
2. **Package cache updates** - Ensures latest package metadata
3. **Dependency installation** - Installs prerequisites before role execution
4. **Commented become directive** - Can be enabled if needed for testing
5. **Simple role invocation** - Minimal role configuration for basic testing

**When to Use:**

- Install test-specific dependencies that aren't part of the role
- Prepare test environment (create directories, files, users)
- Update package caches to avoid transient failures
- Set up prerequisites that vary by OS family

**Anti-pattern:**

- Don't install role dependencies here (use meta/main.yml dependencies instead)
- Avoid complex logic in pre-tasks (keep test setup simple)
- Don't duplicate role functionality in pre-tasks

## Test Matrix

### Pattern: Multi-Distribution Testing

**Description:** Test the role across multiple Linux distributions to ensure cross-platform compatibility.

**File Path:** `.github/workflows/ci.yml` (matrix strategy section)

**Example Code:**

```yaml
molecule:
  name: Molecule
  runs-on: ubuntu-latest
  strategy:
    matrix:
      distro:
        - rockylinux9
        - ubuntu2204
        - debian11
```

**Key Elements:**

1. **Strategic distribution selection** - Mix of RedHat and Debian families
2. **Current LTS/stable versions** - Rocky Linux 9, Ubuntu 22.04, Debian 11
3. **Representative sampling** - Not exhaustive, but covers main use cases
4. **Environment variable passing** - MOLECULE_DISTRO passed to molecule

**Test Coverage Strategy:**

- **RedHat family:** rockylinux9 (represents RHEL, CentOS, Rocky, Alma)
- **Debian family:** ubuntu2204, debian11 (covers Ubuntu and Debian variants)
- **Version selection:** Latest LTS or stable releases

**When to Use:**

- Test on at least one RedHat and one Debian distribution
- Include distributions you actually support in production
- Use latest stable/LTS versions unless testing legacy compatibility
- Consider adding Fedora for testing newer systemd/package versions

**Anti-pattern:**

- Don't test every possible distribution (diminishing returns)
- Avoid outdated distributions unless explicitly supported
- Don't test distributions you won't support in production

## CI/CD Integration

### Pattern: GitHub Actions Workflow Structure

**Description:** Comprehensive CI workflow with separate linting and testing jobs, triggered on multiple events.

**File Path:** `.github/workflows/ci.yml`

**Example Code:**

```yaml
---
name: CI
'on':
  pull_request:
  push:
    branches:
      - master
  schedule:
    - cron: "30 4 * * 4"

defaults:
  run:
    working-directory: 'geerlingguy.security'

jobs:

  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - name: Check out the codebase.
        uses: actions/checkout@v4
        with:
          path: 'geerlingguy.security'

      - name: Set up Python 3.
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'

      - name: Install test dependencies.
        run: pip3 install yamllint

      - name: Lint code.
        run: |
          yamllint .

  molecule:
    name: Molecule
    runs-on: ubuntu-latest
    strategy:
      matrix:
        distro:
          - rockylinux9
          - ubuntu2204
          - debian11

    steps:
      - name: Check out the codebase.
        uses: actions/checkout@v4
        with:
          path: 'geerlingguy.security'

      - name: Set up Python 3.
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'

      - name: Install test dependencies.
        run: pip3 install ansible molecule molecule-plugins[docker] docker

      - name: Run Molecule tests.
        run: molecule test
        env:
          PY_COLORS: '1'
          ANSIBLE_FORCE_COLOR: '1'
          MOLECULE_DISTRO: ${{ matrix.distro }}
```

**Key Elements:**

1. **Multiple trigger events:**
   - `pull_request` - Test all PRs before merge
   - `push.branches: master` - Test main branch commits
   - `schedule: cron` - Weekly scheduled tests (Thursday 4:30 AM UTC)

2. **Separate lint job:**
   - Runs independently of molecule tests
   - Fails fast on YAML syntax issues
   - Uses yamllint for consistency

3. **Working directory default:**
   - Sets context for Galaxy role structure
   - Matches expected role path in Galaxy

4. **Environment variables:**
   - PY_COLORS, ANSIBLE_FORCE_COLOR - Enable colored output in CI logs
   - MOLECULE_DISTRO - Passes matrix value to molecule

5. **Dependency installation:**
   - ansible - The automation engine
   - molecule - Testing framework
   - molecule-plugins[docker] - Docker driver support
   - docker - Python Docker SDK

**When to Use:**

- Always run tests on pull requests (prevents bad merges)
- Test main branch to catch integration issues
- Use scheduled tests to detect dependency breakage
- Separate linting from testing for faster feedback
- Enable colored output for easier log reading

**Anti-pattern:**

- Don't run expensive tests on every commit to every branch
- Avoid skipping scheduled tests (catches dependency rot)
- Don't combine linting and testing in one job (slower feedback)

## Idempotence Testing

### Pattern: Molecule Default Test Sequence

**Description:** Molecule's default test sequence includes an idempotence test that runs the role twice and verifies no changes occur on the second run.

**Test Sequence (molecule test command):**

1. **dependency** - Install Galaxy dependencies
2. **cleanup** - Remove previous test containers
3. **destroy** - Ensure clean state
4. **syntax** - Check playbook syntax
5. **create** - Create test instances
6. **prepare** - Run preparation playbook (if exists)
7. **converge** - Run the role
8. **idempotence** - Run role again, expect no changes
9. **verify** - Run verification tests (if exists)
10. **cleanup** - Remove test containers
11. **destroy** - Final cleanup

**Idempotence Verification:**

Molecule automatically fails if the second converge run reports changed tasks. This validates that the role:

- Uses proper idempotent modules (lineinfile, service, package, etc.)
- Checks state before making changes
- Doesn't have tasks that always report changed

**When to Use:**

- Run full `molecule test` in CI/CD
- Use `molecule converge` for faster development iteration
- Use `molecule verify` to test without full cleanup

**Anti-pattern:**

- Don't disable idempotence testing (critical quality check)
- Avoid using command/shell modules without changed_when
- Don't mark tasks as changed:false when they actually change things

## Verification Strategies

### Pattern: No Explicit Verify Playbook

**Description:** The geerlingguy.security role relies on:

1. **Molecule's automatic idempotence check** - Validates role stability
2. **CI matrix testing** - Tests across distributions
3. **Converge success** - Role executes without errors

**Alternative Verification Approaches:**

For more complex roles, consider adding `molecule/default/verify.yml`:

```yaml
---
- name: Verify
  hosts: all
  tasks:
    - name: Check SSH service is running
      service:
        name: ssh
        state: started
      check_mode: true
      register: result
      failed_when: result.changed

    - name: Verify fail2ban is installed
      package:
        name: fail2ban
        state: present
      check_mode: true
      register: result
      failed_when: result.changed
```

**When to Use:**

- Simple roles: Rely on idempotence testing
- Complex roles: Add explicit verification
- Stateful services: Verify running state
- Configuration files: Test file contents/permissions

**Anti-pattern:**

- Don't create verification tests that duplicate idempotence tests
- Avoid complex verification logic (keep tests simple)

## Comparison to Virgo-Core Roles

### system_user Role

**Gaps:**

- ❌ No molecule/ directory
- ❌ No CI/CD integration (.github/workflows/)
- ❌ No automated testing across distributions
- ❌ No idempotence verification

**Matches:**

- ✅ Simple, focused role scope
- ✅ Uses idempotent modules (user, authorized_key, lineinfile)

**Priority Actions:**

1. **Critical:** Add molecule/default scenario (2-4 hours)
2. **Critical:** Add GitHub Actions CI workflow (2 hours)
3. **Important:** Test on Ubuntu and Debian (1 hour)

### proxmox_access Role

**Gaps:**

- ❌ No molecule/ directory
- ❌ No CI/CD integration
- ❌ No automated testing
- ⚠️  Uses shell module (needs changed_when validation)

**Matches:**

- ✅ Well-structured tasks
- ✅ Uses handlers appropriately

**Priority Actions:**

1. **Critical:** Add molecule testing (2-4 hours)
2. **Critical:** Add changed_when to shell tasks (30 minutes)
3. **Critical:** Add GitHub Actions CI (2 hours)

### proxmox_network Role

**Gaps:**

- ❌ No molecule/ directory
- ❌ No CI/CD integration
- ❌ No automated testing
- ⚠️  Network changes are hard to test (consider check mode tests)

**Matches:**

- ✅ Uses handlers for network reload
- ✅ Conditional task execution

**Priority Actions:**

1. **Critical:** Add molecule testing with network verification (3-4 hours)
2. **Critical:** Add GitHub Actions CI (2 hours)
3. **Important:** Add verification tests for network state (2 hours)

## Summary

**Universal Patterns Identified:**

1. Molecule default scenario with Docker driver
2. Multi-distribution test matrix (RedHat + Debian families)
3. Separate linting and testing jobs
4. GitHub Actions for CI/CD
5. Automated idempotence testing
6. Scheduled testing for dependency health
7. Environment variable configuration for flexibility

**Key Takeaways:**

- Testing infrastructure is not optional for production roles
- Idempotence verification catches most role quality issues
- Multi-distribution testing ensures cross-platform compatibility
- Scheduled tests detect ecosystem changes (package updates, deprecations)
- Separate linting gives faster feedback than combined jobs

**Next Steps:**

Apply these patterns to Virgo-Core roles, starting with system_user (simplest) to establish testing infrastructure template.
