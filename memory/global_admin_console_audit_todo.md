# Global Admin Console Audit — OpenAI

**Org ID:** `org-bYl72BcNqzqcAkh341jS71Xl`  
**Workspace / Project ID:** `proj_QeO1HsgWepb5Sz6LDyWjjcJ8` (`aiproject`)  
**Status:** checklist created, pending execution  
**Source:** creator-provided Global Admin Console audit tree  

---

## Legend

- `[API]` can be read or verified through OpenAI Admin API (`connector_control_plane/adapters/openai.py`).
- `[MANUAL]` requires dashboard/screenshot evidence (`ManualEvidenceAdapter`).
- `[POLICY]` requires a creator decision before any change.

---

## Overview

- [ ] Confirm workspace + organization list under the tenant
- [ ] Confirm navigation to required Tenant settings sections

## Access

### External Access

- [ ] [POLICY] Enable/disable "Sign in with ChatGPT for your organization"
- [ ] [POLICY] Enable/disable "Approved applications"
- [ ] [MANUAL] Review and disable individual apps in Approved applications list

### Domains

- [ ] [MANUAL] Add/remove verified domains matching company domain list
- [ ] [MANUAL] Record any "already in-use" domain conflicts for resolution

### Domain Eligibility and Mapping

- [ ] [MANUAL] Check per-domain mapping status (default often "Not Mapped")
- [ ] [POLICY] Choose mapping scope: All Workspaces/Orgs or subset workspaces
- [ ] [MANUAL] Confirm mapping applies to: SSO, AAC, External Invites, Account Merges
- [ ] [POLICY] Confirm operating principles:
  - ChatGPT SSO = workspace + domain
  - Platform SSO = domain-based (broader impact)

### Automatic Account Creation (AAC)

- [ ] [POLICY] Enable/disable AAC per workspace
- [ ] [POLICY] If domain maps to multiple workspaces, users auto-invited to all
- [ ] [POLICY] If using SCIM, consider leaving AAC disabled
- [ ] [POLICY] If enabling AAC, assess forced-merge of personal accounts into Enterprise

### External Invites

- [ ] [POLICY] Allow or block invites to emails outside verified domains
- [ ] [MANUAL] Confirm external-domain users are not forced to SSO

### Account Merge

- [ ] [POLICY] Define merge logic, especially when AAC / SSO rollout begins

## Single Sign-On (SSO)

- [ ] [MANUAL] Set up 1 SSO connection shared for API orgs + ChatGPT workspaces as needed
- [ ] [MANUAL] Verify SSO "active" conditions:
  - SSO connection enabled on ChatGPT or API
  - Verified domains mapped to correct workspace/org
- [ ] [POLICY] ChatGPT SSO mode: Optional vs Required
- [ ] [POLICY] Platform SSO mode: Optional vs Required
- [ ] [POLICY] Admin Portal SSO mode: Optional vs Required (avoid lock-out)

## Manage Invites

- [ ] [API] Review invite backlog per workspace
- [ ] [POLICY] Confirm invite rules (internal vs external) per workspace

## Users

- [ ] [API] Review user list, roles, and workspace/org access scope

## Credentials

- [ ] [API] Review API keys / service accounts / admin keys
- [ ] [POLICY] Align credentials with internal access policy

## Analytics

### Overview

- [ ] [API] Identify adoption/usage metrics to track

### Leaderboards

- [ ] [POLICY] Enable/disable leaderboards per internal policy

### Credits

- [ ] [API] Track and reconcile credits per workspace
- [ ] [API] ChatGPT consumption by group/user
- [ ] [API] Codex consumption by group/user

## Billing (ChatGPT Enterprise/Edu only)

### Plan

- [ ] [API] Reconcile plan per selected workspace

### Grant Activity

- [ ] [API] Reconcile grant/credit history

### Invoices

- [ ] [MANUAL/API] Reconcile invoices by period

## Usage Limits

### Workspace

- [ ] [API] Set default usage limit (credit) per usage period
- [ ] [POLICY] Choose usage period: Monthly (UTC) or aligned to billing cycle

### Groups

- [ ] [API] Set group overrides / Unlimited if policy allows
- [ ] [API] Remove overrides to inherit correctly

### Users

- [ ] [API] Set user overrides / inspect effective limits

### Pending Requests

- [ ] [MANUAL] Process approve/deny requests for additional usage

## Agents

- [ ] [API] Review agent list per workspace
- [ ] [API] Per agent: Agent ID, connected apps, memory files, schedules
- [ ] [API] Review analytics: unique users, runs over time

## Adding/Removing Workspaces and Organizations

- [ ] [POLICY] Identify need to add/remove workspaces/orgs and list IDs

## Troubleshooting Global Admin Console

### "Unable to login / You are not a global admin"

- [ ] [MANUAL] Confirm Global Admin Console membership (separate from workspace/org membership)
- [ ] [MANUAL] Confirm owner role on each workspace/org to administer
- [ ] [MANUAL] Record Organization ID and Workspace ID for cross-check
