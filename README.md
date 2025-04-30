# FastAPI Crash Course

This project is a hands-on crash course on building APIs using **FastAPI**, a modern, fast (high-performance) web framework for Python. The course is inspired by **Chai aur Code** and demonstrates how to create RESTful APIs with CRUD operations, database integration, and more.

---

## Features

- **User Management**:
  - Create, Read, Update, and Delete (CRUD) operations for users.
  - SQLite database integration using `SQLModel`.
  - Dependency injection for database sessions.

- **Tea Management**:
  - Manage a list of teas with CRUD operations.
  - In-memory storage for simplicity.

- **FastAPI Features**:
  - Dependency injection.
  - Pydantic models for data validation.
  - Asynchronous event handling.
  ---

  ## Installation

  1. Clone the repository:
    ```bash
    git clone https://github.com/arafatDU/fastapi-crash-course.git
    cd fastapi-crash-course
    ```

  2. Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

  3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

  4. Run the application:
    ```bash
    uvicorn main:app --reload
    ```