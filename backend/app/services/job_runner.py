from datetime import datetime
import json
import re
from app.models.job import JobStatus
from app.services.serp_provider import MockSerpProvider
from app.agents.content_agent import ContentAgent
from collections import Counter

def run_full_generation(job):
    try:
        print(f"\n🚀 [JOB RUNNER] Starting job: {job.id}")
        print(f"🚀 [JOB RUNNER] Topic: {job.topic}")
        print(f"🚀 [JOB RUNNER] Target word count: {job.target_word_count}")
        
        job.status = JobStatus.running
        job.current_step = "Analyzing SERP results..."
        job.updated_at = datetime.utcnow()

        print(f"📊 [JOB RUNNER] Fetching SERP results...")
        serp_results = MockSerpProvider().fetch(job.topic)
        print(f"📊 [JOB RUNNER] Got {len(serp_results)} SERP results")
        print(f"📊 [JOB RUNNER] Sample SERP result: {json.dumps(serp_results[0].dict(), ensure_ascii=False)}")
        
        texts = [job.topic] + [r.title for r in serp_results] + [r.snippet for r in serp_results]
        tokens = re.findall(r'\w+', " ".join(texts).lower())
        stopwords = {
            "the","and","for","with","that","this","from","about","your","have","them",
            "their","they","what","when","where","which","will","would","could","should",
            "also","more","than","into","only","other","these","those","using","use","uses",
            "tool","tools","best","top","guide","remote","team","teams"
        }
        filtered = [t for t in tokens if len(t) > 3 and t.isalpha() and t not in stopwords]
        counts = Counter(filtered)
        primary_keywords = [kw for kw, _ in counts.most_common(5)]
        if not primary_keywords:
            primary_keywords = [job.topic]
        print(f"📊 [JOB RUNNER] Derived primary keywords: {primary_keywords}")


        external_links = [
            {"url": r.url, "context": f"Reference from SERP result #{r.rank}"}
            for r in serp_results[:5]
        ]
        print(f"📊 [JOB RUNNER] External links (top 5): {json.dumps([e['url'] for e in external_links], ensure_ascii=False)}")
        
        internal_links = []
        for i, kw in enumerate(primary_keywords[:5], start=1):
            slug = kw.replace(" ", "-").lower()
            internal_links.append({"anchorText": f"{kw} guide", "targetPage": f"/{slug}"})
        print(f"📊 [JOB RUNNER] Internal links: {json.dumps([i['targetPage'] for i in internal_links], ensure_ascii=False)}")

        job.current_step = "Generating article content..."
        job.updated_at = datetime.utcnow()

        print(f"✍️ [JOB RUNNER] Starting content generation...")
        article = ContentAgent().generate_article(
            topic=job.topic,
            primary_keywords=primary_keywords,
            internal_links=internal_links,
            external_links=external_links,
            target_word_count=job.target_word_count,
        )
        print(f"✍️ [JOB RUNNER] Content generation completed")
        if isinstance(article, dict):
            article["externalReferences"] = external_links
            print(f"📎 [JOB RUNNER] Overrode article externalReferences with SERP links: {json.dumps([e['url'] for e in external_links], ensure_ascii=False)}")

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
