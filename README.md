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
- **Request Format:** JSON
- **Request Data:** Requires user details including username, email, password, address, and user type (Client or Management). Management users must also provide a role.
- **Functionality:** Registers a new user in the system.
- **Response Format:** JSON
- **Response Data:** Confirms successful registration or returns an error if the username is already registered or required fields are missing.

#### User login (`POST /auth/login`)
- **Request Format:** JSON
- **Request Data:** Requires a username and password.
- **Functionality:** Authenticates the user and starts a session.
- **Response Format:** JSON
- **Response Data:** Confirms successful login or returns an error if the credentials are incorrect.

### Inventory Management
#### Search for products (`GET /inventory`)
- **Request Format:** JSON
- **Request Data:** Allows filtering by product name, category, or price range.
- **Functionality:** Retrieves products from the inventory based on the provided filters.
- **Response Format:** JSON
- **Response Data:** Returns a list of matching furniture items or an error if no products are found.

### Shopping Cart
#### Add an item to the cart (`POST /cart/items`)
- **Request Format:** JSON
- **Request Data:** Requires product name and quantity.
- **Functionality:** Adds the specified product to the user's shopping cart.
- **Response Format:** JSON
- **Response Data:** Confirms the addition or returns an error if the item is out of stock.

#### Remove an item from the cart (`DELETE /cart/items`)
- **Request Format:** JSON
- **Request Data:** Requires product name.
- **Functionality:** Removes the specified product from the user's shopping cart.
- **Response Format:** JSON
- **Response Data:** Confirms the removal or returns an error if the item does not exist in the cart.

### Order Processing
#### Checkout and place an order (`POST /orders`)
- **Request Format:** JSON
- **Request Data:** Requires payment details.
- **Functionality:** Processes an order for all items in the cart and updates inventory.
- **Response Format:** JSON
- **Response Data:** Confirms successful checkout or returns an error if the cart is empty or payment fails.
