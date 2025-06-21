from typing import List

def calculate_moving_average(prices: List[float]) -> float:
    """
    Calculate the moving average of the most recent up to 5 price points.

    Args:
        prices (List[float]): A list of price values ordered from newest to oldest.

    Returns:
        float: The moving average rounded to 2 decimal places. Returns 0.0 if no prices provided.
    
    Notes:
        - The input list is expected to be ordered with the newest price first.
        - The function takes at most the first 5 prices to compute the average.
    """
    if not prices:
        return 0.0
    
    # Take the first up to 5 prices (newest prices)
    relevant_prices = prices[:5]

    # Calculate average and round to two decimals
    average = round(sum(relevant_prices) / len(relevant_prices), 2)
    return average
