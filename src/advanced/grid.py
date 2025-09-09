from binance.client import Client

def place_grid_orders(client: Client, symbol: str, side: str, quantity_per_order: float, low_price: float, high_price: float, grid_count: int):
    """
    Places multiple limit orders evenly spaced between low_price and high_price.
    Side indicates the direction for initial grid (e.g. 'BUY' for buy grid).
    """
    try:
        price_step = (high_price - low_price) / (grid_count - 1)
        orders = []

        for i in range(grid_count):
            price = round(low_price + i * price_step, 2)
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                timeInForce="GTC",
                quantity=quantity_per_order,
                price=str(price)
            )
            orders.append(order)

        return orders
    except Exception as e:
        return {"error": str(e)}
