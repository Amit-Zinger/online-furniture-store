import pandas as pd
import pickle
import os
from typing import Optional, List, Dict
from models.cart import ShoppingCart


class OrderManager:
    """
    Manages orders in the system, including creation, updates, cancellations, and retrieval.

    Attributes:
        orders (pd.DataFrame): A DataFrame to store order information.
    """

    ORDER_STORAGE_FILE = "orders.pkl"  # Define the pickle file name

    def __init__(self):
        """
        Initializes the OrderManager, loading orders from a pickle file if available.
        """
        self.orders = self.load_orders()  # Load orders from storage

    def save_orders(self) -> None:
        """Saves the orders DataFrame to a pickle file."""
        with open(self.ORDER_STORAGE_FILE, "wb") as f:
            pickle.dump(self.orders, f)

    def load_orders(self) -> pd.DataFrame:
        """Loads the orders DataFrame from a pickle file if it exists, otherwise returns an empty DataFrame."""
        if os.path.exists(self.ORDER_STORAGE_FILE):
            with open(self.ORDER_STORAGE_FILE, "rb") as f:
                return pickle.load(f)
        return pd.DataFrame(columns=["order_id", "client_id", "items", "total_price", "payment_info", "status", "order_date"])

    def create_order(self, cart: ShoppingCart, payment_info: str, total_price: float) -> None:
        """
        Creates a new order and appends it to the DataFrame, then saves it.
        """
        import uuid
        from datetime import datetime
        import json

        order_id = str(uuid.uuid4())
        order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        serialized_items = json.dumps(
            [{"item": vars(i["item"]), "quantity": i["quantity"]} for i in cart.items],
            default=str
        )

        order_data = {
            "order_id": order_id,
            "client_id": int(cart.user_id),
            "items": serialized_items,
            "total_price": total_price,
            "payment_info": payment_info,
            "status": "Processing",
            "order_date": order_date,
        }

        new_order_df = pd.DataFrame([order_data])
        self.orders = pd.concat([self.orders, new_order_df], ignore_index=True)

        self.save_orders()  # ✅ Save after creation

        print(f"✅ Order {order_id} created successfully!")

    def get_order(self, order_id: str, client_id: str) -> Optional[Dict]:
        """
        Retrieves the details of an order for a given client.

        Args:
            order_id (str): The unique ID of the order.
            client_id (str): The unique ID of the client.

        Returns:
            Optional[Dict]: A dictionary containing the order details if found, else None.
        """
        order = self.orders[
            (self.orders["order_id"] == order_id)
            & (self.orders["client_id"] == client_id)
        ]
        if not order.empty:
            return order.to_dict(orient="records")[0]
        print(f"No order found with ID {order_id} for client {client_id}.")
        return None

    def update_order_status(self, order_id: str, status: str) -> None:
        """
        Updates the status of an order and saves the change.
        """
        if order_id in self.orders["order_id"].values:
            self.orders.loc[self.orders["order_id"] == order_id, "status"] = status
            self.save_orders()  # ✅ Save after update
            print(f"Order {order_id} status updated to {status}.")
        else:
            print(f"No order found with ID {order_id}.")

    def cancel_order(self, order_id: str) -> None:
        """
        Cancels an order by updating its status to 'Cancelled' and saves the change.
        """
        if order_id in self.orders["order_id"].values:
            self.orders.loc[self.orders["order_id"] == order_id, "status"] = "Cancelled"
            self.save_orders()  # ✅ Save after cancellation
            print(f"Order {order_id} has been cancelled.")
        else:
            print(f"No order found with ID {order_id}.")

    def get_order_history(self, client_id: str) -> List[Dict]:
        """
        Retrieves the order history for a specific client.

        Args:
            client_id (str): The unique ID of the client.

        Returns:
            List[Dict]: A list of dictionaries containing the client's order history.
        """
        history = self.orders[self.orders["client_id"] == client_id]
        if history.empty:
            print(f"No order history found for client {client_id}.")
            return []
        return history.to_dict(orient="records")

    def update_observer(self, order_id: str) -> None:
        """
        Updates observers about the current status of an order.

        Args:
            order_id (str): The unique ID of the order.
        """
        if order_id in self.orders["order_id"].values:
            order_status = self.orders.loc[
                self.orders["order_id"] == order_id, "status"
            ].values[0]
            print(
                f"Order {order_id} status is now {order_status}. Notifying observers..."
            )
        else:
            print(f"No order found with ID {order_id}.")
