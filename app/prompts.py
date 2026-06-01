# System prompt for EU AI Act compliance analysis — English only

SYSTEM_PROMPT_EN = """You are an expert on the EU AI Act. High-risk AI systems include: biometric identification, critical infrastructure, employment, credit scoring, education. Key requirements: risk management, data governance, transparency, human oversight, logging, conformity assessment.
Respond strictly with facts from the provided context only, using markdown format.

Your response MUST be in ENGLISH. Use technical terms in English only."""

SYSTEM_PROMPT_DE = """Sie sind ein Experte für den EU AI Act (EU-Verordnung 2024/1689 über künstliche Intelligenz). Hochrisiko-KI-Systeme umfassen: biometrische Identifizierung, kritische Infrastruktur, Beschäftigung, Bonitätsbewertung, Bildung. Wichtige Anforderungen: Risikomanagement, Datenqualität, Transparenz, menschliche Aufsicht, Protokollierung, Konformitätsbewertung.
Antworten Sie streng mit Fakten aus dem bereitgestellten Kontext, im Markdown-Format.

Ihre Antwort MUSS auf DEUTSCH sein. Verwenden Sie Fachbegriffe in der deutschen Übersetzung."""

SYSTEM_PROMPT_FR = """Vous êtes un expert de l'AI Act européen (Règlement UE 2024/1689 sur l'intelligence artificielle). Les systèmes d'IA à haut risque comprennent : l'identification biométrique, les infrastructures critiques, l'emploi, la notation de crédit, l'éducation. Exigences clés : gestion des risques, gouvernance des données, transparence, supervision humaine, journalisation, évaluation de la conformité.
Répondez strictement avec des faits provenant du contexte fourni uniquement, en utilisant le format markdown.

Votre réponse DOIT être en FRANÇAIS. Utilisez les termes techniques en français."""

SYSTEM_PROMPT_IT = """Sei un esperto dell'AI Act europeo (Regolamento UE 2024/1689 sull'intelligenza artificiale). I sistemi di IA ad alto rischio includono: identificazione biometrica, infrastrutture critiche, occupazione, valutazione del credito, istruzione. Requisiti chiave: gestione del rischio, governance dei dati, trasparenza, supervisione umana, registrazione, valutazione della conformità.
Rispondi rigorosamente con fatti tratti esclusivamente dal contesto fornito, utilizzando il formato markdown.

La tua risposta DEVE essere in ITALIANO. Utilizza i termini tecnici in italiano."""

SYSTEM_PROMPT_ES = """Eres un experto en la Ley de IA de la UE (Reglamento UE 2024/1689 sobre inteligencia artificial). Los sistemas de IA de alto riesgo incluyen: identificación biométrica, infraestructuras críticas, empleo, calificación crediticia, educación. Requisitos clave: gestión de riesgos, gobernanza de datos, transparencia, supervisión humana, registro, evaluación de la conformidad.
Responda estrictamente con hechos del contexto proporcionado solamente, utilizando el formato markdown.

Su respuesta DEBE estar en ESPAÑOL. Utilice los términos técnicos en español."""

def get_system_prompt(lang: str = "en") -> str:
    """Return system prompt in the requested language."""
    prompts = {
        "en": SYSTEM_PROMPT_EN,
        "de": SYSTEM_PROMPT_DE,
        "fr": SYSTEM_PROMPT_FR,
        "it": SYSTEM_PROMPT_IT,
        "es": SYSTEM_PROMPT_ES,
    }
    return prompts.get(lang, SYSTEM_PROMPT_EN)

def build_company_profile(submission, lang: str = "en") -> str:
    """Build structured company profile from submission data."""
    import json
    
    labels = {
        "en": {"company": "Company", "website": "Website", "size": "Company Size",
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
        "de": {"company": "Unternehmen", "website": "Webseite", "size": "Unternehmensgröße",
               "sector": "Branche", "employees": "Mitarbeiter", "revenue": "Jahresumsatz",
               "hq": "Hauptsitz", "not_specified": "Nicht angegeben", "ai_details": "KI-System-Details",
               "ai_count": "KI-Systeme im Einsatz", "ai_names": "Systemnamen",
               "ai_purpose": "KI-Zweck", "deployment": "Einsatzart",
               "data_sources": "Datenquellen", "decision_type": "Entscheidungsart",
               "risk_self": "Risiko-Selbsteinschätzung", "tech_details": "Technische Details",
               "model_types": "Modelltypen", "training_data": "Trainingsdaten-Herkunft",
               "human_oversight": "Menschliche Aufsicht", "explainability": "Erklärbarkeit / Interpretierbarkeit",
               "data_retention": "Datenaufbewahrungsrichtlinie", "compliance_status": "Compliance-Status",
               "documentation": "Dokumentation", "dpo": "DSB bestellt",
               "gdpr": "DSGVO-konform", "certifications": "Zertifizierungen",
               "audits": "Vorherige Audits", "ce_marking": "CE-Kennzeichnung",
               "high_risk": "Hochrisiko-Kategorien (ausgewählt)", "none_selected": "Keine ausgewählt",
               "additional_info": "Zusätzliche Informationen", "ai_activity": "KI-Aktivitätsbeschreibung",
               "yes": "Ja", "no": "Nein"},
        "fr": {"company": "Entreprise", "website": "Site web", "size": "Taille de l'entreprise",
               "sector": "Secteur", "employees": "Employés", "revenue": "Chiffre d'affaires annuel",
               "hq": "Siège social", "not_specified": "Non spécifié", "ai_details": "Détails du système d'IA",
               "ai_count": "Systèmes d'IA en production", "ai_names": "Noms des systèmes",
               "ai_purpose": "Objectif de l'IA", "deployment": "Type de déploiement",
               "data_sources": "Sources de données", "decision_type": "Type de décision",
               "risk_self": "Auto-évaluation des risques", "tech_details": "Détails techniques",
               "model_types": "Types de modèles", "training_data": "Origine des données d'entraînement",
               "human_oversight": "Supervision humaine", "explainability": "Explicabilité / Interprétabilité",
               "data_retention": "Politique de conservation des données", "compliance_status": "Statut de conformité",
               "documentation": "Documentation", "dpo": "DPO désigné",
               "gdpr": "Conforme RGPD", "certifications": "Certifications",
               "audits": "Audits précédents", "ce_marking": "Marquage CE",
               "high_risk": "Catégories à haut risque (sélectionnées)", "none_selected": "Aucune sélectionnée",
               "additional_info": "Informations supplémentaires", "ai_activity": "Description de l'activité IA",
               "yes": "Oui", "no": "Non"},
        "it": {"company": "Azienda", "website": "Sito web", "size": "Dimensioni azienda",
               "sector": "Settore", "employees": "Dipendenti", "revenue": "Fatturato annuo",
               "hq": "Sede principale", "not_specified": "Non specificato", "ai_details": "Dettagli sistema IA",
               "ai_count": "Sistemi IA in produzione", "ai_names": "Nomi dei sistemi",
               "ai_purpose": "Scopo dell'IA", "deployment": "Tipo di implementazione",
               "data_sources": "Fonti di dati", "decision_type": "Tipo di decisione",
               "risk_self": "Autovalutazione del rischio", "tech_details": "Dettagli tecnici",
               "model_types": "Tipi di modello", "training_data": "Origine dati di addestramento",
               "human_oversight": "Supervisione umana", "explainability": "Spiegabilità / Interpretabilità",
               "data_retention": "Politica di conservazione dati", "compliance_status": "Stato di conformità",
               "documentation": "Documentazione", "dpo": "DPO nominato",
               "gdpr": "Conforme GDPR", "certifications": "Certificazioni",
               "audits": "Audit precedenti", "ce_marking": "Marcatura CE",
               "high_risk": "Categorie ad alto rischio (selezionate)", "none_selected": "Nessuna selezionata",
               "additional_info": "Informazioni aggiuntive", "ai_activity": "Descrizione attività IA",
               "yes": "Sì", "no": "No"},
        "es": {"company": "Empresa", "website": "Sitio web", "size": "Tamaño de la empresa",
               "sector": "Sector", "employees": "Empleados", "revenue": "Ingresos anuales",
               "hq": "Sede central", "not_specified": "No especificado", "ai_details": "Detalles del sistema de IA",
               "ai_count": "Sistemas de IA en producción", "ai_names": "Nombres de sistemas",
               "ai_purpose": "Propósito de la IA", "deployment": "Tipo de implementación",
               "data_sources": "Fuentes de datos", "decision_type": "Tipo de decisión",
               "risk_self": "Autoevaluación de riesgos", "tech_details": "Detalles técnicos",
               "model_types": "Tipos de modelo", "training_data": "Origen de los datos de entrenamiento",
               "human_oversight": "Supervisión humana", "explainability": "Explicabilidad / Interpretabilidad",
               "data_retention": "Política de retención de datos", "compliance_status": "Estado de cumplimiento",
               "documentation": "Documentación", "dpo": "DPO designado",
               "gdpr": "Conforme al RGPD", "certifications": "Certificaciones",
               "audits": "Auditorías previas", "ce_marking": "Marcado CE",
               "high_risk": "Categorías de alto riesgo (seleccionadas)", "none_selected": "Ninguna seleccionada",
               "additional_info": "Información adicional", "ai_activity": "Descripción de la actividad de IA",
               "yes": "Sí", "no": "No"},
    }
    L = labels.get(lang, labels["en"])
    ns = L["not_specified"]
    
    profile = []
    profile.append(f"**{L['company']}:** {submission.company or ns}")
    profile.append(f"**{L['website']}:** {submission.url or ns}")
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
        search_text = "No open-source data found." if lang == "en" else "Aucune donnée open-source trouvée." if lang == "fr" else "Nessun dato open-source trovato." if lang == "it" else "No se encontraron datos de código abierto." if lang == "es" else "Keine öffentlichen Daten gefunden."
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
    sections_fr = "\n".join([
        "Sur la base de ces données, déterminez:",
        "1) Le produit relève-t-il d'une catégorie à haut risque ? (Oui/Non/Données insuffisantes).",
        "2) Quelles exigences de l'AI Act sont probablement applicables (liste).",
        "3) Lacunes identifiées (ce qui manque pour la conformité).",
        "4) Recommandations spécifiques (documents, processus, points de contrôle).",
        "Formatez la réponse en markdown avec les sections : **Conclusion**, **Catégorie de risque**, **Exigences applicables**, **Lacunes**, **Recommandations**, **Sources**.",
        "Si les données sont insuffisantes, indiquez quelles informations sont nécessaires."
    ])
    sections_it = "\n".join([
        "Sulla base di questi dati, determina:",
        "1) Il prodotto rientra in una categoria ad alto rischio? (Sì/No/Dati insufficienti).",
        "2) Quali requisiti dell'AI Act sono probabilmente applicabili (elenco).",
        "3) Lacune identificate (cosa manca per la conformità).",
        "4) Raccomandazioni specifiche (documenti, processi, punti di controllo).",
        "Formatta la risposta in markdown con le sezioni: **Conclusione**, **Categoria di rischio**, **Requisiti applicabili**, **Lacune**, **Raccomandazioni**, **Fonti**.",
        "Se i dati sono insufficienti, indica quali informazioni sono necessarie."
    ])
    sections_es = "\n".join([
        "Basándose en estos datos, determine:",
        "1) ¿El producto cae en una categoría de alto riesgo? (Sí/No/Datos insuficientes).",
        "2) Qué requisitos de la AI Act son probablemente aplicables (lista).",
        "3) Brechas identificadas (qué falta para el cumplimiento).",
        "4) Recomendaciones específicas (documentos, procesos, puntos de control).",
        "Formatee la respuesta en markdown con las secciones: **Conclusión**, **Categoría de riesgo**, **Requisitos aplicables**, **Brechas**, **Recomendaciones**, **Fuentes**.",
        "Si los datos son insuficientes, indique qué información se necesita."
    ])
    sections = sections_fr if lang == "fr" else sections_it if lang == "it" else sections_es if lang == "es" else sections_de if lang == "de" else sections_en
    prompt = f"""Analyze the following company and its product for EU AI Act compliance.
Company: {company}
Website: {url}
Product description: {description}
Open-source data:
{search_text}
{sections}"""
    return prompt

def build_enhanced_prompt(submission, search_text: str = "", lang: str = "en", website_data: dict = None) -> str:
    """Build enhanced prompt from complete submission object with all fields.
    lang: 'en' or 'de'.
    website_data: dict from WebsiteAnalyzer.analyze()"""
    profile = build_company_profile(submission, lang)
    
    # Build website analysis section
    website_section = ""
    if website_data and "error" not in website_data:
        parts = []
        legal_pages = website_data.get("legal_pages", {})
        if legal_pages:
            pages_str = ", ".join(legal_pages.keys())
            parts.append(f"Legal pages found: {pages_str}")
        
        tech_stack = website_data.get("tech_stack", {})
        if tech_stack:
            tech_str = "; ".join(f"{k}: {', '.join(v)}" for k, v in tech_stack.items() if v)
            parts.append(f"Technology stack: {tech_str}")
        
        gdpr = website_data.get("gdpr_signals", {})
        gdpr_found = [k for k, v in gdpr.items() if v]
        if gdpr_found:
            parts.append(f"GDPR compliance signals detected: {', '.join(gdpr_found)}")
        
        ai_act = website_data.get("ai_act_signals", {})
        ai_act_found = [k for k, v in ai_act.items() if v]
        if ai_act_found:
            parts.append(f"EU AI Act disclosure signals detected: {', '.join(ai_act_found)}")
        
        chatbot = website_data.get("chatbot_detected")
        if chatbot:
            platform = website_data.get("chatbot_platform", "unknown")
            parts.append(f"Chatbot detected on website: {platform}")
        
        cmp = website_data.get("cmp_detected")
        if cmp:
            parts.append(f"Cookie consent management platform: {cmp}")
        
        company_info = website_data.get("company_info", {})
        if company_info:
            info_str = ", ".join(f"{k}: {v}" for k, v in company_info.items() if v)
            parts.append(f"Company info extracted: {info_str}")
        
        if parts:
            website_section = "\n## Website Analysis\n\n" + "\n".join(f"- {p}" for p in parts)
    
    # Build raw website data section — shows what data we scraped from the URL
    raw_website_section = ""
    if website_data:
        raw_parts = []
        scanned_url = website_data.get("url", str(submission.url or "N/A"))
        raw_parts.append(f"**Analyzed URL**: {scanned_url}")
        
        if website_data.get("page_title"):
            raw_parts.append(f"**Page title**: {website_data['page_title']}")
        if website_data.get("page_description"):
            raw_parts.append(f"**Meta description**: {website_data['page_description'][:200]}")
        if website_data.get("company_name"):
            raw_parts.append(f"**Detected company name**: {website_data['company_name']}")
        if website_data.get("sector"):
            raw_parts.append(f"**Detected industry**: {website_data['sector']}")
        if website_data.get("hq_location"):
            raw_parts.append(f"**Detected HQ location**: {website_data['hq_location']}")
        
        ai_uses = website_data.get("ai_use_cases", [])
        if ai_uses:
            raw_parts.append(f"**AI-related keywords found on website**: {', '.join(ai_uses[:8])}")
        
        if website_data.get("privacy_policy_url"):
            raw_parts.append(f"**Privacy policy found**: {website_data['privacy_policy_url']}")
        if website_data.get("has_cookie_banner"):
            raw_parts.append("**Cookie consent banner**: detected")
        gdpr = website_data.get("gdpr_signals", [])
        if gdpr:
            raw_parts.append(f"**GDPR signals**: {', '.join(gdpr[:5])}")
        
        if website_data.get("ai_disclosures"):
            raw_parts.append(f"**AI disclosure pages found**: {len(website_data['ai_disclosures'])}")
        
        if raw_parts:
            raw_website_section = "\n## Source Data (Scraped from Website)\n\n" + "\n".join(f"- {p}" for p in raw_parts)
    
    if not search_text:
        search_text = "No open-source data found."

    # Build bilingual prompt sections
    lang_upper = "FRENCH" if lang == "fr" else "ITALIAN" if lang == "it" else "SPANISH" if lang == "es" else "GERMAN" if lang == "de" else "ENGLISH"
    
    sections_en = """## 1. OVERALL CONCLUSION (1-2 sentences only)
Is the company's activity regulated by the EU AI Act? What is the overall risk level?

## 2. KEY FINDINGS (3-5 bullet points max)
Most critical compliance issues found.

## 3. RISK LEVEL (one line)
Unacceptable / High / Limited / Minimal — with one sentence justification.

## 4. CRITICAL GAPS (3-5 bullet points max)
Only the most urgent compliance gaps.

## 5. TOP RECOMMENDATIONS (3-5 bullet points max)
Priority actions to take — ordered by urgency (immediate / short-term / long-term).

## 6. PENALTY RISK (1-2 sentences)
Potential fines and consequences if not addressed.

## 7. METHODOLOGY
How this analysis was performed: automated website scan (HTTP GET, HTML parsing, keyword detection for AI use cases, GDPR signals, privacy/cookie policies) + open-source data search (DuckDuckGo) + structured form data analysis against EU AI Act risk categories and requirements. The compliance score (0-100) is calculated from risk factors and compliance measures per the multi-variate formula defined in the AI Verify engine. Always provide this section.

## 8. SOURCES
- Official EU AI Act text: https://eur-lex.europa.eu/eli/reg/2024/1689
- EU AI Act high-risk list: https://artificialintelligenceact.eu/high-risk/
- European Commission AI page: https://digital-strategy.ec.europa.eu/en/policies/european-approach-artificial-intelligence"""

    sections_de = """## 1. GESAMTFAZIT (1-2 Sätze)
Wird die Tätigkeit des Unternehmens durch den EU AI Act reguliert? Wie hoch ist das Gesamtrisiko?

## 2. WICHTIGSTE ERKENNTNISSE (max. 3-5 Stichpunkte)
Die kritischsten Compliance-Probleme.

## 3. RISIKOSTUFE (eine Zeile)
Inakzeptabel / Hoch / Begrenzt / Minimal — mit einem Satz Begründung.

## 4. KRITISCHE LÜCKEN (max. 3-5 Stichpunkte)
Nur die dringendsten Compliance-Lücken.

## 5. WICHTIGSTE EMPFEHLUNGEN (max. 3-5 Stichpunkte)
Prioritäre Maßnahmen — geordnet nach Dringlichkeit (sofort / kurzfristig / langfristig).

## 6. STRAFRISTIKO (1-2 Sätze)
Mögliche Geldbußen und Konsequenzen bei Nichtbeachtung.

## 7. METHODIK
Diese Analyse wurde durchgeführt mittels: automatisiertem Website-Scan (HTTP GET, HTML-Parsing, Schlüsselwort-Erkennung für KI-Anwendungsfälle, GDPR-Signale, Datenschutz-/Cookie-Richtlinien) + Open-Source-Datensuche (DuckDuckGo) + strukturierte Formulardatenanalyse nach EU AI Act-Risikokategorien und -Anforderungen. Der Compliance-Score (0-100) wird aus Risikofaktoren und Compliance-Maßnahmen nach der multivariaten Formel der AI Verify Engine berechnet. Diese Sektion immer angeben.

## 8. QUELLEN
- Offizieller EU AI Act Text: https://eur-lex.europa.eu/eli/reg/2024/1689
- EU AI Act Hochrisiko-Liste: https://artificialintelligenceact.eu/high-risk/
- Europäische Kommission KI-Seite: https://digital-strategy.ec.europa.eu/en/policies/european-approach-artificial-intelligence"""

    sections_fr = """## 1. CONCLUSION GÉNÉRALE (1-2 phrases seulement)
L'activité de l'entreprise est-elle réglementée par l'AI Act de l'UE ? Quel est le niveau de risque global ?

## 2. PRINCIPAUX CONSTATS (max. 3-5 points)
Problèmes de conformité les plus critiques trouvés.

## 3. NIVEAU DE RISQUE (une ligne)
Inacceptable / Élevé / Limité / Minimal — avec une phrase de justification.

## 4. LACUNES CRITIQUES (max. 3-5 points)
Seules les lacunes de conformité les plus urgentes.

## 5. PRINCIPALES RECOMMANDATIONS (max. 3-5 points)
Mesures prioritaires à prendre — classées par urgence (immédiate / court terme / long terme).

## 6. RISQUE D'AMENDE (1-2 phrases)
Amendes et conséquences potentielles en l'absence de mesures.

## 7. MÉTHODOLOGIE
Comment cette analyse a été réalisée : scan automatisé du site web (HTTP GET, analyse HTML, détection de mots-clés pour les cas d'usage IA, signaux RGPD, politiques de confidentialité/cookies) + recherche de données open-source (DuckDuckGo) + analyse structurée des données du formulaire par rapport aux catégories de risque et aux exigences de l'AI Act de l'UE. Le score de conformité (0-100) est calculé à partir des facteurs de risque et des mesures de conformité selon la formule multivariée définie dans le moteur AI Verify. Toujours fournir cette section.

## 8. SOURCES
- Texte officiel de l'AI Act de l'UE : https://eur-lex.europa.eu/eli/reg/2024/1689
- Liste des systèmes à haut risque de l'AI Act : https://artificialintelligenceact.eu/high-risk/
- Page de la Commission européenne sur l'IA : https://digital-strategy.ec.europa.eu/en/policies/european-approach-artificial-intelligence"""

    sections_it = """## 1. CONCLUSIONE GENERALE (1-2 frasi soltanto)
L'attività dell'azienda è regolamentata dall'AI Act dell'UE? Qual è il livello di rischio complessivo?

## 2. RISULTATI PRINCIPALI (max. 3-5 punti)
I problemi di conformità più critici trovati.

## 3. LIVELLO DI RISCHIO (una riga)
Inaccettabile / Alto / Limitato / Minimo — con una frase di giustificazione.

## 4. LACUNE CRITICHE (max. 3-5 punti)
Solo le lacune di conformità più urgenti.

## 5. PRINCIPALI RACCOMANDAZIONI (max. 3-5 punti)
Azioni prioritarie da intraprendere — ordinate per urgenza (immediata / breve termine / lungo termine).

## 6. RISCHIO SANZIONI (1-2 frasi)
Multe e conseguenze potenziali se non affrontate.

## 7. METODOLOGIA
Come è stata eseguita questa analisi: scansione automatizzata del sito web (HTTP GET, parsing HTML, rilevamento di parole chiave per casi d'uso IA, segnali GDPR, policy sulla privacy/cookie) + ricerca dati open-source (DuckDuckGo) + analisi strutturata dei dati del modulo rispetto alle categorie di rischio e ai requisiti dell'AI Act dell'UE. Il punteggio di conformità (0-100) viene calcolato da fattori di rischio e misure di conformità secondo la formula multivariata definita nel motore AI Verify. Fornire sempre questa sezione.

## 8. FONTI
- Testo ufficiale dell'AI Act dell'UE: https://eur-lex.europa.eu/eli/reg/2024/1689
- Elenco ad alto rischio dell'AI Act: https://artificialintelligenceact.eu/high-risk/
- Pagina della Commissione europea sull'IA: https://digital-strategy.ec.europa.eu/en/policies/european-approach-artificial-intelligence"""

    sections_es = """## 1. CONCLUSIÓN GENERAL (1-2 frases solamente)
¿La actividad de la empresa está regulada por la AI Act de la UE? ¿Cuál es el nivel de riesgo general?

## 2. HALLAZGOS PRINCIPALES (max. 3-5 puntos)
Los problemas de cumplimiento más críticos encontrados.

## 3. NIVEL DE RIESGO (una línea)
Inaceptable / Alto / Limitado / Mínimo — con una frase de justificación.

## 4. BRECHAS CRÍTICAS (max. 3-5 puntos)
Solo las brechas de cumplimiento más urgentes.

## 5. PRINCIPALES RECOMENDACIONES (max. 3-5 puntos)
Acciones prioritarias a tomar — ordenadas por urgencia (inmediata / corto plazo / largo plazo).

## 6. RIESGO DE MULTA (1-2 frases)
Multas y consecuencias potenciales si no se abordan.

## 7. METODOLOGÍA
Cómo se realizó este análisis: escaneo automatizado del sitio web (HTTP GET, análisis HTML, detección de palabras clave para casos de uso de IA, señales GDPR, políticas de privacidad/cookies) + búsqueda de datos de código abierto (DuckDuckGo) + análisis estructurado de datos de formularios contra categorías de riesgo y requisitos de la AI Act de la UE. La puntuación de cumplimiento (0-100) se calcula a partir de factores de riesgo y medidas de cumplimiento según la fórmula multivariante definida en el motor AI Verify. Proporcione siempre esta sección.

## 8. FUENTES
- Texto oficial de la AI Act de la UE: https://eur-lex.europa.eu/eli/reg/2024/1689
- Lista de alto riesgo de la AI Act: https://artificialintelligenceact.eu/high-risk/
- Página de la Comisión Europea sobre IA: https://digital-strategy.ec.europa.eu/en/policies/european-approach-artificial-intelligence"""

    format_rules_en = """- MAXIMUM 3-4 sentences per section. No long paragraphs.
- Use short bullet points (max 5 per section), not long lists.
- NO tables unless absolutely necessary.
- Focus on the MOST CRITICAL findings only — don't list everything.
- The report should be EASY TO SCAN in 30 seconds."""

    format_rules_de = """- MAXIMAL 3-4 Sätze pro Abschnitt. Keine langen Absätze.
- Verwenden Sie kurze Aufzählungspunkte (max. 5 pro Abschnitt), keine langen Listen.
- KEINE Tabellen, es sei denn, unbedingt erforderlich.
- Konzentrieren Sie sich NUR auf die KRITISCHSTEN Erkenntnisse — nicht alles auflisten.
- Der Bericht sollte in 30 Sekunden EINFACH ÜBERBLICKBAR sein."""

    format_rules_fr = """- MAXIMUM 3-4 phrases par section. Pas de longs paragraphes.
- Utilisez des points courts (max 5 par section), pas de longues listes.
- PAS de tableaux sauf si absolument nécessaire.
- Concentrez-vous UNIQUEMENT sur les résultats les PLUS CRITIQUES — ne listez pas tout.
- Le rapport doit être FACILE À PARCOURIR en 30 secondes."""

    format_rules_it = """- MASSIMO 3-4 frasi per sezione. Niente paragrafi lunghi.
- Usa punti elenco brevi (max 5 per sezione), non elenchi lunghi.
- NIENTE tabelle se non assolutamente necessario.
- Concentrati SOLO sui risultati PIÙ CRITICI — non elencare tutto.
- Il rapporto deve essere FACILE DA SCORRERE in 30 secondi."""

    format_rules_es = """- MÁXIMO 3-4 frases por sección. Sin párrafos largos.
- Use puntos breves (máx. 5 por sección), no listas largas.
- SIN tablas a menos que sea absolutamente necesario.
- Concéntrese SOLO en los hallazgos MÁS CRÍTICOS — no enumere todo.
- El informe debe ser FÁCIL DE ESCANEAR en 30 segundos."""

    sections = sections_fr if lang == "fr" else sections_it if lang == "it" else sections_es if lang == "es" else sections_de if lang == "de" else sections_en
    format_rules = format_rules_fr if lang == "fr" else format_rules_it if lang == "it" else format_rules_es if lang == "es" else format_rules_de if lang == "de" else format_rules_en
    
    profile_banner = "## Company Profile (Profil de l'entreprise)" if lang == "fr" else "## Company Profile (Profilo aziendale)" if lang == "it" else "## Company Profile (Perfil de la empresa)" if lang == "es" else "## Company Profile (Unternehmensprofil)" if lang == "de" else "## Company Profile"

    prompt = f"""Analyze the following company and its AI systems for EU AI Act compliance.

{profile_banner}

{profile}

Open-source data / Öffentliche Daten:
{search_text}{website_section}{raw_website_section}

Based on all provided data, provide a SHORT, CONCISE compliance report.

IMPORTANT FORMAT RULES:
{format_rules}

You MUST write the entire report in {lang_upper}. All section headers MUST be in {lang_upper}. Use {lang_upper} terminology throughout.

Provide these sections:

{sections}

Keep the entire response under 2000 characters total. Short and actionable. Write like a lawyer advising a client — direct, clear, no fluff."""

    return prompt
