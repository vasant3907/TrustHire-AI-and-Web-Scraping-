"""
Scraping Service Module
Handles company data scraping from web using BeautifulSoup and optional Playwright.
"""

from __future__ import annotations

import re
from urllib.parse import parse_qs, quote_plus, unquote, urlparse

import httpx
from bs4 import BeautifulSoup


class ScrapingService:
    def __init__(self):
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121 Safari/537.36"
            )
        }
        self.timeout = httpx.Timeout(15.0, connect=6.0)

    def scrape_company_info(self, company_name: str) -> dict:
        company_name = (company_name or "").strip()
        if not company_name:
            return self._empty_company("")

        search_results = self._search_web(f"{company_name} official company website")
        website = self._pick_company_website(company_name, search_results)
        website_snapshot = self._scrape_website_snapshot(website) if website else {}
        reviews = self.scrape_reviews(company_name)
        linkedin = self.scrape_linkedin(company_name)
        naukri = self.scrape_naukri(company_name)
        public_mentions = self._collect_public_mentions(company_name)

        return {
            "company_name": company_name,
            "website": website,
            "title": website_snapshot.get("title"),
            "description": website_snapshot.get("description"),
            "linkedin_url": linkedin.get("linkedin_url"),
            "employee_count": linkedin.get("employee_count"),
            "industry": linkedin.get("industry"),
            "naukri_url": naukri.get("naukri_url"),
            "naukri_mentions": naukri.get("mentions", []),
            "reviews": reviews,
            "public_mentions": public_mentions,
            "search_results": search_results[:5],
            "source": "beautifulsoup_playwright_optional",
        }

    def scrape_linkedin(self, company_name: str) -> dict:
        results = self._search_web(f"{company_name} LinkedIn company")
        linkedin_url = next((item["url"] for item in results if "linkedin.com/company" in item["url"]), None)
        return {
            "linkedin_url": linkedin_url or f"https://www.google.com/search?q=site%3Alinkedin.com%2Fcompany+{quote_plus(company_name)}",
            "employee_count": None,
            "industry": None,
            "mentions": results[:4],
        }

    def scrape_naukri(self, company_name: str) -> dict:
        results = self._search_web(f"{company_name} Naukri company jobs reviews")
        naukri_url = next((item["url"] for item in results if "naukri.com" in item["url"]), None)
        return {
            "naukri_url": naukri_url or f"https://www.google.com/search?q=site%3Anaukri.com+{quote_plus(company_name)}+jobs",
            "mentions": [item for item in results[:5] if "naukri.com" in item["url"] or "job" in item["snippet"].lower()],
        }

    def scrape_reviews(self, company_name: str) -> list:
        queries = [
            f"{company_name} company reviews",
            f"{company_name} Glassdoor reviews",
            f"{company_name} Indeed reviews",
            f"{company_name} AmbitionBox reviews",
            f"{company_name} Trustpilot reviews",
        ]
        reviews = []
        for query in queries:
            for item in self._search_web(query)[:5]:
                item["review_source"] = self._source_name(item["url"])
                if item["review_source"] or any(word in item["snippet"].lower() for word in ["review", "rating", "salary", "interview", "work culture"]):
                    reviews.append(item)
        reviews = self._dedupe_results(reviews)[:10]
        return reviews or self._fallback_review_links(company_name)

    def _search_web(self, query: str) -> list[dict]:
        results = self._search_bing(query)
        if results:
            return results
        url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
        try:
            response = httpx.get(url, headers=self.headers, timeout=self.timeout, follow_redirects=True)
            response.raise_for_status()
        except Exception:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        for result in soup.select(".result"):
            link = result.select_one(".result__a")
            snippet = result.select_one(".result__snippet")
            if not link or not link.get("href"):
                continue
            normalized_url = self._normalize_result_url(link["href"])
            results.append(
                {
                    "title": link.get_text(" ", strip=True),
                    "url": normalized_url,
                    "snippet": snippet.get_text(" ", strip=True) if snippet else "",
                }
            )
        return results

    def _search_bing(self, query: str) -> list[dict]:
        url = f"https://www.bing.com/search?q={quote_plus(query)}"
        try:
            response = httpx.get(url, headers=self.headers, timeout=self.timeout, follow_redirects=True)
            response.raise_for_status()
        except Exception:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        for item in soup.select("li.b_algo"):
            link = item.select_one("h2 a")
            snippet = item.select_one(".b_caption p")
            if not link or not link.get("href"):
                continue
            results.append(
                {
                    "title": link.get_text(" ", strip=True),
                    "url": self._normalize_result_url(link["href"]),
                    "snippet": snippet.get_text(" ", strip=True) if snippet else "",
                }
            )
        return results

    def _normalize_result_url(self, url: str) -> str:
        if url.startswith("//"):
            url = "https:" + url
        parsed = urlparse(url)
        if "duckduckgo.com" in parsed.netloc:
            uddg = parse_qs(parsed.query).get("uddg")
            if uddg:
                return unquote(uddg[0])
        return url

    def _collect_public_mentions(self, company_name: str) -> list[dict]:
        queries = [
            f"{company_name} careers official",
            f"{company_name} hiring scam fake job",
            f"{company_name} recruiter email fraud",
            f"{company_name} company profile",
        ]
        mentions = []
        for query in queries:
            mentions.extend(self._search_web(query)[:4])
        return self._dedupe_results(mentions)[:12]

    def _source_name(self, url: str) -> str | None:
        host = urlparse(url).netloc.lower()
        if "glassdoor" in host:
            return "Glassdoor"
        if "indeed" in host:
            return "Indeed"
        if "ambitionbox" in host:
            return "AmbitionBox"
        if "trustpilot" in host:
            return "Trustpilot"
        if "naukri" in host:
            return "Naukri"
        if "linkedin" in host:
            return "LinkedIn"
        return None

    def _dedupe_results(self, results: list[dict]) -> list[dict]:
        seen = set()
        unique = []
        for item in results:
            key = item.get("url")
            if not key or key in seen:
                continue
            seen.add(key)
            unique.append(item)
        return unique

    def _pick_company_website(self, company_name: str, results: list[dict]) -> str | None:
        blocked = ["linkedin.", "glassdoor.", "indeed.", "naukri.", "facebook.", "instagram.", "twitter.", "x.com"]
        normalized_company = re.sub(r"[^a-z0-9]", "", company_name.lower())
        for item in results:
            parsed = urlparse(item["url"])
            host = parsed.netloc.lower().replace("www.", "")
            if any(domain in host for domain in blocked):
                continue
            host_token = re.sub(r"[^a-z0-9]", "", host.split(".")[0])
            if normalized_company and (normalized_company in host_token or host_token in normalized_company):
                return item["url"]
        for item in results:
            host = urlparse(item["url"]).netloc.lower()
            if host and not any(domain in host for domain in blocked):
                return item["url"]
        return None

    def _scrape_website_snapshot(self, url: str) -> dict:
        html = self._fetch_static(url)
        source = "beautifulsoup"
        if not html:
            html = self._fetch_with_playwright(url)
            source = "playwright"
        if not html:
            return {}

        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.get_text(" ", strip=True) if soup.title else None
        description_tag = soup.find("meta", attrs={"name": "description"})
        description = description_tag.get("content", "").strip() if description_tag else ""
        headings = [heading.get_text(" ", strip=True) for heading in soup.select("h1, h2")[:6]]
        return {
            "title": title,
            "description": description,
            "headings": headings,
            "source": source,
        }

    def _fetch_static(self, url: str) -> str | None:
        try:
            response = httpx.get(url, headers=self.headers, timeout=self.timeout, follow_redirects=True)
            response.raise_for_status()
            return response.text
        except Exception:
            return None

    def _fetch_with_playwright(self, url: str) -> str | None:
        try:
            from playwright.sync_api import sync_playwright
        except Exception:
            return None

        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True)
                page = browser.new_page(user_agent=self.headers["User-Agent"])
                page.goto(url, wait_until="domcontentloaded", timeout=12000)
                html = page.content()
                browser.close()
                return html
        except Exception:
            return None

    def _empty_company(self, company_name: str) -> dict:
        return {
            "company_name": company_name,
            "website": None,
            "employee_count": None,
            "founded_year": None,
            "reviews": [],
            "search_results": [],
        }

    def _fallback_review_links(self, company_name: str) -> list[dict]:
        query = quote_plus(company_name)
        sources = [
            ("Glassdoor", f"https://www.google.com/search?q=site%3Aglassdoor.com+{query}+reviews"),
            ("Indeed", f"https://www.google.com/search?q=site%3Aindeed.com+{query}+reviews"),
            ("AmbitionBox", f"https://www.google.com/search?q=site%3Aambitionbox.com+{query}+reviews"),
            ("Trustpilot", f"https://www.google.com/search?q=site%3Atrustpilot.com+{query}+reviews"),
        ]
        return [
            {
                "title": f"{company_name} reviews on {source}",
                "url": url,
                "snippet": f"Open public {source} search results for employee/customer review listings.",
                "review_source": source,
                "fallback": True,
            }
            for source, url in sources
        ]
