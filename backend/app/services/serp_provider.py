from app.models.serp import SerpResult

class MockSerpProvider:
    def fetch(self, query: str) -> list[SerpResult]:
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
            # assume up to 10
        ]
