# Zapier Field Mapping Reference — CR Form > SF Zap
**Date:** September 10, 2026  
**Status:** Staging-ready; Zapier owner action required

---

## Background

The `CR Form > SF` Zap currently maps only the **Estates form schema** 
(from `estates.truelegacyhomes.com`). The **main-site form** 
(`www.truelegacyhomes.com/schedule-consult/` and `/contact/`) uses a different 
field naming convention in CallRail. This causes the main-site Salesforce leads 
to arrive with blank phone, email, ZIP, county, source, and landing-page fields.

**Do not change the existing Estates mapping.** Add a separate conditional path for main-site submissions.

---

## How to identify the path

Add a Zapier **Filter / Path** step immediately after the CallRail trigger, split on:

| Condition | Value |
|-----------|-------|
| `Form Data Form Type` **is** | `schedule-consult` |
| **OR** Form URL **contains** | `truelegacyhomes.com/schedule-consult` |
| **OR** Form URL **contains** | `truelegacyhomes.com/contact` |

Everything else → existing Estates path (unchanged).

---

## Main-site path: CallRail field → Salesforce field mapping

| Salesforce Field | CallRail Field | Notes |
|-----------------|---------------|-------|
| `FirstName` | `Form Data First Name` | |
| `LastName` | `Form Data Last Name` | Required — stop run if absent |
| `Phone` | `Form Data Phone Number` → fallback `Customer Phone Number` | Normalize to E.164 if possible |
| `Email` | `Form Data Email` | Stop run if absent or no `@` character |
| `PostalCode` | `Form Data Zip Code` | |
| `Cnty__c` | `Form Data Property County` | Values: San Diego / Orange County / Los Angeles |
| `LeadSource` | *(hardcoded)* | `CallRail` |
| `Utm_Source__c` | `CallRail Source` → fallback `Form Data Lead Source` | |
| `Utm_Medium__c` | `CallRail Medium` | |
| `Utm_Campaign__c` | `CallRail Campaign` | Only when present |
| `Keywords__c` | `CallRail Keywords` | Only when present |
| `GCLID__c` | `Form Data Gclid` OR `Google Click ID` | Only when present (new field as of Sep 10) |
| `Landing_Page_URL__c` | `Form Data Landing Page` | Capped at 255 chars; as of Sep 10 this is the full URL |
| `I_need__c` | `Form Data Service` (normalized — see below) | |

---

## `I_need__c` normalization — DO NOT hardcode "Running An Estate Sale"

The form sends one of three values from the `service` field. Map each to the 
Salesforce-approved picklist value:

| Form value (from CallRail `Form Data Service`) | Salesforce `I_need__c` value |
|-----------------------------------------------|------------------------------|
| `Estate Sale` | `Running An Estate Sale` |
| `Care Placement` | *(confirm exact SF picklist label — e.g. "Care Placement" or "Senior Care Placement")* |
| `Cash Home Offer` | *(confirm exact SF picklist label — e.g. "Cash Home Offer" or "Selling My Home")* |

⚠️ The `Care Placement` and `Cash Home Offer` SF values **must be confirmed against 
the live Salesforce `I_need__c` picklist** before going live. Do not use a text 
value that doesn't exist in the picklist — Salesforce will reject it silently.

---

## Required-field gate (stop / hold behavior)

If either of these is missing, **stop the Zap run visibly** (do not create a hollow lead):

- Last name
- Phone AND email both absent (at least one must be present)

A Zap "Error" state is preferable to a Salesforce lead with no contact information.

---

## Duplicate call handling (separate Zap: CR Calls > SF)

Five errors logged September 10 — all confirmed Salesforce duplicate rejections, not missing leads:

- 1× returning OC caller
- 2× linked tracking-number legs for same postcard caller
- 1× returning GBP caller
- 1× known Justin test caller

**Preferred behavior (implement after main-site form fix):**

1. Normalize caller phone (strip non-digits, prepend +1 if 10 digits)
2. Query Salesforce: find existing Lead by `Phone`
3. If found → preserve original attribution; optionally log the call; end Zap successfully (no new lead)
4. If not found → create new lead as today

---

## Acceptance test checklist

### Main-site positive test
- [ ] Open `https://www.truelegacyhomes.com/schedule-consult/?utm_source=google&utm_medium=cpc&utm_campaign=test&gclid=TEST_GCLID_001`
- [ ] Submit: synthetic first/last name, unique test phone, valid email, ZIP, county = Orange County, service = Estate Sale
- [ ] Confirm CallRail form event contains all submitted fields + `gclid`
- [ ] Confirm one successful Zapier run on the main-site path
- [ ] In Zapier Salesforce step "Data in" — verify: phone, email, ZIP, county, service, source, medium, campaign, gclid, landing page all populated
- [ ] In Salesforce lead record — verify same fields are stored
- [ ] Record: CallRail event ID / Zapier run ID / Salesforce Lead ID

### Main-site negative test
- [ ] Enter email without `@` character
- [ ] Confirm browser blocks submission (error message appears inline)
- [ ] Confirm no CallRail event, Zapier run, or Salesforce lead created

### Estates regression test
- [ ] Submit one labeled synthetic lead through an Estates landing page
- [ ] Confirm phone and attribution fields still map correctly to Salesforce
- [ ] Confirm this run took the Estates path (not main-site path) in Zapier

---

## What is NOT in scope

- No change to Google Ads
- No change to public Estates landing pages
- No Salesforce schema, flow, duplicate-rule, or historical-record changes without separate review
- No replay or deletion of September 10 production records

---

## Form field names in HTML (for CallRail reference)

These are the HTML `name` attributes CallRail reads from 
`www.truelegacyhomes.com/schedule-consult/`:

| HTML `name` attr | CallRail label | Value example |
|-----------------|---------------|---------------|
| `first_name` | Form Data First Name | Jane |
| `last_name` | Form Data Last Name | Smith |
| `email` | Form Data Email | jane@example.com |
| `phone_number` | Form Data Phone Number | (619) 555-1234 |
| `service` | Form Data Service | Estate Sale |
| `property_county` | Form Data Property County | Orange County |
| `zip_code` | Form Data Zip Code | 90630 |
| `form_type` | Form Data Form Type | schedule-consult |
| `utm_source` | Form Data Utm Source | google |
| `utm_medium` | Form Data Utm Medium | cpc |
| `utm_campaign` | Form Data Utm Campaign | spring-2026 |
| `lead_source` | Form Data Lead Source | Paid |
| `gclid` | Form Data Gclid | *(new — as of Sep 10, 2026 push)* |
| `landing_page` | Form Data Landing Page | `https://www.truelegacyhomes.com/schedule-consult/` |
