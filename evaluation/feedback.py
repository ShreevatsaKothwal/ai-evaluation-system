import os
import json
from groq import Groq


def generate_feedback(answer):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return {
            "strengths": "",
            "improvements": "",
            "overall_comment": "Feedback unavailable (API key not configured)."
        }

    client = Groq(api_key=api_key)

    question_text = answer.question.question_code
    student_answer = answer.extracted_text
    score = answer.marks_awarded
    max_score = answer.question.max_marks

    prompt = f"""
Return ONLY valid JSON.
Do not include markdown.
Do not include explanation outside JSON.

Format:
{{
  "strengths": "...",
  "improvements": "...",
  "overall_comment": "..."
}}

Question:
{question_text}

Student Answer:
{student_answer}

Score:
{score}/{max_score}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )

        output = response.choices[0].message.content

        try:
            return json.loads(output)
        except:
            return {
                "strengths": "",
                "improvements": "",
                "overall_comment": output
            }

    except Exception as e:
        return {
            "strengths": "",
            "improvements": "",
            "overall_comment": f"Feedback generation failed: {str(e)}"
        }



