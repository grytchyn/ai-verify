# System prompt for EU AI Act compliance analysis — bilingual EN/DE
# Language is injected by build_enhanced_prompt based on submission.lang

SYSTEM_PROMPT_EN = """You are an expert on the EU AI Act. High-risk AI systems include: biometric identification, critical infrastructure, employment, credit scoring, education. Key requirements: risk management, data governance, transparency, human oversight, logging, conformity assessment.
Respond strictly with facts from the provided context only, using markdown format.

Your response MUST be in ENGLISH. Use technical terms in English only."""

SYSTEM_PROMPT_DE = """Du bist ein Experte für den EU AI Act. Hochrisiko-KI-Systeme umfassen: biometrische Identifizierung, kritische Infrastruktur, Beschäftigung, Bonitätsbewertung, Bildung. Wichtige Anforderungen: Risikomanagement, Datenverwaltung, Transparenz, menschliche Aufsicht, Protokollierung, Konformitätsbewertung.
Antworte ausschließlich mit Fakten aus dem bereitgestellten Kontext im Markdown-Format.

Deine Antwort MUSS auf DEUTSCH erfolgen. Fachbegriffe dürfen auf Englisch bleiben."""

SYSTEM_PROMPT = SYSTEM_PROMPT_EN  # default fallback

def build_company_profile(submission, lang: str = "en") -> str:
    """Build structured company profile from submission data.
    lang: 'en' or 'de' — used for section labels."""
    import json
    
    labels = {
        "en": {"company": "Company", "website": "Website", "email": "Email", "size": "Company Size",
               "sector": "Sector", "employees": "Employees", "revenue": "Annual Revenue",
               "hq": "HQ Location", "not_specified": "Not specified", "ai_details": "AI System Details",
               "ai_count": "AI Systems in Production", "ai_names": "System Names",
               "ai_purpose": "AI Purpose", "deployment": "Deployment Type",
               "data_sources": "Data Sources", "decision_type": "Decision Type",
               "risk_self": "Risk Self-Assessment", "tech_details": "Technical Details",
               "model_types": "Model Types", "training_data": "Training Data Origin",
               "human_oversight": "Human Oversight", "explainability": "Explainability / Interpretability",
               "data_retention": "Data Retention Policy", "compliance_status": "Compliance Status",
               "documentation": "Documentation", "dpo": "DPO Appointed",
               "gdpr": "GDPR Compliant", "certifications": "Certifications",
               "audits": "Previous Audits", "ce_marking": "CE Marking",
               "high_risk": "High-Risk Categories (selected)", "none_selected": "None selected",
               "additional_info": "Additional Information", "ai_activity": "AI Activity Description",
               "yes": "Yes", "no": "No"},
        "de": {"company": "Unternehmen", "website": "Webseite", "email": "E-Mail", "size": "Unternehmensgröße",
               "sector": "Branche", "employees": "Mitarbeiter", "revenue": "Jahresumsatz",
               "hq": "Hauptsitz", "not_specified": "Nicht angegeben", "ai_details": "KI-System-Details",
               "ai_count": "KI-Systeme in Produktion", "ai_names": "Systemnamen",
               "ai_purpose": "KI-Zweck", "deployment": "Bereitstellungstyp",
               "data_sources": "Datenquellen", "decision_type": "Entscheidungstyp",
               "risk_self": "Risiko-Selbsteinschätzung", "tech_details": "Technische Details",
               "model_types": "Modelltypen", "training_data": "Trainingsdaten-Herkunft",
               "human_oversight": "Menschliche Aufsicht", "explainability": "Erklärbarkeit / Interpretierbarkeit",
               "data_retention": "Datenaufbewahrungsrichtlinie", "compliance_status": "Compliance-Status",
               "documentation": "Dokumentation", "dpo": "DSB ernannt",
               "gdpr": "DSGVO-konform", "certifications": "Zertifizierungen",
               "audits": "Vorherige Audits", "ce_marking": "CE-Kennzeichnung",
               "high_risk": "Hochrisiko-Kategorien (ausgewählt)", "none_selected": "Keine ausgewählt",
               "additional_info": "Zusätzliche Informationen", "ai_activity": "KI-Aktivitätsbeschreibung",
               "yes": "Ja", "no": "Nein"}
    }
    L = labels.get(lang, labels["en"])
    ns = L["not_specified"]
    
    profile = []
    profile.append(f"**{L['company']}:** {submission.company or ns}")
    profile.append(f"**{L['website']}:** {submission.url or ns}")
    profile.append(f"**{L['email']}:** {submission.email or ns}")
    profile.append(f"**{L['size']}:** {submission.company_size or ns}")
    profile.append(f"**{L['sector']}:** {submission.sector or ns}")
    profile.append(f"**{L['employees']}:** {submission.employees or ns}")
    profile.append(f"**{L['revenue']}:** {submission.annual_revenue or ns}")
    profile.append(f"**{L['hq']}:** {submission.hq_location or ns}")
    profile.append(f"### {L['ai_details']}")
    profile.append(f"**{L['ai_count']}:** {submission.ai_systems_count or ns}")
    profile.append(f"**{L['ai_names']}:** {submission.ai_system_names or ns}")
    profile.append(f"**{L['ai_purpose']}:** {submission.ai_purpose or ns}")
    profile.append(f"**{L['deployment']}:** {submission.deployment_type or ns}")
    profile.append(f"**{L['data_sources']}:** {submission.data_sources or ns}")
    profile.append(f"**{L['decision_type']}:** {submission.decision_type or ns}")
    profile.append(f"**{L['risk_self']}:** {submission.risk_self_assessment or ns}")

    profile.append("")
    profile.append(f"### {L['tech_details']}")
    profile.append(f"**{L['model_types']}:** {submission.model_types or ns}")
    profile.append(f"**{L['training_data']}:** {submission.training_data_origin or ns}")
    profile.append(f"**{L['human_oversight']}:** {submission.human_oversight or ns}")
    profile.append(f"**{L['explainability']}:** {submission.explainability or ns}")
    profile.append(f"**{L['data_retention']}:** {submission.data_retention or ns}")

    profile.append("")
    profile.append(f"### {L['compliance_status']}")
    profile.append(f"**{L['documentation']}:** {submission.has_documentation or ns}")
    profile.append(f"**{L['dpo']}:** {submission.dpo_appointed or ns}")
    profile.append(f"**{L['gdpr']}:** {submission.gdpr_compliant or ns}")
    profile.append(f"**{L['certifications']}:** {submission.existing_certifications or ns}")
    profile.append(f"**{L['audits']}:** {submission.previous_audits or ns}")
    profile.append(f"**{L['ce_marking']}:** {submission.ce_marking or ns}")

    profile.append("")
    profile.append(f"### {L['high_risk']}")
    active = submission.risk_categories_active() if hasattr(submission, 'risk_categories_active') else []
    if active:
        for cat in active:
            profile.append(f"- [x] {cat}")
    else:
        profile.append(f"- {L['none_selected']}")

    # Additional info JSON
    if submission.additional_info:
        try:
            extra = json.loads(submission.additional_info)
            if extra:
                profile.append("")
                profile.append(f"### {L['additional_info']}")
                for k, v in extra.items():
                    profile.append(f"- **{k}:** {v}")
        except:
            pass

    profile.append("")
    if submission.description:
        profile.append(f"**{L['ai_activity']}:** {submission.description}")

    return "\n".join(profile)

def build_user_prompt(company: str, url: str, description: str, search_text: str, lang: str = "en") -> str:
    """Compatibility: build user prompt from simple fields."""
    if not search_text:
        search_text = "No open-source data found." if lang == "en" else "Keine öffentlichen Daten gefunden."
    sections_en = "\n".join([
        "Based on this data, determine:",
        "1) Does the product fall under a high-risk category? (Yes/No/Insufficient data).",
        "2) Which AI Act requirements are likely applicable (list).",
        "3) Identified gaps (what is missing for compliance).",
        "4) Specific recommendations (documents, processes, checkpoints).",
        "Format the answer in markdown with sections: **Conclusion**, **Risk Category**, **Applicable Requirements**, **Gaps**, **Recommendations**, **Sources**.",
        "If data is insufficient, indicate what information is needed."
    ])
    sections_de = "\n".join([
        "Bestimme auf Basis dieser Daten:",
        "1) Fällt das Produkt unter eine Hochrisiko-Kategorie? (Ja/Nein/Unzureichende Daten).",
        "2) Welche AI Act-Anforderungen sind wahrscheinlich anwendbar (Liste).",
        "3) Identifizierte Lücken (was fehlt zur Konformität).",
        "4) Konkrete Empfehlungen (Dokumente, Prozesse, Kontrollpunkte).",
        "Formatiere die Antwort in Markdown mit Abschnitten: **Fazit**, **Risikokategorie**, **Anwendbare Anforderungen**, **Lücken**, **Empfehlungen**, **Quellen**.",
        "Bei unzureichenden Daten: gib an, welche Informationen benötigt werden."
    ])
    sections = sections_en if lang == "en" else sections_de
    prompt = f"""Analyze the following company and its product for EU AI Act compliance.
Company: {company}
Website: {url}
Product description: {description}
Open-source data:
{search_text}
{sections}"""
    return prompt

def build_enhanced_prompt(submission, search_text: str = "", lang: str = "en") -> str:
    """Build enhanced prompt from complete submission object with all fields.
    lang: 'en' or 'de'."""
    profile = build_company_profile(submission, lang)
    
    if not search_text:
        search_text = "No open-source data found." if lang == "en" else "Keine öffentlichen Daten gefunden."
    
    if lang == "en":
        prompt = f"""Analyze the following company and its AI systems for EU AI Act compliance.

## Company Profile

{profile}

Open-source data:
{search_text}

Based on all provided data, determine and describe in detail:

## 1. OVERALL CONCLUSION
Does the company's activity fall under EU AI Act regulation? What is the overall risk level?

## 2. EU AI ACT CLASSIFICATION
- Risk category under EU AI Act (Unacceptable / High / Limited / Minimal)
- Justification with references to specific articles
- Which AI systems fall under regulation

## 3. APPLICABLE REQUIREMENTS
Detailed list of EU AI Act requirements applicable to this case:
- Risk management (Article 9)
- Data governance and training (Article 10)
- Technical documentation and transparency (Articles 11-12)
- Automated decision-making and human oversight (Article 14)
- Accuracy, robustness and cybersecurity (Article 15)
- EU database registration (Article 49)
- Transparency obligations for users (Article 50)

## 4. IDENTIFIED GAPS
For each requirement, indicate whether the company complies, and if not — what specific gap exists:
- Missing documentation
- Insufficient control measures
- Data issues
- Lack of human oversight
- Insufficient transparency

## 5. SPECIFIC RECOMMENDATIONS
Step-by-step action plan:
- What documents to prepare
- What processes to implement
- What technical measures to adopt
- Deadlines and priorities (immediate / short-term / long-term)
- DPO requirement and registration

## 6. RISKS AND PENALTIES
- Potential fines for non-compliance (up to 35M EUR or 7% of global revenue)
- Reputational risks
- Risk of business suspension

Format the answer in markdown with H2 (##) and H3 (###) headings.
Use tables, lists, and bold text for emphasis."""
    else:
        prompt = f"""Analysiere das folgende Unternehmen und seine KI-Systeme auf EU AI Act-Konformität.

## Unternehmensprofil

{profile}

Öffentliche Daten:
{search_text}

Bestimme und beschreibe auf Basis aller bereitgestellten Daten im Detail:

## 1. GESAMTFAZIT
Fällt die Geschäftstätigkeit des Unternehmens unter die EU AI Act-Regulierung? Wie hoch ist das Gesamtrisiko?

## 2. EU AI ACT-EINSTUFUNG
- Risikokategorie nach EU AI Act (Unacceptable / High / Limited / Minimal)
- Begründung mit Verweisen auf konkrete Artikel
- Welche KI-Systeme fallen unter die Regulierung

## 3. ANWENDBARE ANFORDERUNGEN
Detaillierte Liste der anwendbaren EU AI Act-Anforderungen:
- Risikomanagement (Artikel 9)
- Datenverwaltung und Training (Artikel 10)
- Technische Dokumentation und Transparenz (Artikel 11-12)
- Automatisierte Entscheidungsfindung und menschliche Aufsicht (Artikel 14)
- Genauigkeit, Robustheit und Cybersicherheit (Artikel 15)
- EU-Datenbankregistrierung (Artikel 49)
- Transparenzpflichten für Nutzer (Artikel 50)

## 4. IDENTIFIZIERTE LÜCKEN
Für jede Anforderung: Gibt das Unternehmen die Konformität an, und wenn nicht — welche spezifische Lücke besteht:
- Fehlende Dokumentation
- Unzureichende Kontrollmaßnahmen
- Datenprobleme
- Fehlende menschliche Aufsicht
- Unzureichende Transparenz

## 5. KONKRETE EMPFEHLUNGEN
Schritt-für-Schritt-Aktionsplan:
- Welche Dokumente müssen erstellt werden
- Welche Prozesse müssen implementiert werden
- Welche technischen Maßnahmen sind erforderlich
- Fristen und Prioritäten (sofort / kurzfristig / langfristig)
- DSB-Anforderung und Registrierung

## 6. RISIKEN UND STRAFEN
- Mögliche Geldstrafen bei Nichteinhaltung (bis zu 35 Mio. EUR oder 7 % des Jahresumsatzes)
- Reputationsrisiken
- Risiko der Geschäftsaussetzung

Formatiere die Antwort in Markdown mit Überschriften der Ebene ## (H2) und ### (H3).
Verwende Tabellen, Listen und Fettdruck zur Hervorhebung."""
    
    return prompt
