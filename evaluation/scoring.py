from django.conf import settings


# ----------------------------
# 🔹 Keyword Based Scoring
# ----------------------------
def keyword_based_score(answer):
    extracted = (answer.extracted_text or "").lower()
    rubric = answer.question.rubric or {}
    total_score = 0
    breakdown = {}

    if not extracted:
        return 0, {}

    for section, data in rubric.items():
        keywords = data.get("keywords", [])
        section_marks = data.get("marks", 0)

        if not keywords:
            breakdown[section] = 0
            continue

        matched = sum(1 for keyword in keywords if keyword.lower() in extracted)
        keyword_ratio = matched / len(keywords)

        section_score = keyword_ratio * section_marks
        breakdown[section] = round(section_score, 2)

        total_score += section_score

    return total_score, breakdown


# ----------------------------
# 🔹 Semantic Similarity Scoring
# ----------------------------
def semantic_similarity_score(answer):

    # ⛔ Stop immediately if semantic mode is OFF
    if not getattr(settings, "USE_SEMANTIC", False):
        return 0

    # 🔥 Import ONLY when needed
    from sentence_transformers import SentenceTransformer, util

    # Load model here (only in local semantic mode)
    model = SentenceTransformer("all-MiniLM-L6-v2")

    extracted = answer.extracted_text or ""
    rubric = answer.question.rubric or {}
    total_score = 0

    if not extracted:
        return 0

    emb_student = model.encode(extracted, convert_to_tensor=True)

    for section, data in rubric.items():
        references = data.get("references", [])
        section_marks = data.get("marks", 0)

        if not references:
            continue

        reference_text = " ".join(references)

        emb_reference = model.encode(reference_text, convert_to_tensor=True)

        similarity = util.cos_sim(emb_student, emb_reference).item()
        similarity = max(0, similarity)

        total_score += similarity * section_marks

    return total_score


# ----------------------------
# 🔹 Hybrid Final Score
# ----------------------------
def calculate_score(answer):
    keyword_score, keyword_breakdown = keyword_based_score(answer)

    if getattr(settings, "USE_SEMANTIC", False):
        semantic_score = semantic_similarity_score(answer)
        final_score = (0.7 * semantic_score) + (0.3 * keyword_score)
    else:
        final_score = keyword_score

    rounded_score = round(final_score * 2) / 2

    return {
        "total": rounded_score,
        "breakdown": keyword_breakdown
    }