# Flask E-Commerce Data Management

This project is a Flask application designed for managing product data in an e-commerce platform. It includes features for CRUD operations, JWT authentication, data cleaning, and generating summary reports.

## Features

- **Database Management**: Create, read product data.
- **User Authentication**: Sign-up and login functionality with JWT tokens.
- **Data Upload**: Upload data from a CSV file to the database.
- **Data Cleaning**: Handle missing values and ensure data consistency.
- **Summary Reports**: Generate summary reports with revenue and top-selling products.

## Requirements

- Python 3.9 or higher
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Pandas
- SQLite 

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/your-repository.git
    cd your-repository
    ```

2. **Create a Virtual Environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Update `config.py` or environment variables to configure the application:

- `DATABASE_URI`: The URI for the database connection (e.g., `sqlite:///ecommerce.db`).
- `SECRET_KEY`: A secret key for signing JWT tokens and session cookies.

## Endpoints
- /signup
- /login
  before acccessing other endpoints please do signIn with username and password
- /upload-data
- /summary-report

### Authentication

- **POST /signup**: Register a new user.
    - Request body: `{ "username": "user", "password": "pass" }`

- **POST /login**: Authenticate a user and get a JWT token.
    - Request body: `{ "username": "user", "password": "pass" }`
    - Response: `{ "access_token": "jwt_token" }`

### Data Management

- **POST /upload-data**: Upload product data from a CSV file.
    - Authorization: Bearer token required.
    - File upload: `multipart/form-data` with file field `file`.

### Data Analysis

- **GET /summary-report**: Generate and retrieve a summary report as a CSV file.
    - Authorization: Bearer token required.
    - Response: CSV file with `category`, `total_revenue`, `top_product`, and `top_product_quantity_sold`.

## Data Models

### Product

- `id`: Integer, primary key
- `product_id`: Integer, unique
- `product_name`: String
- `category`: String
- `price`: Integer
- `quantity_sold`: Integer
- `rating`: Integer
- `review_count`: Integer

### User

- `id`: Integer, primary key
- `username`: String, unique
- `password_hash`: String

## Running the Application

1. **Start the Flask Server**

    ```bash
    python3 app.py
    ```

2. **Visit the Application endpoints using postman**

    base-url- `http://127.0.0.1:5000/<endpoint>`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Flask: The web framework used for building the application.
- SQLAlchemy: ORM used for database interactions.
- JWT: For user authentication.
