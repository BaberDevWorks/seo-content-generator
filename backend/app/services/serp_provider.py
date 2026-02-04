from app.models.serp import SerpResult
import requests
import json
from app.config import SERP_API_KEY

class MockSerpProvider:
    def fetch(self, query: str) -> list[SerpResult]:
        """
        If SERP_API_KEY is set, call SerpApi (serpapi.com) to fetch up to 10 organic results,
        print JSONs as we receive them, and return a list[SerpResult].
        On any failure or if SERP_API_KEY is missing, fall back to the static mock list.
        """
        if not SERP_API_KEY:
            print("⚠️ [SERP PROVIDER] SERP_API_KEY not set; using static mock results")
            return [
                SerpResult(
                    rank=1,
                    url="https://example.com/productivity-tools",
                    title="15 Best Productivity Tools for Remote Teams",
                    snippet="Discover the best productivity tools that help remote teams collaborate efficiently."
                ),
                SerpResult(
                    rank=2,
                    url="https://example.com/remote-work-tools",
                    title="Top Remote Work Tools for Distributed Teams",
                    snippet="A complete guide to tools for communication, project management, and productivity."
                ),
                SerpResult(
                    rank=3,
                    url="https://example.com/best-collaboration-tools",
                    title="Best Collaboration Tools for Remote Teams",
                    snippet="Compare collaboration tools used by remote-first companies."
                ),
            ]

        try:
            print(f"📡 [SERP PROVIDER] Fetching SERP for query: {query}")
            params = {"q": query, "api_key": SERP_API_KEY, "num": 10}
            resp = requests.get("https://serpapi.com/search.json", params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            print(f"📡 [SERP PROVIDER] Raw API response keys: {list(data.keys())}")

            organic = data.get("organic_results") or data.get("organic") or data.get("results") or []

            results = []
            for idx, item in enumerate(organic[:10]):
                url = item.get("link") or item.get("url") or item.get("source") or ""
                title = item.get("title") or item.get("position") or ""
                snippet = item.get("snippet") or item.get("snippet") or item.get("snippet_highlighted") or ""
                sr = SerpResult(rank=idx + 1, url=url, title=title, snippet=snippet)
                # print each result JSON as we go (doesn't affect UI)
                print(f"📡 [SERP PROVIDER] Result {idx+1}: {json.dumps(sr.dict(), ensure_ascii=False)}")
                results.append(sr)

            if not results:
                print("⚠️ [SERP PROVIDER] No organic results returned; falling back to static mock")
                return [
                    SerpResult(
                        rank=1,
                        url="https://example.com/productivity-tools",
                        title="15 Best Productivity Tools for Remote Teams",
                        snippet="Discover the best productivity tools that help remote teams collaborate efficiently."
                    ),
                    SerpResult(
                        rank=2,
                        url="https://example.com/remote-work-tools",
                        title="Top Remote Work Tools for Distributed Teams",
                        snippet="A complete guide to tools for communication, project management, and productivity."
                    ),
                    SerpResult(
                        rank=3,
                        url="https://example.com/best-collaboration-tools",
                        title="Best Collaboration Tools for Remote Teams",
                        snippet="Compare collaboration tools used by remote-first companies."
                    ),
                ]

            return results

        except Exception as e:
            print(f"❌ [SERP PROVIDER] Fetch failed, falling back to static mock. Error: {e}")
            return [
                SerpResult(
                    rank=1,
                    url="https://example.com/productivity-tools",
                    title="15 Best Productivity Tools for Remote Teams",
                    snippet="Discover the best productivity tools that help remote teams collaborate efficiently."
                ),
                SerpResult(
                    rank=2,
                    url="https://example.com/remote-work-tools",
                    title="Top Remote Work Tools for Distributed Teams",
                    snippet="A complete guide to tools for communication, project management, and productivity."
                ),
                SerpResult(
                    rank=3,
                    url="https://example.com/best-collaboration-tools",
                    title="Best Collaboration Tools for Remote Teams",
                    snippet="Compare collaboration tools used by remote-first companies."
                ),
            ]