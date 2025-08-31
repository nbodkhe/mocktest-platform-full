def percentile_from_histogram(score: float, histogram: dict):
    total = sum(histogram.values())
    if total == 0:
        return 0.0
    items = sorted((float(k), v) for k, v in histogram.items())
    below = 0
    for threshold, count in items:
        if score > threshold:
            below += count
        else:
            break
    return 100.0 * below / total

def predict_percentiles(total_score: float, subject_scores: dict, real_distribution: dict):
    p_overall = percentile_from_histogram(total_score, real_distribution.get("overall", {}))
    p_subjects = {s: percentile_from_histogram(v, real_distribution.get(s, {})) for s, v in subject_scores.items()}
    return p_overall, p_subjects
