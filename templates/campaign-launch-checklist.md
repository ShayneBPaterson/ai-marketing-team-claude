# JENGAI Campaign & Feature Launch Checklist — [Launch Name]

- **Owner:** Renata Doralieva-Paterson (CMO) · Support: Berwyn San Juan
- **Sales handoff contact:** Shayne Paterson (Sales)
- **Target date:** [MM/DD/YYYY]
- **Launch type:** [Feature release / Owner AI Workshop / Association event / Proof campaign]

---

## T-3 to T-2 Weeks: Foundation & Truth Check

- [ ] Confirm feature scope, naming, and account gating against `product-state.md` (no unshipped claims)
- [ ] Confirm positioning lock (pricing and operations platform, never estimating or takeoff tool)
- [ ] Select approved proof points from `marketing/outputs/messaging/approved-messaging.md`
- [ ] Draft landing page updates or dedicated page brief for `jengai-com/public-website`
- [ ] Draft Constant Contact emails (copy + branded MJML via `templates/email-constant-contact.mjml`)
- [ ] Draft weekly LinkedIn announcement post (Shayne founder voice or JENGAI company voice)

## T-1 Week: QA, Tracking & Sales Enablement

- [ ] Run `python3 scripts/validate_copy.py <drafts> --public --register external` (0 errors)
- [ ] Complete `core-brain/how-we-work/ai-conventions/pre-publish-checklist.md`
- [ ] Verify GA4 (`G-EJJJHWZFQQ`), HubSpot tracking (`51915935`), HubSpot form fields, and pre-filled Calendly embeds
- [ ] Brief Sales (Shayne, Zhai, Aica) with 1-page talking points and approved objection responses
- [ ] Export any PDF/visual deliverables directly to SharePoint (`AI_Marketing_Outputs/...`) with `.sharepoint.md` stubs
- [ ] Obtain explicit Renata / Shayne approval on all outbound drafts (notify via Microsoft Teams)

## Launch Week: Execution

- [ ] Publish approved website changes to `jengai.com`
- [ ] Send approved Constant Contact email
- [ ] Publish approved weekly LinkedIn post (Tue–Thu, 8:00–11:00 AM ET)
- [ ] Share live links in Microsoft Teams so Sales and CS can amplify

## T+1 to T+2 Weeks: Measurement & Follow-Through

- [ ] Pull Constant Contact open/click rates, HubSpot form submissions, and Calendly bookings (`hubspot-data` / `salesforce-data`)
- [ ] Log learnings in `marketing/status.md` and capture any new customer quotes for `marketing-case-study`
- [ ] Update quarterly content calendar with follow-up angles
