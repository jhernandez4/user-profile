# Backend Set Up and Installation

## Prerequisites
* **Python 3.8+**
* **MySQL 8.0+**


## Installation
**1. Clone the repository**
```bash
git clone https://github.com/jhernandez4/user-profile.git
cd user-profile
```

**2. Create a MySQL database** 
```sql
CREATE DATABASE user_profile;
```

**3. Create an `.env` file**
* In the root of your project directory, create a `.env` file with the following content
* Make sure that the name of the database created in the previous step 
matches the database name in the `.env` file
* You can create a secret key with the command `openssl rand -hex 32`

```bash
MYSQL_URI="mysql://<username>:<password>@localhost/user_profile"
SECRET_KEY="MY_SECRET_KEY"
FRONTEND_ORIGIN="http://localhost:5173"
```

**4. Create a virtual environment**
```bash
python -m venv virtualEnv
```
**5. Activate the virtual environment**
* **Windows**
```bash
.\virtualEnv\Scripts\activate
```
* **MacOS/Linux**
```bash
source virtualEnv/bin/activate
```

**6. Install the dependencies**
```bash
pip install -r requirements.txt 
```

**7. Run the FastAPI development server**
```bash
fastapi dev .\main.py
```