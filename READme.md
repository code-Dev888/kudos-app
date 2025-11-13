# Kudos Project

A simple **Django + React** full-stack web application that allows users within an organization to send and receive *Kudos* — short appreciation messages — to promote a positive team culture.

---

## Project Overview

This project demonstrates a cleanly separated **Django REST API backend** and a **React frontend**.  
Each user belongs to an organization and can:
- Log in using their username and password  
- Give kudos to colleagues in the same organization (limited number per week)  
- View kudos they have received from others  

---

## Backend Setup (Django)

### 1. Create and activate a virtual environment

```bash
cd kudos_project/kudos_project
python -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Load Demo Data
```bash
python manage.py demo_data
```

### 5. Start backend server
```bash
python manage.py runserver
```
By default, the backend runs at:

http://127.0.0.1:8000/

## Frontend Setup (React)
### 1. Move into frontend directory
```bash
cd frontend
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Run frontend server
```bash
npm start
```
By default, the frontend runs at:

http://localhost:3000/

## API Endpoints
#### User Login

```http
  POST /api/auth/login/
```

#### Get all users

```http
  GET /api/users/
```

#### Get colleagues from same organization
```http
GET /api/users/<user_id>/
```

#### Send a Kudo to colleagues
```http
POST /api/kudos/give/<sender_id>/
```

#### Get all kudos received by the user
```http
GET /api/kudos/received/<user_id>/
```

#### Check how many kudos the user has
```http
GET /api/kudos/remaining/<user_id>/
```

## Management Commands
Note: This command will overwrite the existing data for users, organization, kudos. In that case the below given `Demo Credentials` won't be affective
### 1. demo_data
Populates the database with fake organizations, users, and kudos messages for quick testing.
```bash
python manage.py demo_data
```

### 2. reset_kudos
Resets all users’ available kudos back to 3 (simulating a weekly reset).
```bash
python manage.py reset_kudos
```

## Application Flow
### 1. Login
- Users log in using username/password. Password is 1234 for all users
- On success, backend returns user data and organization info.
### 2. Give kudos
- Logged-in user selects a colleague (from the same org) and sends a message.
- Kudos count decreases for the sender.
### 3. View received kudos
- User can view all the kudos they have received, along with sender.

## Application Tech Stack
- Backend : Django + DRF
- Frontend : React + Fetch API
- Data : Populated using Faker for demo
- Authentication : Simple credential-based
- Database : SQLite

## Future Improvements
- Add JWT-based authentication
- Add pagination for kudos list
- Password encryption
- Weekly automatic kudos reset using something similar to AWS CloudWatch

## Demo Credentials
These are the existing credentials in the database will be overwritten when demo_data command is executed.

```javascript
username	  password
bfranklin	    1234
caitlin92	    1234
ptaylor	        1234
melissa74	    1234
zcollins	    1234
pkeller	        1234
njacobson	    1234
xjennings	    1234
tparker	        1234
gpowers	        1234
meredithsutton	1234
dmarshall	    1234
```