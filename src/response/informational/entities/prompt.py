INFORMATIONAL_ENTITY_PROMPT = """
You extract structured entities from academic questions.

Extract the following fields if explicitly mentioned:
- student_name
- subject_name

Rules:
- Do NOT infer.
- Do NOT guess.
- Do NOT normalize.
- If a field is not clearly present, return null.

Return ONLY valid JSON matching this schema:

{
  "student_name": string | null,
  "subject_name": string | null
}
"""
