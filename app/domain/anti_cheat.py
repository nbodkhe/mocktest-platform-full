def check_burst(timestamps: list[int], window: int, threshold: int) -> bool:
    if not timestamps:
        return False
    timestamps = sorted(timestamps)
    i = 0
    for j in range(len(timestamps)):
        while timestamps[j] - timestamps[i] > window:
            i += 1
        if j - i + 1 >= threshold:
            return True
    return False
