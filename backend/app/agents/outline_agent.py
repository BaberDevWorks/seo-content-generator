from openai import OpenAI

client = OpenAI(api_key="YOUR_OPENAI_API_KEY_HERE")

class OutlineAgent:
    def generate_outline(self, topic: str, topics: list[str]) -> list[str]:
        prompt = f"""
        You are an SEO expert. Create a detailed outline for an article about:
        Topic: {topic}
        Based on these key subtopics: {', '.join(topics)}

        Generate 5-8 headings (H2/H3) that cover all subtopics.
        Return only a JSON array of headings.
        """
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        text = response.choices[0].message.content
        # parse JSON safely
        import json
        headings = []
        try:
            headings = json.loads(text)
        except Exception:
            headings = topics  # fallback
        return headings
