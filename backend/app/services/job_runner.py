from datetime import datetime
from app.models.job import JobStatus
from app.services.serp_provider import MockSerpProvider
from app.agents.serp_agent import SerpAnalysisAgent
from app.agents.content_agent import ContentAgent

def run_full_generation(job):
    try:
        print(f"\n🚀 [JOB RUNNER] Starting job: {job.id}")
        print(f"🚀 [JOB RUNNER] Topic: {job.topic}")
        print(f"🚀 [JOB RUNNER] Target word count: {job.target_word_count}")
        
        job.status = JobStatus.running
        job.current_step = "Analyzing SERP results..."
        job.updated_at = datetime.utcnow()

        print(f"📊 [JOB RUNNER] Fetching SERP results...")
        # SERP
        serp_results = MockSerpProvider().fetch(job.topic)
        print(f"📊 [JOB RUNNER] Got {len(serp_results)} SERP results")
        
        topics = SerpAnalysisAgent().extract_topics(serp_results)
        print(f"📊 [JOB RUNNER] Extracted topics: {topics}")

        # External links from SERP
        external_links = [
            {"url": r.url, "context": f"Reference from SERP result #{r.rank}"}
            for r in serp_results[:3]
        ]
        print(f"📊 [JOB RUNNER] External links: {len(external_links)}")

        # Internal links (mocked)
        internal_links = [
            {"anchorText": "Remote team management best practices", "targetPage": "/remote-team-management"},
            {"anchorText": "Top collaboration tools", "targetPage": "/collaboration-tools"},
            {"anchorText": "Workflow automation guide", "targetPage": "/workflow-automation"},
        ]
        print(f"📊 [JOB RUNNER] Internal links: {len(internal_links)}")

        job.current_step = "Generating article content..."
        job.updated_at = datetime.utcnow()

        print(f"✍️ [JOB RUNNER] Starting content generation...")
        article = ContentAgent().generate_article(
            topic=job.topic,
            primary_keywords=["remote", "teams", "productivity tools"],
            internal_links=internal_links,
            external_links=external_links,
            target_word_count=job.target_word_count,
        )
        print(f"✍️ [JOB RUNNER] Content generation completed")

        job.status = JobStatus.completed
        job.current_step = "Article generation completed"
        job.updated_at = datetime.utcnow()

        print(f"✅ [JOB RUNNER] Job completed successfully: {job.id}")
        return article

    except Exception as e:
        print(f"❌ [JOB RUNNER] Job failed: {job.id}")
        print(f"❌ [JOB RUNNER] Error: {str(e)}")
        job.status = JobStatus.failed
        job.error = str(e)
        job.updated_at = datetime.utcnow()
        raise