from ShoppingCart import ShoppingCart
import pandas as pd
class OrderManager:
    def __init__(self):
        # DataFrame to store order information, using order_id as the key
        self.orders = pd.DataFrame(columns=[
            'order_id', 'client_id', 'items', 'total_price',
            'payment_info', 'status', 'order_date'
        ])

    def create_order(self, cart, payment_info, total_price):
        import uuid
        from datetime import datetime

        order_id = str(uuid.uuid4())  # Generate a unique order ID
        order_date = datetime.now()
        order_data = {
            'order_id': order_id,
            'client_id': cart.client_id,
            'items': cart.cart,  # Includes item IDs and quantities
            'total_price': total_price,
            'payment_info': payment_info,
            'status': 'Processing',  # Initial status
            'order_date': order_date
        }
        # Append the order to the DataFrame
        self.orders = self.orders.append(order_data, ignore_index=True)
        print(f"Order {order_id} created successfully.")

    def get_order(self, order_id, client_id):
        order = self.orders[
            (self.orders['order_id'] == order_id) &
            (self.orders['client_id'] == client_id)
        ]
        if not order.empty:
            return order.to_dict(orient='records')[0]
        print(f"No order found with ID {order_id} for client {client_id}.")
        return None

    def update_order_status(self, order_id, status):
        if order_id in self.orders['order_id'].values:
            self.orders.loc[self.orders['order_id'] == order_id, 'status'] = status
            print(f"Order {order_id} status updated to {status}.")
        else:
            print(f"No order found with ID {order_id}.")

    def cancel_order(self, order_id):
        if order_id in self.orders['order_id'].values:
            self.orders.loc[self.orders['order_id'] == order_id, 'status'] = 'Cancelled'
            print(f"Order {order_id} has been cancelled.")
        else:
            print(f"No order found with ID {order_id}.")

    def get_order_history(self, client_id):
        history = self.orders[self.orders['client_id'] == client_id]
        if history.empty:
            print(f"No order history found for client {client_id}.")
            return []
        return history.to_dict(orient='records')

    def update_observer(self, order_id):
        if order_id in self.orders['order_id'].values:
            order_status = self.orders.loc[self.orders['order_id'] == order_id, 'status'].values[0]
            # Notify observer (e.g., email notification)
            print(f"Order {order_id} status is now {order_status}. Notifying observers...")
            # Assuming Email_Notification class exists and is used here
        else:
            print(f"No order found with ID {order_id}.")
