# Clone the project
git clone https://github.com/Utsavch189/Employee-Data-Generation-Visualization

# Create virtualenv
python3 -m venv env
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python3 manage.py runserver

# Run By docker
docker-compose up -d

# Stop docker
docker-compose down

# Application Address
http://127.0.0.1:8000

# Seeding Synthetic Data [Already seeded]
python3 scripts.py

## 📡 API Endpoints

### 🔐 **Login API**

**Endpoint:** `/api/auth/login/`  
**Method:** `POST`  
**Payload:**

```json
{
  "email": "utsavchatterjee71@gmail.com",
  "password": "admin"
}
```

### 📊 **Average Net Salary**

**Endpoint:** `/api/analytics/average-salary/`  
**Method:** `GET`  
**Authentication:** ✅ Required  
**Throttle Limit:** 20 requests/minute  


### 📊 **Attendance Summary**

**Endpoint:** `/api/analytics/attendance-summary/`  
**Method:** `GET`  
**Authentication:** ✅ Required  
**Throttle Limit:** 20 requests/minute  


### 📊 **Department-wise Salary Details**

**Endpoint:** `/api/analytics/department-salary/`  
**Method:** `GET`  
**Authentication:** ✅ Required  
**Throttle Limit:** 20 requests/minute  

### 📊 **Performance Stats & Top Performers**

**Endpoint:** `/api/analytics/performance-stats/`  
**Method:** `GET`  
**Authentication:** ✅ Required  
**Throttle Limit:** 20 requests/minute  


### 📊 **Recent Salary Payments**

**Endpoint:** `/api/analytics/recent-salaries/`  
**Method:** `GET`  
**Authentication:** ✅ Required  
**Throttle Limit:** 20 requests/minute  