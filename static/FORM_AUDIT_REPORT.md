# Form Audit Report: submit.html (886 lines)

**Goal:** Reduce to only 2 text input fields (website URL + HQ city). Everything else must be select / checkbox / radio / toggle. Auto-detect where possible. Conditional reveal for progressive disclosure.

---

## UX Research Summary: Best Patterns for Compliance Wizards

| Pattern | When to Use | Evidence |
|---|---|---|
| **Rich card-style checkboxes** (already implemented) | Multi-select, "select all that apply" — compliance fields almost always allow multiple answers | ✅ Keep — proven pattern from Carbon Design System, NN/g |
| **Single-select dropdown** | Mutually exclusive options with 5+ choices (company size, revenue band, risk level) | ✅ Keep — standard pattern |
| **Radio button group** | 2–4 mutually exclusive options that benefit from seeing all choices at once | ⬆️ Upgrade from dropdown for DPO/CE marking |
| **Tag input (multi-select + type-to-add)** | Fields like "certifications" or "model types" where user may have uncommon values | ⬆️ New — best pattern per UXPin research for hybrid predefined+custom |
| **Progressive disclosure / conditional reveal** | Hide irrelevant sections (e.g., technical details hidden when AI count = 0) | ⬆️ New — NN/g says this is the #1 pattern for complex forms |
| **Step-by-step wizard** | Long compliance forms (5 sections) | Already partially done — progress bar exists but should become real steps |
| **Auto-detect from website** | Company name, sector, size estimate, location | ⬆️ New — leverage website scan to eliminate text fields |

---

## Full Field Audit: CURRENT → PROPOSED

### Section 1: Company Information

| # | Field Name | CURRENT Type | PROPOSED Type | Proposed Options / Details | Auto-Detectable? | Conditional? |
|---|---|---|---|---|---|---|
| 1 | **Company Name** | `<input type="text">` | ❌ **REMOVED** — auto-detect from website scan | Detect from URL: `<title>`, `<meta og:title>`, domain name | ✅ **Yes** — scrape from website metadata | No |
| 2 | **Company Size** | `<select>` (4 options) | ✅ **KEEP as select** | Startup (1–10), SME (11–250), Mid-sized (251–1000), Enterprise (1000+) | ✅ Partially — employee count may be on About page | No |
| 3 | **Sector / Industry** | `<input type="text">` | ⬆️ **CHANGE to select dropdown** (15 options) | 1. Aerospace & Defense, 2. Agriculture, 3. Automotive, 4. Banking & Finance, 5. Education, 6. Energy & Utilities, 7. Healthcare & Pharma, 8. Insurance, 9. Legal & Compliance, 10. Manufacturing, 11. Media & Entertainment, 12. Public Sector / Government, 13. Retail & E-commerce, 14. Technology & SaaS, 15. Telecom & Transport, 16. Other | ✅ **Yes** — HTML meta keywords, Crunchbase/LinkedIn data | No |
| 4 | **Annual Revenue** | `<input type="text">` | ⬆️ **CHANGE to select dropdown** (7 bands) | < €1M, €1M–€10M, €10M–€50M, €50M–€250M, €250M–€1B, > €1B, Prefer not to say | ❌ Hard to detect | No |
| 5 | **HQ Location** | `<input type="text">` | ✅ **KEEP as text input** (one of 2 allowed text fields) | City + Country format (e.g., "Munich, Germany") | ✅ **Yes** — website contact page, footer, WHOIS | No |
| 6 | **Website URL** | `<input type="url">` | ✅ **KEEP as text input** (one of 2 allowed text fields) | https://example.com | N/A — this is the input itself | No |
| 7 | **Description of AI Activities** | `<textarea>` | ⬆️ **CHANGE to multi-select checkbox** (card-style) | Common AI use cases: Customer support chatbot, Content generation, Fraud detection, Recommendation engine, Image/Video analysis, Document processing, Predictive analytics, Speech/Voice recognition, Autonomous systems, Other (with text note) | ✅ **Yes** — scan website for AI-related keywords | Show if ai_systems_count > 0 |

### Section 2: AI System Details

| # | Field Name | CURRENT Type | PROPOSED Type | Proposed Options / Details | Auto-Detectable? | Conditional? |
|---|---|---|---|---|---|---|
| 8 | **Number of AI Systems in Production** | `<select>` (4 options) | ✅ **KEEP as select** | None yet, 1–3 systems, 4–10 systems, More than 10 | ❌ | 🔑 **Master toggle** — if "None yet", hide sections 3 + 4 entirely |
| 9 | **AI System Names** | `<input type="text">` | ⬆️ **CHANGE to tag input** (multi-select with type-to-add) | Predefined tags: CustomerBot, FraudDetect, RecruitAI, ChatSupport, ContentGen, CodeAssist, DataAnalyzer, VisionAI + user can type custom name | ❌ | Show only if ai_systems_count > 0 |
| 10 | **Purpose of AI Systems** | `<textarea>` | ⬆️ **CHANGE to multi-select checkbox** (card-style) | Customer support automation, Resume/CV screening, Fraud & risk detection, Content moderation, Personalized recommendations, Predictive maintenance, Document classification, Medical diagnosis support, Code generation, Data analytics & reporting, Other | ✅ Partially — infer from site content | Show if ai_systems_count > 0 |
| 11 | **Deployment Type** | `<select>` (4 options) | ✅ **KEEP as select** | Internal use only, Customer-facing, Both internal and external, Third-party AI integrated | ❌ | Show if ai_systems_count > 0 |
| 12 | **Decision Type** | `<select>` (4 options) | ✅ **KEEP as select** | Fully automated decisions, Human-in-the-loop, Decision support only, Recommendation only | ❌ | Show if ai_systems_count > 0 |
| 13 | **Data Sources** | `<textarea>` | ⬆️ **CHANGE to multi-select checkbox** (card-style) | Public datasets, Customer data, Third-party APIs, User-generated content, Web scraping, Proprietary datasets, Purchased data, Open government data, Synthetic data | ❌ | Show if ai_systems_count > 0 |
| 14 | **Risk Self-Assessment** | `<select>` (5 options) | ✅ **KEEP as select** | Minimal risk, Limited risk, High risk, Unacceptable risk, Not sure | ❌ | Show if ai_systems_count > 0 |

### Section 3: Technical Details

| # | Field Name | CURRENT Type | PROPOSED Type | Proposed Options / Details | Auto-Detectable? | Conditional? |
|---|---|---|---|---|---|---|
| 15 | **AI Model Types Used** | `<input type="text">` | ⬆️ **CHANGE to multi-select checkbox** (card-style) | Large Language Models (LLM), Computer Vision (CNN), Regression models, Decision Trees / Random Forest, Reinforcement Learning, GANs, Transformer (non-LLM), Classic ML (SVM, Naive Bayes), Other | ✅ Partially | **Hidden when** ai_systems_count = 0 or risk = minimal |
| 16 | **Training Data Origin** | `<textarea>` | ⬆️ **CHANGE to multi-select checkbox** (same as #13, deduplicate) | Merge with Data Sources (#13) — same options | ❌ | Hidden when ai_systems_count = 0 |
| 17 | **Human Oversight Mechanisms** | `<textarea>` | ⬆️ **CHANGE to multi-select checkbox** (card-style) | Manual review queue, Approval workflow, Exception handling, Audit logging, Human-in-the-loop validation, Periodic sampling, No oversight mechanism | ❌ | Hidden when ai_systems_count = 0 |
| 18 | **Explainability / Interpretability** | `<input type="text">` | ⬆️ **CHANGE to multi-select checkbox** | SHAP, LIME, Attention visualization, Feature importance, Counterfactual explanations, Decision trees, None implemented | ❌ | Hidden when ai_systems_count = 0 |
| 19 | **Data Retention Policy** | `<input type="text">` | ⬆️ **CHANGE to select dropdown** | < 30 days, 30–90 days, 90 days–1 year, 1–3 years, Indefinite / As needed, Not defined, Not applicable | ❌ | Hidden when ai_systems_count = 0 |

### Section 4: High-Risk Categories

| # | Field Name | CURRENT Type | PROPOSED Type | Proposed Options / Details | Auto-Detectable? | Conditional? |
|---|---|---|---|---|---|---|
| 20 | **Biometric ID** | `<input type="checkbox">` | ✅ **KEEP as checkbox** (card-style) | Already correct | ✅ Partially | Hidden when ai_systems_count = 0 |
| 21 | **Critical Infrastructure** | `<input type="checkbox">` | ✅ **KEEP as checkbox** | Already correct | ✅ Partially | Hidden when ai_systems_count = 0 |
| 22 | **Education & Training** | `<input type="checkbox">` | ✅ **KEEP as checkbox** | Already correct | ✅ Partially | Hidden when ai_systems_count = 0 |
| 23 | **Employment & Worker Mgmt** | `<input type="checkbox">` | ✅ **KEEP as checkbox** | Already correct | ✅ Partially | Hidden when ai_systems_count = 0 |
| 24 | **Credit Assessment** | `<input type="checkbox">` | ✅ **KEEP as checkbox** | Already correct | ✅ Partially | Hidden when ai_systems_count = 0 |
| 25 | **Law Enforcement** | `<input type="checkbox">` | ✅ **KEEP as checkbox** | Already correct | ✅ Partially | Hidden when ai_systems_count = 0 |
| 26 | **Migration & Border Control** | `<input type="checkbox">` | ✅ **KEEP as checkbox** | Already correct | ✅ Partially | Hidden when ai_systems_count = 0 |
| 27 | **Administration of Justice** | `<input type="checkbox">` | ✅ **KEEP as checkbox** | Already correct | ✅ Partially | Hidden when ai_systems_count = 0 |
| 28 | **Democratic Processes** | `<input type="checkbox">` | ✅ **KEEP as checkbox** | Already correct | ✅ Partially | Hidden when ai_systems_count = 0 |

### Section 5: Current Compliance Status

| # | Field Name | CURRENT Type | PROPOSED Type | Proposed Options / Details | Auto-Detectable? | Conditional? |
|---|---|---|---|---|---|---|
| 29 | **Existing Compliance Documentation** | `<select>` (3 options) | ✅ **KEEP as select** | Yes, comprehensive; Partially; Not yet | ❌ | No |
| 30 | **DPO Appointed?** | `<select>` (3 options) | ⬆️ **CHANGE to radio group** (3 choices visible at once) | Yes, No, Planned | ❌ | No |
| 31 | **GDPR Compliance Status** | `<select>` (4 options) | ✅ **KEEP as select** | Fully compliant, In progress, Not yet started, Not applicable | ❌ | No |
| 32 | **CE Marking for AI** | `<select>` (3 options) | ⬆️ **CHANGE to radio group** (3 choices) | Yes (obtained), Planned, Not yet | ❌ | Hidden when ai_systems_count = 0 |
| 33 | **Existing Certifications** | `<input type="text">` | ⬆️ **CHANGE to multi-select checkbox + "Other" tag input** | ISO 27001, ISO 42001 (AI Management), SOC 2, SOC 3, HIPAA, PCI DSS, FedRAMP, C5 (Germany), ENS (Spain), BSI Grundschutz, None yet, Other (please specify) | ❌ | Show only if has_documentation ≠ "no" |
| 34 | **Previous Audit History** | `<textarea>` | ⬆️ **CHANGE to yes/no radio + conditional multi-select** | Radio: Yes / No. If Yes → multi-select: GDPR audit, AI audit, Security audit, Internal audit, Third-party audit, Other | ❌ | Show only if has_documentation ≠ "no" |

---

## Summary: Current vs Proposed Counts

| Metric | Current | Proposed |
|---|---|---|
| **Total fields** | 34 | 28 |
| **Text inputs** | 8 (company, sector, revenue, system names, model types, explainability, retention, certifications) | **2** (website URL, HQ city) |
| **Textareas** | 6 (description, ai_purpose, data_sources, training_data, oversight, previous_audits) | **0** |
| **Select dropdowns** | 10 | 8 |
| **Checkboxes (card-style)** | 9 (all in High-Risk section) | 14 (7 new multi-select groups + 9 retained) |
| **Radio groups** | 0 | 2 (DPO, CE Marking) |
| **Tag inputs** | 0 | 1 (AI System Names) |
| **Auto-detectable fields** | 0 | 5 (company name, sector, hq city, ai activities, risk categories) |
| **Conditional/hidden fields** | 0 | 15 (all of sections 3+4 + several section 5 fields) |

---

## Implementation Recommendations (Priority Order)

### 1. Conditional Reveal Logic (+ progressive disclosure)
```
IF ai_systems_count == "None yet" OR "0" THEN
  HIDE: Section 3 (Technical Details) entirely
  HIDE: Section 4 (High-Risk Categories) entirely
  HIDE: CE Marking, Human Oversight, Explainability, Data Retention
  SHOW: minimal compliance fields only
END
```

### 2. New Multi-Select Checkbox Components (7 fields need these)
Use the existing card-style `.checkbox-item` pattern (lines 163–216 of current CSS) — it's already excellent. Just add a "select all" / "clear all" toggle for each group.

### 3. Tag Input for AI System Names
Hybrid component: predefined chips (CustomerBot, FraudDetect, etc.) + a text input to type custom names that turn into chips. Reference: web.dev "building a multi-select component".

### 4. Auto-Detection Strategy
On URL input blur → POST to a `/scan-website` endpoint:
- Extract: company name (og:title / <title> / domain)
- Sector (meta keywords, industry classifiers)
- HQ location (contact page, footer, WHOIS)
- AI keywords presence (flag "has AI content")
- Company size clues (employee count if found)
- Pre-populate fields, let user confirm/edit

### 5. Wizard Steps (optional but recommended)
The current single-page scroll form works for desktop but should become a step-through wizard for mobile:
- Step 1: Company Info (fields 2–6)
- Step 2: AI Details (fields 7–14, conditionally)
- Step 3: Technical (fields 15–19, conditionally)
- Step 4: Risk Categories (fields 20–28, conditionally)
- Step 5: Compliance Status (fields 29–34)

The existing progress bar already supports this pattern.

---

## Files

This report: `/root/ai-compliance-consultant/static/FORM_AUDIT_REPORT.md`
Original file: `/root/ai-compliance-consultant/static/submit.html` (886 lines)
