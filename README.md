## Installation & Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/Girishg17/Expense-Sharing.git
    cd Expense-Sharing
    ```
2. **Create and activate a virtual environment:**

    ```sh
    python -m venv venv
    venv\Scripts\activate
    ```
3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```
4. **Go to project directory
   
   ```sh
   cd expense_app
   ```
5. **Migrate the project
   
   ```sh
   python manage.py migrate
   ```
6. **Finally run the server
   ```sh
    python manage.py runserver
   ```
## Usage
- Access the application at `http://127.0.0.1:8000/`.
- Use the Django admin interface at `http://127.0.0.1:8000/admin/` to manage users and expenses.
- alterenatively You can use `Postman`,`Thunder Client` to manage users and expenses.

## API Endpoints

### Users

- **Create a new user: POST request**
  ```sh
  http://127.0.0.1:8000/api/users/
  ```
  example JSON Body for this
  ```sh
  {"email": "girish@gmail.com",
  "name": "Girish",
  "phone_number": "1234567892"}
  ```
- Retrieve the users: GET request
  ```sh
  http://127.0.0.1:8000/api/users/
  ```
- Create an `exact` Type expense: POST request
  ```sh
  http://127.0.0.1:8000/api/expenses/
  ```
  example JSON Body for this
  ```sh
  {
  "created_by_email": "girish@gmail.com",
  "total_amount": 80.00,
  "split_type": "exact",
  "participants": [
      {"user_email": "girish1@gmail.com", "amount": 30},
      {"user_email": "girish2@gmail.com", "amount": 50}
  ]
    }
  ```
  **Note: Here participants should be created before creating expenses
  
- Create an `equal` type expense : POST request
  ```sh
  http://127.0.0.1:8000/api/expenses/
  ```
   example JSON Body for this
  ```sh
  {
  "created_by_email": "girish@gmail.com",
  "total_amount": 80.00,
  "split_type": "equal",
  "participants": [
      {"user_email": "girish1@gmail.com"},
      {"user_email": "girish2@gmail.com"}
  ]
    }
  ```
- Create a percentage expense : POST request
  ```sh
  http://127.0.0.1:8000/api/expenses/
  ```
  example JSON Body for this
  ```sh
  {
  "created_by_email": "girish@gmail.com",
  "total_amount": 80.00,
  "split_type": "percentage",
  "participants": [
      {"user_email": "girish1@gmail.com", "amount": 70},
      {"user_email": "girish2@gmail.com", "amount": 30}
  ]
    }
  ```
- Get total amount pent by a user : POST request
  ```sh
  http://127.0.0.1:8000/api/users/total-amount-spent/
  ```
  example JSON Body for this
  ```sh
  {
  "email": "girish2@gmail.com"
    }
  ```
- Get total amount owed by a user: GET request
  ```sh
  http://127.0.0.1:8000/api/users/owed-amounts/
  ```
  example JSON Body for this
  ```sh
  {
  "email": "girish2@gmail.com"
    }
- Download balance sheet in PDF: GET request
  ```sh
  http://127.0.0.1:8000/api/expenses/download-balance-sheet/
  ```
- Get overall expenses: GET request
  ```sh
  http://127.0.0.1:8000/api/expenses/overall-expenses/
  ```


 

