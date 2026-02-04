from openai import OpenAI
from app.config import OPENAI_API_KEY
import json
import re

client = OpenAI(api_key=OPENAI_API_KEY)

class ContentAgent:
    def generate_article(
        self,
        topic: str,
        primary_keywords: list[str],
        internal_links: list[dict],
        external_links: list[dict],
        target_word_count: int = 900,
    ) -> dict:

        prompt_template = """You are an expert SEO content writer. Write a comprehensive, detailed article with real content.

Topic: {topic}

Primary keywords to use: {primary_keywords}

Target word count: {word_count}

IMPORTANT: Write ACTUAL, DETAILED content. Do NOT use placeholder text like "Your paragraph here" or "Content here". Every paragraph must be 100+ words of real information.

Requirements:
- High primary keyword density (naturally integrated)
- Proper heading hierarchy (H1, H2, H3)
- SEO metadata (title tag, meta description)
- Keyword analysis (primary + secondary)
- Internal linking suggestions (3-5)
- External references (2-4 authoritative sources with context)
- Structured data (JSON-LD, schema.org Article)
- Real, detailed paragraphs (100+ words each)
- Actionable insights and examples

Return ONLY valid JSON in this EXACT format (no markdown, no code blocks):

{{
  "title": "Best Productivity Tools for Remote Teams in 2025",
  "meta": {{
    "title": "Best Productivity Tools for Remote Teams - 2025 Guide | Complete Review",
    "description": "Discover the best productivity tools for remote teams in 2025. Compare features, pricing, and find the perfect solution for your team."
  }},
  "keywords": {{
    "primary": ["remote productivity tools", "team collaboration software", "remote work solutions"],
    "secondary": ["distributed team management", "asynchronous communication tools", "project management software", "team communication platforms"]
  }},
  "content": [
    {{
      "type": "heading",
      "level": 1,
      "text": "Best Productivity Tools for Remote Teams in 2025"
    }},
    {{
      "type": "paragraph",
      "text": "Write a detailed 150+ word introduction explaining the importance of productivity tools for remote teams, current trends, and what this guide covers."
    }},
    {{
      "type": "heading",
      "level": 2,
      "text": "Why Remote Teams Need Productivity Tools"
    }},
    {{
      "type": "paragraph",
      "text": "Write a detailed 150+ word explanation of challenges remote teams face and how productivity tools solve them."
    }},
    {{
      "type": "heading",
      "level": 2,
      "text": "Top Productivity Tools for Remote Teams"
    }},
    {{
      "type": "paragraph",
      "text": "Write a detailed 200+ word overview of leading tools like Slack, Asana, Monday.com, Notion, etc. Include specific features and use cases."
    }},
    {{
      "type": "heading",
      "level": 3,
      "text": "Communication and Collaboration"
    }},
    {{
      "type": "paragraph",
      "text": "Write a detailed 150+ word section about communication tools specifically."
    }},
    {{
      "type": "heading",
      "level": 3,
      "text": "Project Management Solutions"
    }},
    {{
      "type": "paragraph",
      "text": "Write a detailed 150+ word section about project management tools."
    }},
    {{
      "type": "heading",
      "level": 2,
      "text": "How to Choose the Right Tool for Your Team"
    }},
    {{
      "type": "paragraph",
      "text": "Write a detailed 150+ word guide on evaluation criteria, budget considerations, and implementation tips."
    }},
    {{
      "type": "heading",
      "level": 2,
      "text": "Conclusion"
    }},
    {{
      "type": "paragraph",
      "text": "Write a detailed 100+ word conclusion summarizing key points and next steps."
    }}
  ],
  "internalLinks": [
    {{"anchorText": "remote team management best practices", "targetPage": "/remote-team-management"}},
    {{"anchorText": "team collaboration tools comparison", "targetPage": "/collaboration-tools"}},
    {{"anchorText": "project management software guide", "targetPage": "/project-management"}},
    {{"anchorText": "remote work efficiency tips", "targetPage": "/remote-work-tips"}},
    {{"anchorText": "asynchronous communication strategies", "targetPage": "/async-communication"}}
  ],
  "externalReferences": [
    {{"url": "https://www.forbes.com/sites/forbescommunicationscouncil/", "context": "According to Forbes Communications Council research on remote team productivity..."}},
    {{"url": "https://www.gartner.com/en", "context": "Gartner research indicates that companies using integrated productivity tools see a 25% improvement in team efficiency..."}},
    {{"url": "https://www.mckinsey.com", "context": "McKinsey studies show that effective remote team communication directly impacts project success rates..."}},
    {{"url": "https://www.techcrunch.com", "context": "TechCrunch analysis of emerging productivity tools reveals trends in AI-powered collaboration features..."}}
  ],
  "structuredData": {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Best Productivity Tools for Remote Teams in 2025",
    "description": "Comprehensive guide to the best productivity tools for remote teams in 2025",
    "author": {{"@type": "Person", "name": "Content Expert"}},
    "publisher": {{"@type": "Organization", "name": "Content Generator"}},
    "datePublished": "2025-01-01",
    "dateModified": "2025-01-01"
  }}
}}"""

        prompt = prompt_template.format(
            topic=topic,
            primary_keywords=", ".join(primary_keywords),
            word_count=target_word_count,
        )

        print(f"\n📝 [CONTENT AGENT] Generating article for: {topic}")
        print(f"📝 [CONTENT AGENT] Target word count: {target_word_count}")
        print(f"📝 [CONTENT AGENT] Primary keywords: {primary_keywords}")

        try:
            print(f"📝 [CONTENT AGENT] Calling OpenAI API...")
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )

            raw_response = response.choices[0].message.content.strip()
            print(f"📝 [CONTENT AGENT] Raw response length: {len(raw_response)} characters")
            print(f"📝 [CONTENT AGENT] First 300 chars: {raw_response[:300]}")
            
            # Try to extract JSON if it's wrapped in markdown code blocks
            json_match = re.search(r'```(?:json)?\s*([\s\S]*?)```', raw_response)
            if json_match:
                print(f"📝 [CONTENT AGENT] Extracted JSON from markdown code blocks")
                raw_response = json_match.group(1).strip()
            
            # Parse JSON
            article = json.loads(raw_response)
            print(f"✅ [CONTENT AGENT] Successfully parsed JSON")
            print(f"✅ [CONTENT AGENT] Article title: {article.get('title')}")
            print(f"✅ [CONTENT AGENT] Content blocks: {len(article.get('content', []))}")
            return article
            
        except json.JSONDecodeError as e:
            print(f"❌ [CONTENT AGENT] JSON parsing error: {str(e)}")
            print(f"❌ [CONTENT AGENT] Raw response: {raw_response[:500]}")
            raise ValueError(f"OpenAI response was not valid JSON. Error: {str(e)}")
        except Exception as e:
            print(f"❌ [CONTENT AGENT] Error: {str(e)}")
            raise ValueError(f"Failed to generate article: {str(e)}")