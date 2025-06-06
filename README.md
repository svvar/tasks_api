
# Tasks API

### Prerequisites

- Python 3.13 (developed with this)
- Virtual Environment

---

### Step 1: Clone the Repository

```sh
git clone https://github.com/svvar/tasks_api.git
cd tasks_api
```

### Step 2: Set Up the Virtual Environment

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Step 3: Install Requirements

```sh
pip install -r requirements.txt
```

### Step 4: Database Setup

Use PostgreSQL as database, create new database with desired name, for example `tasks_db`.
Then, set environment variables for database connection in `.env` file:

```env
DB_HOST=<...>
DB_PORT=<...>
DB_USER=<...>
DB_NAME=<...>
DB_PASSWORD=<...>
```

### Step 5: RSA Key Generation (optional)

Generate your unique RSA key pair for JWT authentication and save them to `rsa_private_key.pem` and `rsa_public_key.pem` 
files in the root directory of the project. OR use the provided example keys.


### Step 6: Run the Application for testing

```sh
fastapi dev api/app.py
```
---

### The application will be available at http://127.0.0.1:8000
### Try the API using the Swagger UI at http://127.0.0.1:8000/docs
### Before using task endpoints create new user and login, JWT is stored in cookies so you may not use Authorization header.
### Logs will be available in console and in `logs/` directory.
