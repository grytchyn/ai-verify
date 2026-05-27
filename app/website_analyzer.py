"""
Website Analyzer for AI Compliance Assessment.

Simple synchronous HTTP-based analysis of a company website.
Extracts company info, AI use cases, privacy policy, GDPR signals, etc.
Uses httpx for requests and html.parser for HTML parsing.
No browser automation — just HTTP GET + HTML parsing.
"""

import re
import ssl
import logging
from html.parser import HTMLParser
from urllib.parse import urlparse, urljoin
from typing import Dict, List, Optional

import httpx

logger = logging.getLogger(__name__)

# ── AI-related keywords for detecting AI use cases ──
AI_USE_CASE_KEYWORDS = [
    "chatbot", "ai", "machine learning", "deep learning", "algorithm",
    "neural network", "neural", "llm", "large language model",
    "recommendation engine", "recommendation system", "recommend",
    "natural language processing", "nlp", "computer vision",
    "predictive analytics", "predictive model", "intelligent",
    "automation", "robotic process automation", "rpa",
    "speech recognition", "voice recognition", "image recognition",
    "facial recognition", "generative ai", "gen ai",
    "gpt", "transformer", "rag", "retrieval augmented generation",
    "conversational ai", "virtual assistant", "personalization",
    "anomaly detection", "fraud detection", "sentiment analysis",
    "knowledge graph", "decision intelligence",
    "autonomous", "self-driving", "cognitive",
    "tensorflow", "pytorch", "openai", "anthropic", "claude",
    "copilot", "co-pilot", "smart", "ml model",
]

# ── Common privacy/cookie page URL patterns ──
PRIVACY_PATTERNS = [
    "privacy", "privacy-policy", "privacy_policy", "privacypolicy",
    "privacy-notice", "privacy_notice", "datenschutz",
    "gdpr", "data-protection", "dataprotection",
    "cookie-policy", "cookie_policy", "cookies",
]

# ── GDPR keyword patterns ──
GDPR_KEYWORDS = [
    "gdpr", "dsgvo", "data protection officer", "dpo",
    "right to erasure", "right to be forgotten", "delete your data",
    "right to access", "subject access request", "access your personal data",
    "data portability", "right to object", "opt-out",
    "legitimate interest", "lawful basis", "consent",
    "data breach", "breach notification",
    "international data transfer", "standard contractual clauses", "scc",
    "data controller", "data processor",
    "cookie consent", "cookie settings", "cookie preferences",
    "personal data", "processing of personal data",
    "datenschutzerklärung", "datenschutzbeauftragter",
    "art. 6", "art. 7", "art. 13", "art. 14", "art. 15",
    "ccpa", "california consumer privacy",
]

# ── Cookie banner / consent UI indicators ──
COOKIE_BANNER_PATTERNS = [
    "cookie", "consent", "accept cookies", "reject cookies",
    "cookie settings", "cookie preferences", "cookie notice",
    "gdpr", "this website uses cookies", "we use cookies",
    "allow cookies", "decline cookies", "manage cookies",
    "cookie consent", "cookie banner", "cookie law",
    "cookie compliance", "cookie notice",
]

# ── Sector/industry clues ──
SECTOR_KEYWORDS = {
    "healthcare": ["healthcare", "health care", "medical", "hospital", "clinical", "pharma", "biotech", "health"],
    "finance": ["finance", "financial", "banking", "bank", "insurance", "investment", "fintech", "payments"],
    "technology": ["technology", "software", "saas", "cloud", "tech", "it ", "digital", "platform", "cyber"],
    "ecommerce": ["ecommerce", "e-commerce", "retail", "shop", "store", "marketplace", "shopping"],
    "education": ["education", "edtech", "learning", "training", "university", "school", "elearning"],
    "legal": ["legal", "law firm", "attorney", "lawyer", "compliance", "regulatory"],
    "manufacturing": ["manufacturing", "industrial", "factory", "supply chain", "logistics", "production"],
    "media": ["media", "advertising", "marketing", "publishing", "news", "entertainment", "social media"],
    "energy": ["energy", "utilities", "oil", "gas", "renewable", "solar", "clean energy"],
    "real_estate": ["real estate", "property", "housing", "commercial real estate"],
    "transportation": ["transportation", "logistics", "shipping", "delivery", "mobility", "automotive"],
    "consulting": ["consulting", "consultancy", "advisory", "professional services"],
    "telecommunications": ["telecom", "telecommunications", "mobile", "network", "isp", "connectivity"],
    "government": ["government", "public sector", "municipal", "federal", "public service"],
    "hospitality": ["hospitality", "hotel", "travel", "tourism", "restaurant", "food"],
}

# ── Simple HTML parser to extract text and meta tags ──
class SimpleHTMLParser(HTMLParser):
    """Minimal HTML parser that extracts title, meta tags, and text."""

    def __init__(self):
        super().__init__()
        self.title = ""
        self.description = ""
        self.og_title = ""
        self.og_description = ""
        self.meta_keywords = ""
        self.meta_generator = ""
        self.text_parts: List[str] = []
        self._in_title = False
        self._skip_tags = 0  # nest counter for script/style

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attrs_dict = dict(attrs)

        if tag == "title":
            self._in_title = True

        if tag in ("script", "style"):
            self._skip_tags += 1

        if tag == "meta":
            name = attrs_dict.get("name", "").lower()
            prop = attrs_dict.get("property", "").lower()
            content = attrs_dict.get("content", "")

            if name == "description" or prop == "og:description":
                self.description = content or self.description
            if name == "keywords":
                self.meta_keywords = content
            if prop == "og:title":
                self.og_title = content
            if name == "generator":
                self.meta_generator = content

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "title":
            self._in_title = False
        if tag in ("script", "style"):
            self._skip_tags = max(0, self._skip_tags - 1)

    def handle_data(self, data):
        if self._skip_tags > 0:
            return
        if self._in_title:
            self.title = (self.title + data).strip()
        else:
            stripped = data.strip()
            if stripped:
                self.text_parts.append(stripped)

    def get_text(self) -> str:
        return " ".join(self.text_parts)


def _normalize_url(url: str) -> str:
    """Ensure URL has a scheme."""
    if not url.startswith(("http://", "https://")):
        return "https://" + url
    return url.rstrip("/")


def _extract_domain_name(domain: str) -> str:
    """Extract a readable company name from domain: strip www., TLD, etc."""
    # Remove www. prefix
    name = re.sub(r"^www\.", "", domain)
    # Remove port if present
    name = name.split(":")[0]
    # Remove TLD (.com, .io, .co.uk, etc.)
    name = re.sub(r"\.[a-z]{2,}(\.[a-z]{2,})?$", "", name)
    # Replace hyphens/dots with spaces and title-case
    name = re.sub(r"[-.]", " ", name).strip()
    return name.title()


def _crawl_page(client: httpx.Client, url: str, timeout: int = 15) -> Optional[str]:
    """Fetch a page, return raw HTML or None on any error."""
    try:
        resp = client.get(url, timeout=timeout)
        resp.raise_for_status()
        return resp.text
    except httpx.TimeoutException:
        logger.warning(f"Timeout fetching {url}")
        return None
    except httpx.HTTPStatusError as e:
        logger.warning(f"HTTP {e.response.status_code} for {url}")
        return None
    except (httpx.RequestError, ssl.SSLError) as e:
        logger.warning(f"Request error for {url}: {e}")
        return None
    except Exception as e:
        logger.warning(f"Unexpected error fetching {url}: {e}")
        return None


def _find_privacy_policy(client: httpx.Client, base_url: str, html_content: str,
                         parsed_html: SimpleHTMLParser) -> Optional[str]:
    """Find privacy policy URL by checking common paths and links."""
    parsed_base = urlparse(base_url)

    # Strategy 1: Check common paths directly
    for pattern in PRIVACY_PATTERNS:
        for ext in ["", ".html", ".htm"]:
            test_url = f"{base_url}/{pattern}{ext}"
            try:
                resp = client.head(test_url, timeout=10)
                if resp.status_code == 200:
                    return test_url
            except Exception:
                pass

    # Strategy 2: Search page text for privacy-related links
    # Look for hrefs containing privacy-related words
    href_pattern = re.compile(
        r'href=["\']([^"\']*(?:privacy|datenschutz|gdpr|cookie)[^"\']*)["\']',
        re.IGNORECASE
    )
    matches = href_pattern.findall(html_content)
    for match in matches:
        full_url = urljoin(base_url, match)
        path = urlparse(full_url).path
        # Avoid anchors, mailto, etc.
        if path and not path.startswith("#") and not full_url.startswith("mailto:"):
            return full_url

    return None


def _detect_cookie_banner(html_content: str, page_text: str) -> bool:
    """Detect if the page has a cookie consent banner."""
    html_lower = html_content.lower()
    text_lower = page_text.lower()

    # Check for common cookie banner HTML patterns
    banner_selectors = [
        'id="cookie', 'id="consent', 'class="cookie', 'class="consent',
        'id="gdpr', 'class="gdpr', 'id="ccpa', 'class="ccpa',
        'cookie-banner', 'cookie-consent', 'cookie-notice',
        'cookiebar', 'cookie-bar', 'cookielaw',
        'consent-banner', 'consent-modal', 'consent-bar',
        'gdpr-banner', 'gdpr-consent',
        'data-cookie', 'data-consent',
    ]
    for sel in banner_selectors:
        if sel in html_lower:
            return True

    # Check text for cookie consent phrases
    consent_phrases = [
        "we use cookies", "this website uses cookies", "this site uses cookies",
        "cookie consent", "accept cookies", "reject cookies",
        "manage cookies", "cookie preferences", "cookie settings",
        "allow cookies", "decline cookies",
        "we and our partners use cookies",
    ]
    for phrase in consent_phrases:
        if phrase in text_lower:
            return True

    return False


def _detect_ai_use_cases(text: str) -> List[str]:
    """Detect AI use cases mentioned in page text."""
    found = []
    text_lower = text.lower()
    for keyword in AI_USE_CASE_KEYWORDS:
        if keyword.lower() in text_lower:
            found.append(keyword)
    return list(dict.fromkeys(found))  # deduplicate preserving order


def _detect_gdpr_signals(text: str) -> List[str]:
    """Detect GDPR compliance signals in page text."""
    found = []
    text_lower = text.lower()
    for keyword in GDPR_KEYWORDS:
        if keyword.lower() in text_lower:
            found.append(keyword)
    return list(dict.fromkeys(found))  # deduplicate


def _detect_sector(text: str, meta_keywords: str = "") -> Optional[str]:
    """Attempt to identify company sector/industry from page content."""
    combined = f"{meta_keywords} {text}".lower()

    scores = {}
    for sector, keywords in SECTOR_KEYWORDS.items():
        score = 0
        for kw in keywords:
            # Count occurrences
            score += combined.count(kw.lower())
        if score > 0:
            scores[sector] = score

    if scores:
        return max(scores, key=scores.get)
    return None


def _extract_hq_location(text: str, parsed: SimpleHTMLParser) -> Optional[str]:
    """Extract HQ location from page content."""
    text_lower = text.lower()

    # Patterns for location mentions
    location_patterns = [
        r"(?:headquarters?|head.?office|hq|hauptsitz)\s*[:–\-]?\s*([^.,\n]+(?:,\s*[A-Z]{2})?)",
        r"(?:based in|located in|headquartered in)\s*[:–\-]?\s*([^.,\n]+(?:,\s*[A-Z]{2})?)",
        r"(?:address|anschrift|registered address)\s*[:–\-]?\s*([^.\n]+)",
        r"office\s*(?:address)?\s*[:–\-]?\s*([^.\n]+(?:,\s*[A-Z]{2})?)",
    ]

    for pattern in location_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            location = match.group(1).strip()
            # Clean up excessive whitespace
            location = re.sub(r"\s+", " ", location)
            if len(location) > 5:
                return location

    return None


def _extract_ai_disclosures(client: httpx.Client, base_url: str,
                            html_content: str) -> List[Dict]:
    """Find pages mentioning 'AI' that could be AI disclosure pages."""
    disclosures = []

    # Check common AI-related page paths
    ai_paths = [
        "ai", "ai-policy", "ai-policies", "ai-disclosure", "ai-disclosures",
        "artificial-intelligence", "responsible-ai", "ai-act",
        "trustworthy-ai", "ai-governance", "ai-ethics",
        "ai-compliance", "ai-safety", "ai-principles",
    ]

    parsed_base = urlparse(base_url)

    for path in ai_paths:
        test_url = f"{base_url}/{path}"
        try:
            resp = client.get(test_url, timeout=10)
            if resp.status_code == 200:
                text_lower = resp.text.lower()
                if "ai" in text_lower or "artificial intelligence" in text_lower:
                    # Simple text extraction for summary
                    ai_text = _extract_text_from_html(resp.text)
                    summary = ai_text[:500] if ai_text else ""
                    disclosures.append({
                        "url": test_url,
                        "summary": summary,
                    })
        except Exception:
            continue

    return disclosures


def _extract_text_from_html(html_content: str) -> str:
    """Simple text extraction from HTML (no parser needed for rough extraction)."""
    # Remove script and style blocks
    text = re.sub(r"<script[^>]*>.*?</script>", "", html_content, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)
    # Decode common entities
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&quot;", '"').replace("&#39;", "'").replace("&#x27;", "'")
    text = text.replace("&nbsp;", " ").replace("&ndash;", "-").replace("&mdash;", "--")
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def analyze_website(url: str) -> Dict:
    """
    Analyze a company website for AI compliance-relevant data.

    Performs HTTP GET requests to discover and extract:
      - Company name (from <title>, og:title, domain)
      - Sector/industry (meta keywords, content analysis)
      - HQ location (footer, contact page text)
      - AI use cases (keywords in content)
      - Privacy policy URL and brief summary
      - Cookie consent presence
      - GDPR signals (privacy policy mentions)
      - AI disclosure content

    Args:
        url: Company website URL (with or without https://)

    Returns:
        dict with keys:
            company_name (str or None)
            sector (str or None)
            hq_location (str or None)
            ai_use_cases (list of str)
            privacy_policy_url (str or None)
            privacy_policy_summary (str)
            has_cookie_banner (bool)
            gdpr_signals (list of str)
            ai_disclosures (list of dict with url, summary)
            page_title (str or None)
            page_description (str or None)
            error (str or None, only set on critical failure)
    """
    url = _normalize_url(url)
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    result: Dict = {
        "company_name": None,
        "sector": None,
        "hq_location": None,
        "ai_use_cases": [],
        "privacy_policy_url": None,
        "privacy_policy_summary": "",
        "has_cookie_banner": False,
        "gdpr_signals": [],
        "ai_disclosures": [],
        "page_title": None,
        "page_description": None,
        "error": None,
    }

    client = httpx.Client(
        follow_redirects=True,
        timeout=httpx.Timeout(15.0, connect=10.0, read=10.0),
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        },
    )

    try:
        # ── Fetch main page ──
        html_content = _crawl_page(client, url)
        if html_content is None:
            result["error"] = f"Could not fetch {url} — site may be unreachable or non-existent"
            client.close()
            return result

        # ── Parse HTML ──
        parser = SimpleHTMLParser()
        parser.feed(html_content)
        page_text = parser.get_text()
        page_text_lower = page_text.lower()

        # ── 1. Company name ──
        company_name = parser.og_title or parser.title
        if not company_name:
            company_name = _extract_domain_name(domain)
        else:
            # Clean up common suffixes
            company_name = re.sub(
                r"\s*[\|–—-]\s*(?:Home|Official Website|Homepage|Official Site|Crunchbase.*)$",
                "", company_name, flags=re.IGNORECASE
            ).strip()
            # If og:title/title is very long, truncate sensibly
            if len(company_name) > 80:
                company_name = company_name[:80]
        result["company_name"] = company_name

        # ── Page title & description ──
        result["page_title"] = parser.title
        result["page_description"] = parser.description

        # ── 2. Sector/industry ──
        result["sector"] = _detect_sector(page_text, parser.meta_keywords)

        # ── 3. HQ location ──
        result["hq_location"] = _extract_hq_location(page_text, parser)

        # ── 4. AI use cases ──
        result["ai_use_cases"] = _detect_ai_use_cases(page_text)

        # ── 5. Privacy policy ──
        privacy_url = _find_privacy_policy(client, url, html_content, parser)
        result["privacy_policy_url"] = privacy_url

        privacy_html = None
        if privacy_url:
            privacy_html = _crawl_page(client, privacy_url)
            if privacy_html:
                privacy_text = _extract_text_from_html(privacy_html)
                # Summarize: first 1000 chars
                result["privacy_policy_summary"] = privacy_text[:1000]

        # ── 6. Cookie consent presence ──
        result["has_cookie_banner"] = _detect_cookie_banner(html_content, page_text)

        # ── 7. GDPR signals ──
        # Check both main page and privacy policy
        all_text_for_gdpr = page_text
        if privacy_url and privacy_html:
            privacy_text = _extract_text_from_html(privacy_html)
            all_text_for_gdpr += " " + privacy_text
        result["gdpr_signals"] = _detect_gdpr_signals(all_text_for_gdpr)

        # ── 8. AI disclosure content ──
        result["ai_disclosures"] = _extract_ai_disclosures(client, url, html_content)

    except Exception as e:
        logger.exception(f"Unexpected error analyzing {url}")
        result["error"] = str(e)
    finally:
        client.close()

    return result


# ── Domain info helper ──
def extract_domain_info(url: str) -> Dict[str, str]:
    """Extract basic domain information from URL."""
    parsed = urlparse(url if url.startswith(("http://", "https://")) else f"https://{url}")
    return {
        "domain": parsed.netloc,
        "scheme": parsed.scheme,
        "path": parsed.path or "/",
    }
