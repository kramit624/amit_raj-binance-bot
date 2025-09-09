from binance.client import Client

def place_market_order(client: Client, symbol: str, side: str, quantity: float):
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity
        )
        return order
    except Exception as e:
        return {"error": str(e)}
