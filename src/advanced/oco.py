import time
from binance.client import Client

def place_oco_order(client: Client, symbol: str, side: str, quantity: float, price1: float, price2: float):
    """
    Simulates OCO (One Cancels Other) by placing two opposite limit orders.
    When one is filled, the other should be canceled manually by monitoring.
    Binance Futures API does not have native OCO, so you handle it in code.
    """
    try:
        order1 = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            price=str(price1)
        )
        
        opposite_side = "SELL" if side == "BUY" else "BUY"
        order2 = client.futures_create_order(
            symbol=symbol,
            side=opposite_side,
            type="STOP_LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            price=str(price2),
            stopPrice=str(price2)
        )

        return {"order1": order1, "order2": order2}
    except Exception as e:
        return {"error": str(e)}
