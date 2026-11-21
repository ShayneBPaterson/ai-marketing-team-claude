# JENGAI Trade Show & Association Event Kit — [Event Name]

- **Status:** DRAFT — awaiting Renata or Shayne approval
- **Event dates:** [MM/DD/YYYY – MM/DD/YYYY] *(verified against `marketing/events/2026/`)*
- **Location & booth:** [City, State] · [Booth # if applicable]
- **Association / audience:** [Starnet Worldwide / FUSE Alliance / AHSG Commercial USA / General commercial specialty contractors]
- **On-site meeting owner:** [Confirm routing — e.g., Renata Doralieva-Paterson]

---

## 1. Booth & Visual Headlines (from `headline-bank.md`)

- **Primary line:** Pipeline Management, Reinvented.
- **Supporting hook:** [Select approved line from `headline-bank.md`]
- **Featured proof point:** [Select alliance-matched approved customer, e.g., Axis Interior Systems for Starnet]

---

## 2. Pre-Show Constant Contact Broadcast (10–14 Days Out)

- **Subject:** [Conference name] — meet JENGAI in [City]
- **Preview text:** [Booth number or meeting invite]
- **CTA:** Schedule a 30-minute discovery call (`https://calendly.com/renata-jengai/jengai-discovery-call`)

```text
[Short, plain invite focused on conference travel — say "traveling to [City] for [Conference]", never "road trip". Skip the full company description if sending exclusively to Starnet, FUSE, or Commercial USA members.]
```

---

## 3. Onsite Welcome Email (Day 1 — Branded MJML)

- Build from `templates/email-constant-contact.mjml`.
- Include booth location, live walkthrough hours, and pre-filled Calendly booking link.

---

## 4. Dedicated Event Landing Page Brief (`/starnet` Pattern)

- **Tracking:** GA4 (`G-EJJJHWZFQQ`) and HubSpot tracking (`51915935`) in `<head>`.
- **Form:** Custom-styled form posting to HubSpot Forms API (`https://api.hsforms.com/submissions/v3/integration/submit/51915935/<form ID>`) with `hubspotutk` cookie, contact fields (`firstname`, `lastname`, `email`), company fields (bids/month, pricing/ERP/takeoff software), and consent checkboxes.
- **Post-submit:** Inline pre-filled Calendly iframe (`renata-jengai/jengai-discovery-call`) plus GA4 `calendly_booking` message listener.

---

## 5. Post-Show Follow-Up Sequence

### Touch 1 (Day +2 — Thank You & Recap)
- **Register:** If 1:1 outreach, follow `gtm-specific-voice.md` Outreach rules (`Dear [First Name],`, no contractions, hyphenated role attribution, closing line before signature).

### Touch 2 (Day +7 — Proof Follow-Up)
- **Angle:** Share one approved finish-trade story matching the prospect's trade (stone, tile, or flooring) and a single direct ask.

### Touch 3 (Day +14 — Direct Close)
- **Angle:** Short direct check-in without re-justifying the full pitch.
