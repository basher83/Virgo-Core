---
description: Execute a task from the task management system
argument-hint: [Task file path]
---

# Execute Task

Implement a task from the task management system using the appropriate tools for your tech stack.

## Core Development Philosophy

When executing tasks, follow these principles to maintain simplicity and focus:

### KISS (Keep It Simple, Silly)

- **Simplicity First**: Choose straightforward solutions over complex ones whenever possible
- **Single Responsibility**: Focus on the specific task objective, avoid scope creep
- **Progressive Enhancement**: Implement basic functionality first, then enhance if needed
- **Avoid Over-Engineering**: Don't add "nice-to-have" features during task execution

### YAGNI (You Aren't Gonna Need It)

- **Essential Only**: Implement only what the task requires, not what might be useful later
- **Avoid Speculation**: Don't add functionality "just in case" - stick to the task requirements
- **MVP Focus**: For learning/validation projects, focus on core functionality that validates the hypothesis
- **Defer Complexity**: Move advanced features to separate tasks if they aren't essential

## Task File

Task file path will be provided as argument, e.g., `path/to/tasks/features/FEAT-001-*.md`

- @$ARGUMENTS

## Task Categories

This repository uses a structured task management system with generic categories that can be adapted to any tech stack:

### Available Categories

- **DEV** - Development setup, tooling, dependencies
- **FEAT** - New features and functionality
- **BUG** - Bug fixes and issue resolution
- **DOCS** - Documentation and guides
- **TEST** - Testing implementation and coverage
- **PERF** - Performance optimizations
- **SEC** - Security improvements
- **REFACTOR** - Code refactoring and improvements

### Task Location

Tasks are organized by category in subdirectories:

- `path/to/tasks/[category]/[PREFIX]-XXX-*.md`
- Example: `path/to/tasks/features/FEAT-001-implement-user-auth.md`

## Project Context

This task system is designed to work with any software project and can be adapted to various tech stacks:

- **Task Tracker**: See `tasks/INDEX.md` for overall progress
- **Template**: Use `tasks/template.md` for creating new tasks
- **Status Tracking**: Tasks use standard status indicators (🔄 Ready, ⏸️ Blocked, 🚧 In Progress, ✅ Complete)

## Tech Stack Validation Patterns

### Web Applications (Next.js/React)

```bash
# Validation (customize for your project)
npm run build          # Build for production
npm run lint           # Check code quality
npm run test           # Run test suite
npm run test:coverage  # Check test coverage

# Development
npm run dev            # Start development server
```

### Databases (PostgreSQL/Supabase)

```bash
# Validation (customize for your database)
psql -f schema.sql     # Apply database schema
dbt build             # Build data models
sqlfluff lint         # Check SQL quality

# Migration
supabase db push      # Apply migrations to Supabase
```

### Infrastructure (Terraform/AWS)

```bash
# Validation (customize for your IaC)
terraform validate    # Validate Terraform configuration
terraform plan        # Preview changes
terraform apply       # Apply infrastructure changes
tflint               # Lint Terraform code

# State management
terraform state list  # List managed resources
```

### Container Workloads (Docker/Kubernetes)

```bash
# Validation (customize for your containers)
docker build -t app .    # Build container image
docker run --rm app      # Test container locally
kubectl apply -f k8s/    # Deploy to Kubernetes

# Testing
docker-compose up        # Test full stack locally
```

## Execution Process

### 1. Load Task

- Read the task file from @$ARGUMENTS
- Identify task category from ID prefix (DEV, FEAT, BUG, DOCS, TEST, PERF, SEC, REFACTOR)
- Review prerequisites and dependencies
- Check task status in `tasks/INDEX.md`

### 2. Pre-flight Checks

**For Development Tasks (DEV):**

- Verify development environment is set up
- Check for required dependencies and tools
- Ensure build system is working
- Review related documentation in `docs/INDEX.md`

**For Feature Tasks (FEAT):**

- Verify core functionality is working
- Check for any blocking dependencies
- Review API documentation and design specs
- Ensure testing framework is available

**For All Task Types:**

- Use TodoWrite tool to create implementation checklist
- Break complex tasks into manageable steps
- Verify access to required systems and permissions

### 3. Implementation

**CRITICAL: No Hardcoded Values**

```yaml
# ❌ NEVER hardcode IPs or hostnames
vars:
  server: "192.168.10.250"  # BAD

# ✅ ALWAYS use variables or discovery
vars:
  server: "{{ vm_ip_address }}"  # GOOD
```

**KISS/YAGNI Implementation Guidelines:**

- **Stick to the Plan**: Follow the task implementation steps exactly, avoid adding extra features
- **Simple Solutions**: Choose the most straightforward approach that meets the requirements
- **No Scope Creep**: If you discover additional functionality needed, create a separate task for it
- **Essential Features Only**: Don't implement "nice-to-have" features during task execution
- **Progressive Enhancement**: Implement basic functionality first, then enhance only if required

**Follow Task Structure:**

1. Complete all implementation steps in order
2. Run validation after each major change
3. Update task status to "🚧 In Progress" in the task file
4. **Resist Temptation**: If you find yourself adding "just one more thing", stop and create a new task instead

### 4. Validation

**Tech Stack Validation:**

Validation commands should be customized for your specific tech stack. Common patterns:

| Tech Stack | Common Validation Commands                        | Notes                                   |
| ---------- | ------------------------------------------------- | --------------------------------------- |
| Web Apps   | `npm run build`, `npm run lint`, `npm run test`   | Check build, quality, and functionality |
| Databases  | `psql -f schema.sql`, `sqlfluff lint`             | Verify schema and SQL quality           |
| IaC        | `terraform validate`, `tflint`, `packer validate` | Infrastructure as Code validation       |
| Containers | `docker build`, `kubectl apply --dry-run`         | Container and deployment validation     |

**KISS/YAGNI Validation Approach:**

- **Focus on Essentials**: Run only the validation commands specified in the task
- **Don't Over-Validate**: Avoid adding extra validation steps unless they're critical
- **Simple Success Criteria**: Verify the task objective is met, not perfection
- **Progressive Testing**: Test basic functionality first, then edge cases if needed

**Common Issues:**

- **Build failures**: Check for missing dependencies or syntax errors
- **Test failures**: Verify test setup and mock data
- **Linting errors**: Follow project coding standards
- **Environment issues**: Ensure proper configuration and credentials
- **Scope creep**: If you find yourself doing more than the task requires, stop and reassess

### 5. Complete Task

1. Verify all success criteria from task file are met
2. Run final validation suite
3. Update task status in:
   - Task file header (Status: ✅ Complete)
   - `tasks/INDEX.md` (update table and percentage)
4. Check if any dependent tasks are now unblocked
5. Report completion with summary of changes

### KISS/YAGNI Decision Framework

**During Implementation, Ask Yourself:**

1. **Is this part of the original task?**

   - If no → Stop and create a new task for additional work
   - If yes → Proceed with simplest possible solution

2. **Can I achieve this with existing tools?**

   - If yes → Use them (don't reinvent the wheel)
   - If no → Choose the simplest tool that meets the need

3. **What is the minimal viable implementation?**

   - Focus on core functionality that meets the success criteria
   - Add complexity only if the basic solution fails
   - Prefer straightforward solutions over elegant complex ones

4. **Should this be a separate task?**
   - If it will take more than 30 minutes → Create a new task
   - If it's not in the original scope → Create a new task
   - If it's a "nice-to-have" → Definitely create a new task

## Directory Structure

```text
.
├── [project-root]/                        # Your project root directory
│   └── tasks/                     # Task management system (customizable location)
│       ├── INDEX.md                       # Active task tracker and progress dashboard
│       ├── template.md                    # Task file template
│       ├── [categories]/                  # Task category directories (DEV, FEAT, BUG, etc.)
│       │   ├── [PREFIX]-XXX-*.md         # Individual task files
│       │   └── [other-tasks]/            # Additional task files
│       └── README.md                      # Task system documentation
├── [source-code]/                         # Your source code (structure varies by tech stack)
├── [config-files]/                        # Configuration files (varies by project type)
├── [documentation]/                       # Project documentation
└── [other-directories]/                   # Project-specific directories
```

## Quick Reference

### Status Indicators

- 🔄 Ready - Can start immediately
- ⏸️ Blocked - Waiting on dependencies
- 🚧 In Progress - Currently active
- ✅ Complete - Finished and validated
- ❌ Failed - Encountered issues

### Priority Levels

- P0 - Critical path, blocks other work
- P1 - Important functionality
- P2 - Nice to have, optimization

### Task ID Format

- DEV-XXX - Development setup and tooling tasks
- FEAT-XXX - New features and functionality
- BUG-XXX - Bug fixes and issue resolution
- DOCS-XXX - Documentation and guides
- TEST-XXX - Testing implementation and coverage
- PERF-XXX - Performance optimizations
- SEC-XXX - Security improvements
- REFACTOR-XXX - Code refactoring and improvements

## Notes

- Always use the TodoWrite tool to track your implementation progress
- Update task status immediately when starting/completing work
- If blocked, document the reason in the task file
- Reference the task file throughout implementation to ensure all requirements are met

## KISS/YAGNI Implementation Reminders

- **Stick to the task**: Focus only on what's specified in the task file
- **Simple solutions**: Choose the most straightforward approach that works
- **No scope creep**: If you discover additional work needed, create separate tasks
- **Essential functionality**: Don't implement features "just in case"
- **Progressive enhancement**: Start simple, enhance only if required by success criteria
- **Use existing tools**: Don't reinvent the wheel - leverage existing libraries and frameworks
- **MVP mindset**: For learning/validation projects, focus on core hypothesis validation

**If you find yourself thinking "this would be nice to add" or "I should make this more robust" - STOP and create a separate task instead.**
