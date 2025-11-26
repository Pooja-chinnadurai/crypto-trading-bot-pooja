"""
Simplified Trading Bot (Assignment Submission Version)
Does NOT require real API keys. Demonstrates full structure, logic,
input validation, and error handling.
"""

import time
import logging
from dataclasses import dataclass

# -------------------------------------------------------------------
# LOGGING SETUP
# -------------------------------------------------------------------
logging.basicConfig(
    filename="trading_bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------------------------------------------------
# DATA STRUCTURES
# -------------------------------------------------------------------
@dataclass
class Order:
    symbol: str
    side: str        # BUY or SELL
    order_type: str  # MARKET or LIMIT
    quantity: float
    price: float | None = None
    status: str = "PENDING"

# -------------------------------------------------------------------
# SIMULATED CLIENT (No API key needed)
# -------------------------------------------------------------------
class FakeBinanceClient:
    """A mock client that simulates Binance behaviour (for assignment)."""

    def _init_(self):
        logging.info("Fake Binance client initialized.")

    def place_order(self, order: Order):
        """Simulate order execution."""
        logging.info(f"Placing order: {order}")

        time.sleep(0.5)  # simulate network delay

        order.status = "FILLED"
        logging.info(f"Order filled: {order}")

        return {
            "symbol": order.symbol,
            "side": order.side,
            "type": order.order_type,
            "quantity": order.quantity,
            "price": order.price,
            "status": order.status
        }

# -------------------------------------------------------------------
# MAIN BOT CLASS
# -------------------------------------------------------------------
class BasicBot:
    def _init_(self):
        self.client = FakeBinanceClient()

    def validate_side(self, side):
        if side.upper() not in ["BUY", "SELL"]:
            raise ValueError("Side must be BUY or SELL")
        return side.upper()

    def validate_order_type(self, ot):
        if ot.upper() not in ["MARKET", "LIMIT"]:
            raise ValueError("Order type must be MARKET or LIMIT")
        return ot.upper()

    def place_market_order(self, symbol, side, quantity):
        side = self.validate_side(side)

        order = Order(
            symbol=symbol,
            side=side,
            order_type="MARKET",
            quantity=quantity,
            price=None
        )

        return self.client.place_order(order)

    def place_limit_order(self, symbol, side, quantity, price):
        side = self.validate_side(side)
        ot = "LIMIT"

        order = Order(
            symbol=symbol,
            side=side,
            order_type=ot,
            quantity=quantity,
            price=price
        )

        return self.client.place_order(order)

# -------------------------------------------------------------------
# COMMAND-LINE INTERFACE (Assignment Requirement)
# -------------------------------------------------------------------
def run_cli():
    print("\n=== Simplified Trading Bot ===\n")

    bot = BasicBot()

    try:
        symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
        side = input("Side (BUY/SELL): ").upper()
        order_type = input("Order Type (MARKET/LIMIT): ").upper()
        quantity = float(input("Quantity: "))

        if order_type == "MARKET":
            result = bot.place_market_order(symbol, side, quantity)

        elif order_type == "LIMIT":
            price = float(input("Limit Price: "))
            result = bot.place_limit_order(symbol, side, quantity, price)

        else:
            raise ValueError("Invalid order type selected.")

        print("\n=== ORDER RESULT ===")
        for k, v in result.items():
            print(f"{k}: {v}")

    except Exception as e:
        logging.error(f"Error: {e}")
        print(f"Error: {e}")

# -------------------------------------------------------------------
# RUN (disabled by default to avoid auto-execution)
# -------------------------------------------------------------------
if _name_ == "_main_":
    run_cli()
