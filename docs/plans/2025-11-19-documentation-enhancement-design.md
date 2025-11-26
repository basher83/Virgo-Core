# Documentation Enhancement Design

**Date**: 2025-11-19
**Status**: Validated
**Scope**: Solid Foundation (16-24 hours)
**Approach**: Fix-then-build with hybrid content creation

## Executive Summary

This design transforms the Virgo-Core Mintlify documentation site from a landing page with broken links into complete
getting-started through advanced reference documentation. The approach preserves the existing documentation structure
while fixing path issues, creating tutorials, and enhancing role documentation with visual elements and integration
examples.

## Design Decisions

### Key Choices Made

**File Organization**: Preserve subdirectory structure (core/, design/, roles/, getting-started/)

- Rationale: Maintains logical organization established in recent documentation reorganization
- Implementation: Update docs.json paths to reference subdirectories

**Scope**: Solid foundation (16-24 hours) focusing on immediate value

- Phase 1: Fix 404 errors (2-4 hours)
- Phase 2: Create getting-started content (6-10 hours)
- Phase 3: Enhance role documentation (8-10 hours)

**Content Creation**: Hybrid approach

- AI drafts procedural/tutorial content
- Collaborative troubleshooting sections leveraging real-world experience
- Enhanced role docs building on existing excellent READMEs

**Archived Documentation**: Extract insights, remove references

- Pull testing metrics into role docs ("15 bugs found and fixed")
- Incorporate migration lessons into ansible-philosophy.md
- Remove archived doc links from navigation

**Role Documentation**: Enhanced versions

- Start with existing 99-580 line READMEs
- Add architecture diagrams and workflow visualizations
- Include integration examples and cross-references
- Show battle-tested metrics from production validation

**Implementation Priority**: Fix-then-build sequence

1. Fix docs.json paths (immediate value from existing content)
2. Create getting-started tutorials (unblock new users)
3. Enhance role documentation (comprehensive reference)

## Three-Phase Implementation

### Phase 1: Foundation Fix (2-4 hours)

**Objective**: Fix all 404 errors to make existing documentation accessible.

**Changes to docs.json**:

Current broken paths → Fixed paths:

- `documentation/goals` → `documentation/core/goals`
- `documentation/infrastructure` → `documentation/core/infrastructure`
- `documentation/ansible-philosophy` → `documentation/design/ansible-philosophy`
- `documentation/ansible-role-design` → `documentation/design/ansible-role-design`
- `documentation/ansible-playbook-design` → `documentation/design/ansible-playbook-design`
- `documentation/netbox-powerdns` → `documentation/core/netbox-powerdns`
- `documentation/references` → `documentation/core/references`

Remove archived document references:

- `documentation/ansible-migration-plan` (archived)
- `documentation/ansible-migration-completion` (archived)
- `documentation/testing-validation-results` (archived)

**Changes to index.mdx**:

Remove links to archived docs in Quick Links section, replace with:

- Links to active documentation
- Link to roadmap (next-features-2025-11.md)

**Insight Extraction**:

Before removing archived doc references, extract key information:

- Testing validation results → Add "Battle Tested" callouts to role docs
  - "15 bugs found and fixed during comprehensive testing"
  - "Perfect idempotency validated across 3-node Matrix cluster"
- Migration completion metrics → Enhance ansible-philosophy.md with proven approach
- Migration plan insights → Already incorporated into design docs

**Validation**:

Test all navigation links on live site after deployment.

**Impact**: Site transforms from "homepage only" to "7 reference docs accessible"

### Phase 2: Getting Started Content (6-10 hours)

**Objective**: Create tutorials targeting the "New Infrastructure Engineer" persona.

**Content Strategy**: Hybrid approach

- AI drafts: Command sequences, procedures, expected outputs, setup instructions
- Collaborative: Troubleshooting sections, real-world gotchas, error messages

**Four New Guides**:

#### 1. prerequisites.md (2 hours)

**Content**:

- Hardware requirements checklist (extract from infrastructure.md)
  - 3+ nodes with CPU/RAM/storage specs
  - Network requirements (management + CEPH networks)
  - Jumbo frame support for switches
- Software prerequisites with version validation
  - Proxmox VE 9.x installation check
  - SSH access verification
  - Development machine tools (mise, uv)
- Infisical setup overview
- Validation section with test commands for each requirement

**Format**:

- Checkbox-style requirements list
- Validation commands with expected outputs
- "Why this matters" explanations for key requirements

#### 2. installation.md (2 hours)

**Content**:

- Clone repository
- Install mise: `curl https://mise.run | sh`
- Setup dependencies: `mise run setup`
- Configure Infisical CLI and authenticate
- Validate installation with test commands

**Format**:

- Step-by-step numbered instructions
- Expected output for each command
- Troubleshooting callouts for common issues
- Success criteria at the end

#### 3. first-deployment.md (3-4 hours)

**Content**: "Zero to Cluster in 60 Minutes" tutorial

**Structure**:

- Prerequisites checklist reference
- Five deployment phases with time estimates:
  1. Inventory Configuration (10 min)
  2. Network Setup (15 min)
  3. Cluster Formation (10 min)
  4. CEPH Deployment (15 min)
  5. Verification (10 min)

**Each Phase Includes**:

- Estimated completion time
- "What will happen" explanation
- Commands to execute
- Expected output examples
- Checkpoint validation
- Links to relevant role docs for deep dives

**Special Features**:

- "What happens next" warnings before destructive operations
- Progress indicators ("You should see X in the output")
- Common gotchas specific to each phase
- Rollback guidance if something fails

#### 4. troubleshooting-basics.md (2-3 hours, collaborative)

**Content**:

- Symptom-based decision tree
- Common first-deployment issues:
  - SSH connection problems
  - Infisical authentication failures
  - Network configuration errors
  - Ansible inventory issues
  - CEPH OSD creation failures
- For each issue:
  - Symptom description
  - Diagnosis procedure
  - Solution steps
  - Prevention guidance

**Collaborative Section**:
This is where your real-world experience is critical. We'll work together to identify:

- Actual error messages you've encountered
- Hardware-specific issues
- Timing and performance gotchas
- Recovery procedures you've used

**Format**:

- Decision tree at top for quick navigation
- Detailed troubleshooting procedures
- Copy-paste ready diagnostic commands
- Links to relevant role documentation

### Phase 3: Enhanced Role Documentation (8-10 hours)

**Objective**: Transform existing role READMEs into enhanced Mintlify pages with visuals and integration examples.

**Enhancement Strategy**:

Start with existing role READMEs (99-580 lines each), then add:

**Visual Elements**:

- Architecture diagrams showing role dependencies
- Workflow diagrams (sequence of tasks)
- Component interaction diagrams
- Network topology (for proxmox_network)

**Integration Examples**:

- How roles work together (e.g., system_user + proxmox_access)
- Playbook composition patterns
- Multi-role workflows with execution order

**Cross-References**:

- "See also" sections linking related roles
- Links to troubleshooting sections
- References to architecture docs

**Battle-Tested Metrics**:

- Validation data from testing-validation-results
- Real deployment metrics from Matrix cluster
- "15 bugs found and fixed" callouts

**Six Enhanced Role Pages** (~1.5 hours each):

#### 1. system_user.md

**Base**: Existing 300+ line README

**Enhancements**:

- User management workflow diagram
- Infisical integration example for SSH keys
- Sudo configuration patterns
- Integration with proxmox_access for automation users

#### 2. proxmox_access.md

**Base**: Existing 580+ line README (most comprehensive)

**Enhancements**:

- Privilege hierarchy diagram
- Terraform token workflow (environment export feature)
- Role composition examples
- ACL permission patterns

#### 3. proxmox_network.md

**Base**: Existing 480+ line README

**Enhancements**:

- Network topology diagram for Matrix cluster
- VLAN configuration examples
- MTU and jumbo frame setup
- Bridge architecture visualization

#### 4. proxmox_repository.md

**Base**: Existing 99 line README (shortest, most opportunity)

**Enhancements**:

- Repository selection decision tree
- Upgrade workflow diagram
- Enterprise vs community repository comparison
- CEPH repository integration

#### 5. proxmox_cluster.md

**Base**: Existing 156 line README

**Enhancements**:

- Cluster formation sequence diagram
- Corosync architecture
- Node addition workflow
- Quorum management

#### 6. proxmox_ceph.md

**Base**: Existing 290 line README

**Enhancements**:

- CEPH architecture diagram (monitors, managers, OSDs, pools)
- OSD creation workflow (automated vs ProxSpray)
- Pool configuration examples
- Performance considerations
- Bug #13 and #14 fixes highlighted

**Mintlify Formatting**:

- Callouts for warnings, tips, notes
- Code tabs for multi-step examples
- Cards for navigation to related topics
- Accordion sections for advanced configuration

## File Organization

**Directory Structure**:

```text
documentation/
├── getting-started/          # NEW - Phase 2 content
│   ├── prerequisites.md
│   ├── installation.md
│   ├── first-deployment.md
│   └── troubleshooting-basics.md
├── roles/                    # NEW - Phase 3 enhanced docs
│   ├── system_user.md
│   ├── proxmox_access.md
│   ├── proxmox_network.md
│   ├── proxmox_repository.md
│   ├── proxmox_cluster.md
│   └── proxmox_ceph.md
├── core/                     # EXISTING - unchanged
│   ├── goals.md
│   ├── infrastructure.md
│   ├── netbox-powerdns.md
│   └── references.md
├── design/                   # EXISTING - enhanced with insights
│   ├── ansible-philosophy.md
│   ├── ansible-role-design.md
│   └── ansible-playbook-design.md
├── brainstorming/            # EXISTING - not published
└── archive/                  # EXISTING - not published
```

## Updated Navigation Structure

**docs.json navigation**:

```json
{
  "navigation": {
    "tabs": [
      {
        "tab": "Documentation",
        "groups": [
          {
            "group": "Getting Started",
            "pages": [
              "index",
              "documentation/getting-started/prerequisites",
              "documentation/getting-started/installation",
              "documentation/getting-started/first-deployment",
              "documentation/getting-started/troubleshooting-basics",
              "documentation/core/goals",
              "documentation/core/infrastructure"
            ]
          },
          {
            "group": "Ansible Roles",
            "pages": [
              "documentation/roles/system_user",
              "documentation/roles/proxmox_access",
              "documentation/roles/proxmox_network",
              "documentation/roles/proxmox_repository",
              "documentation/roles/proxmox_cluster",
              "documentation/roles/proxmox_ceph"
            ]
          },
          {
            "group": "Ansible Architecture",
            "pages": [
              "documentation/design/ansible-philosophy",
              "documentation/design/ansible-role-design",
              "documentation/design/ansible-playbook-design"
            ]
          },
          {
            "group": "Integration",
            "pages": [
              "documentation/core/netbox-powerdns",
              "documentation/core/references"
            ]
          }
        ]
      }
    ]
  }
}
```

**Navigation Improvements**:

- Clear separation: Getting Started → Roles → Architecture → Integration
- Logical progression from tutorial to reference to design
- Removed archived document references
- Added new "Ansible Roles" group for discoverability

## Documentation Quality Standards

**Every guide must include**:

- Prerequisites section with validation commands
- Estimated time to complete
- Expected outcomes with examples
- Verification steps to confirm success
- Troubleshooting section for common issues
- Next steps to guide user journey

**Code examples must include**:

- Complete, copy-paste ready commands
- Expected output (or note if output varies)
- Explanation of what's happening
- Error handling examples where relevant
- Links to relevant documentation

**Troubleshooting sections must include**:

- Symptom description
- Diagnosis procedure
- Solution steps
- Prevention guidance
- Related issues

**Mintlify Formatting Standards**:

- Use callouts (`<Note>`, `<Warning>`, `<Tip>`) for important information
- Use code tabs for multi-step commands or alternatives
- Use cards for navigation between related topics
- Use accordion sections for advanced/optional content
- Apply Elements of Style principles for clarity

## Success Metrics

**Phase 1 Complete**:

- ✅ All navigation links work (0 404 errors)
- ✅ 7 existing high-quality docs accessible
- ✅ Index.mdx updated with active doc links
- ✅ Insights extracted from archived docs

**Phase 2 Complete**:

- ✅ New user can deploy cluster following first-deployment.md tutorial
- ✅ Prerequisites validated before starting (prerequisites.md)
- ✅ Development environment setup documented (installation.md)
- ✅ Common issues documented with solutions (troubleshooting-basics.md)
- ✅ Clear user journey from "never used" to "cluster deployed"

**Phase 3 Complete**:

- ✅ All 6 roles have enhanced documentation
- ✅ Visual diagrams aid understanding
- ✅ Cross-references enable discovery
- ✅ Integration examples show how roles work together
- ✅ Battle-tested metrics demonstrate production readiness

**Overall Transformation**:

- **Before**: Landing page + 10 broken links
- **After**: Complete getting-started through advanced reference
- **Impact**: New users onboard independently, operators troubleshoot with guides, developers reference complete role documentation

## Implementation Sequence

**Week 1**:

- Day 1: Phase 1 - Fix docs.json and index.mdx (2-4 hours)
- Day 2-3: Phase 2 - Create getting-started content (6-10 hours)

**Week 2**:

- Day 1-3: Phase 3 - Enhance role documentation (8-10 hours)
- Day 4: Final review, polish with Elements of Style, deploy

**Total Effort**: 16-24 hours across 2 weeks

## Next Steps

1. **Apply Elements of Style** to this design document
2. **Commit design** to repository
3. **Set up implementation workspace** with superpowers:using-git-worktrees
4. **Create detailed implementation plan** with superpowers:writing-plans
5. **Execute Phase 1** - Fix docs.json
6. **Execute Phase 2** - Create getting-started content
7. **Execute Phase 3** - Enhance role documentation

## Design Validation

Collaborative brainstorming validated this design with these key decisions:

- ✅ Preserve subdirectory structure for organization
- ✅ Solid foundation scope (16-24 hours) for achievable completion
- ✅ Hybrid content approach leveraging AI drafting + real-world experience
- ✅ Enhanced role docs building on existing foundation
- ✅ Extract insights from archived docs, remove references
- ✅ Fix-then-build implementation priority

**Status**: Ready for implementation
