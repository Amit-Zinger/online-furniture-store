from models.cart import ShoppingCart
import pandas as pd
from typing import Optional, List, Dict

class OrderManager:
    """
    Manages orders in the system, including creation, updates, cancellations, and retrieval.

    Attributes:
        orders (pd.DataFrame): A DataFrame to store order information with columns for
        order_id, client_id, items, total_price, payment_info, status, and order_date.
    """

    def __init__(self):
        """
        Initializes the OrderManager with an empty DataFrame to manage orders.
        """
        self.orders = pd.DataFrame(
            columns=[
                "order_id",
                "client_id",
                "items",
                "total_price",
                "payment_info",
                "status",
                "order_date",
            ]
        )

    def create_order(
        self, cart: ShoppingCart, payment_info: str, total_price: float
    ) -> None:
        """
        Creates a new order and appends it to the DataFrame.

        Args:
            cart (ShoppingCart): The shopping cart associated with the client.
            payment_info (str): Payment details for the order.
            total_price (float): The total price of the order.
        """
        import uuid
        from datetime import datetime

        order_id = str(uuid.uuid4())  # Generate a unique order ID
        order_date = datetime.now()
        order_data = {
            "order_id": order_id,
            "client_id": cart.client_id,
            "items": cart.cart,  # Includes item IDs and quantities
            "total_price": total_price,
            "payment_info": payment_info,
            "status": "Processing",  # Initial status
            "order_date": order_date,
        }
        self.orders = self.orders.append(order_data, ignore_index=True)
        print(f"Order {order_id} created successfully.")

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
        Updates the status of an order.

        Args:
            order_id (str): The unique ID of the order.
            status (str): The new status of the order (e.g., 'Shipped', 'Cancelled').
        """
        if order_id in self.orders["order_id"].values:
            self.orders.loc[self.orders["order_id"]
                            == order_id, "status"] = status
            print(f"Order {order_id} status updated to {status}.")
        else:
            print(f"No order found with ID {order_id}.")

    def cancel_order(self, order_id: str) -> None:
        """
        Cancels an order by updating its status to 'Cancelled'.

        Args:
            order_id (str): The unique ID of the order.
        """
        if order_id in self.orders["order_id"].values:
            self.orders.loc[self.orders["order_id"]
                            == order_id, "status"] = "Cancelled"
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
            # Assuming Email_Notification class exists and is used here
        else:
            print(f"No order found with ID {order_id}.")
