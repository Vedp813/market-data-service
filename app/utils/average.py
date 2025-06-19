def calculate_moving_average(prices: list[float]) -> float:
    if len(prices) == 0:
        return 0.0
    return round(sum(prices[-5:]) / min(5, len(prices)), 2)
