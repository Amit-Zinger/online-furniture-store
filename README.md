# Online Furniture Store

## Group Members
- **Amit Zinger** - [GitHub Profile](https://github.com/Amit-Zinger)
- **Nitzan Ifrah** - [GitHub Profile](https://github.com/nitzanifrah)
- **Elad Shneor** - [GitHub Profile](https://github.com/EladShneor)
- **Etai Alfassa** - [GitHub Profile](https://github.com/EtaiAlfassa)

## Project Overview
This project is an **online furniture store** implemented in Python using Flask. It provides a platform for managing an inventory of furniture items, user authentication, shopping cart operations, and an order processing system.

## Project Structure
```
/
├── .github/workflows/  # Contains CI/CD pipeline configuration
│   ├── CI.yml          # Defines automated tests and deployment workflow
│
├── app/                # Core application logic
│   ├── APIroutes.py    # Handles API endpoints for authentication, inventory, cart, and orders
│   ├── __init__.py     # Package initializer for the app module
│   ├── auth.py         # Manages user authentication and authorization
│   ├── main.py         # Entry point to run the Flask application
│
├── models/             # Data models for the application
│   ├── __init__.py     # Package initializer for the models module
│   ├── cart.py         # Manages shopping cart operations
│   ├── factory.py      # Implements factory pattern for creating furniture objects
│   ├── furniture.py    # Defines furniture data structure
│   ├── inventory.py    # Handles inventory management
│   ├── order.py        # Manages order creation and processing
│   ├── user.py         # Defines user-related operations (registration, login, etc.)
│
├── requirements/       # Dependency management
│   ├── requirements.in # Raw dependencies
│   ├── requirements.txt# List of required dependencies for installation
│
├── tests/              # Unit and integration tests
│   ├── __init__.py     # Package initializer for the tests module
│   ├── regression.py   # Runs regression tests for the system
│   ├── test_APIroutes.py  # Tests API endpoints
│   ├── test_auth.py       # Tests authentication logic
│   ├── test_cart.py       # Tests cart operations
│   ├── test_factory.py    # Tests furniture factory creation
│   ├── test_furniture.py  # Tests furniture-related functionality
│   ├── test_inventory.py  # Tests inventory operations
│   ├── test_order.py      # Tests order processing
│   ├── test_user.py       # Tests user management
│
├── .coveragerc         # Configuration for test coverage reports
├── .gitignore          # Specifies ignored files in version control
├── Final Project Design Document.pdf  # Project design documentation
├── README.md           # Documentation for project usage and setup
```

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
#### Register a new user (`POST /users`)
Registers a new user in the system. The request must include a username, email, password, address, and user type (Client or Management). Management users must also provide a role. A successful request returns a confirmation message.

#### User login (`POST /auth/login`)
Authenticates a user with a username and password. On success, it returns a message indicating successful login along with session details.

### Inventory Management
#### Search for products (`GET /inventory`)
Allows searching for furniture in the inventory. Users can filter by product name, category, or price range. The response includes a list of matching furniture items with details such as name, price, and stock availability.

### Shopping Cart
#### Add an item to the cart (`POST /cart/items`)
Adds a specified quantity of a product to the user's shopping cart. The request must include the product name and quantity. If successful, the response confirms the item was added.

#### Remove an item from the cart (`DELETE /cart/items`)
Removes a specified product from the user's shopping cart. The request must include the product name. If the item exists in the cart, it is removed, and a confirmation message is returned.

### Order Processing
#### Checkout and place an order (`POST /orders`)
Processes an order for all items in the user's cart. The request must include user credentials and payment details. If successful, the system confirms the order and provides an order ID.
