def build_prompt(user_query: str, results: list) -> str:
    """
    Builds a high-quality analyst-style prompt with natural language answers.
    """

    context_lines = []

    for r in results:
        context_lines.append(
            f"- STAT_ID: {r['statisticId']}\n"
            f"  Title: {r['title']}\n"
            f"  Region: {r.get('region', 'Global')}\n"
            f"  Industry: {r.get('industryId', 'N/A')}\n"
            f"  Chart Type: {r.get('chart_type', 'N/A')}\n"
        )

    context_text = "\n".join(context_lines)

    prompt = f"""
You are a professional market research analyst.

Using ONLY the statistics provided in the context below:
- Write clear, natural, business-friendly insights
- Do NOT invent numbers or facts
- Each bullet point MUST end with a citation in this format: [STAT_ID]

Context:
{context_text}

Question:
{user_query}

Instructions:
- Write 3 to 5 concise bullet points
- Each bullet should be insightful and readable
- End every bullet with [STAT_ID]

After the bullets, add a section:
Sources:
- STAT_ID: Statistic Title
"""

    return prompt.strip()
