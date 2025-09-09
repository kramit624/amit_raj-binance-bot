import time
from binance.client import Client

def place_twap_order(client: Client, symbol: str, side: str, total_quantity: float, duration_sec: int, parts: int):
    """
    Splits a large order into smaller equal parts over duration_sec seconds.
    Places parts number of market orders evenly spaced.
    """
    try:
        qty_per_part = total_quantity / parts
        interval = duration_sec / parts

        results = []
        for i in range(parts):
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=round(qty_per_part, 8) 
            )
            results.append(order)
            time.sleep(interval)

        return results
    except Exception as e:
        return {"error": str(e)}
