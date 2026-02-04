from app.models.serp import SerpResult
import re

class SerpAnalysisAgent:

    def extract_topics(self, results: list[SerpResult]) -> list[str]:
        topics = set()

        for r in results:
            title = r.title.lower()
            snippet = r.snippet.lower()

            if "tool" in title or "tool" in snippet:
                topics.add("Productivity tools overview")

            if "remote" in title or "distributed" in snippet:
                topics.add("Remote team challenges")

            if "collaboration" in title or "communication" in snippet:
                topics.add("Team collaboration & communication")

            if "compare" in title or "best" in title:
                topics.add("Comparison of top tools")

        return list(topics)
