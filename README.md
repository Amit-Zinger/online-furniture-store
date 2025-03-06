# Online Furniture Store

## Group Members
- **Amit Zinger** - [GitHub Profile](https://github.com/Amit-Zinger)
- **Nitzan Ifrah** - [GitHub Profile](https://github.com/nitzanifrah)
- **Elad Shneor** - [GitHub Profile](https://github.com/EladShneor)
- **Etai Alfassa** - [GitHub Profile](https://github.com/EtaiAlfassa)

## Project Overview
This project is an **online furniture store** implemented in Python using Flask. It provides a platform for managing an inventory of furniture items, user authentication, shopping cart operations, and an order processing system.

## Wireframe
A detailed **Wireframe** was created to visualize the user interface and functionality of the platform. It includes:
- Homepage layout
- Navigation structure
- Shopping cart functionality
- User authentication flow

## Market Research
A **market analysis** was conducted to compare features and user experiences of leading online furniture stores. Key insights include:
- User expectations for **fast navigation** and **efficient filtering**
- Placement of elements based on common UX patterns
- Competitive advantages such as **discounted bundles and custom furniture options**

## Backend Planning
The backend architecture was designed with **performance, scalability, and security** in mind. We chose:
- **AWS CloudFront** for static content delivery
- **AWS Lambda** for serverless computing to reduce costs and improve performance
- **PostgreSQL on AWS RDS** for scalable and reliable database management
- **API Gateway** to manage communication between services
- **Amazon SES** for email notifications (order confirmations, registration emails)

### **Response Time Estimates**
| Action | Expected Response Time (seconds) | Notes |
|--------|--------------------------------|-------|
| Page Load | 0.5 - 2.0 | Using image compression (WebP) |
| User Login | 0.2 - 0.3 | Optimized authentication processing |
| Add to Cart | 0.15 - 0.3 | Real-time cart update |
| View Product Page | 0.7 - 2.5 | Cache used for static data |
| Apply Filters | 0.5 - 2.0 | Indexed database queries |
| Checkout Process | 1.0 - 5.0 | Includes payment processing |

## Software Diagram
A **UML class diagram** was created to model the relationships between the system components. Notable features:
- **Standardized function naming conventions**
- **Accurate arrows representing dependencies and data flow**
- **Distinction between static and dynamic calls**

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

## Contributors
For any questions or contributions, feel free to open an issue or a pull request.

