# Online Furniture Store

## Group Members
- **Amit Zinger** - [GitHub Profile](https://github.com/Amit-Zinger)
- **Nitzan Ifrah** - [GitHub Profile](https://github.com/nitzanifrah)
- **Elad Shneor** - [GitHub Profile](https://github.com/EladShneor)
- **Etai Alfassa** - [GitHub Profile](https://github.com/EtaiAlfassa)

## Project Overview
This project is an **online furniture store** implemented in Python using Flask. It provides a platform for managing an inventory of furniture items, user authentication, shopping cart operations, and an order processing system.

## Installation

### Prerequisites
- Python 3.8+
- pip

### Steps to Install & Run
```bash
# Clone the repository
git clone https://github.com/your-repo/furniture-store.git
cd furniture-store

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```
The application will be accessible at `http://127.0.0.1:5000/`.

## API Documentation
### User Authentication
| Method | Endpoint | Description | Expected Request Body | Expected Response |
|--------|---------|-------------|------------------|------------------|
| `POST` | `/users` | Register a new user | `{ "username": "JohnDoe", "email": "john@example.com", "password": "pass123", "address": "123 Street" }` | `{ "message": "Registration successful!" }` |
| `POST` | `/auth/login` | Log in a user | `{ "username": "JohnDoe", "password": "pass123" }` | `{ "message": "Login successful!", "session": { "user_id": 1 } }` |

### Inventory Management
| Method | Endpoint | Description | Expected Request Body | Expected Response |
|--------|---------|-------------|------------------|------------------|
| `GET` | `/inventory` | Get available furniture items | None | `[ { "name": "Table", "price": 100.0, "quantity": 5 } ]` |
| `POST` | `/inventory` | Add a new furniture item | `{ "name": "Sofa", "price": 200.0, "quantity": 3 }` | `{ "message": "Item added successfully!" }` |
| `DELETE` | `/inventory` | Remove a furniture item | `{ "name": "Sofa" }` | `{ "message": "Item removed successfully!" }` |

### Shopping Cart
| Method | Endpoint | Description | Expected Request Body | Expected Response |
|--------|---------|-------------|------------------|------------------|
| `POST` | `/cart/items` | Add item to cart | `{ "name": "Table", "quantity": 2 }` | `{ "message": "Item added to cart" }` |
| `DELETE` | `/cart/items` | Remove item from cart | `{ "name": "Table" }` | `{ "message": "Item removed from cart" }` |

### Order Processing
| Method | Endpoint | Description | Expected Request Body | Expected Response |
|--------|---------|-------------|------------------|------------------|
| `POST` | `/orders` | Checkout and place an order | `{ "payment_info": "Visa 1234" }` | `{ "message": "Checkout successful", "order_id": "abc123" }` |
| `GET` | `/orders` | View order history | None | `[ { "order_id": "abc123", "total": 250.0, "status": "Processing" } ]` |


