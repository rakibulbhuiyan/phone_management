import os

from openai import OpenAI


class PhoneLLMService:

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY is not configured."
            )

        self.client = OpenAI(
            api_key=api_key
        )

    def generate_answer(self, question, context):
        instructions = """
You are a Samsung phone research assistant.

Your job is to answer questions about Samsung
phones using the provided database context.

Rules:

1. Use the provided context as the primary source.
2. Do not invent phone specifications.
3. If information is missing, say that it is not
   available in the database.
4. When comparing phones, clearly mention the
   differences.
5. Keep the answer concise but informative.
6. Do not claim that a specification is from the
   database unless it is actually present there.
"""

        prompt = f"""
User question:
{question}

Database context:
{context}
"""

        response = self.client.responses.create(
            model="gpt-5.6-luna",
            instructions=instructions,
            input=prompt,
        )

        return response.output_text