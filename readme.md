# Foodo Backend

This is the backend service for **Foodo**, a food ordering and management application.  
It is containerized with Docker to ensure easy setup and consistent environments.

---

## 🚀 Getting Started

Follow these steps to run the project locally:

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Supriyo02/Foodo-Backend.git
cd Foodo-Backend
```

### 2️⃣ Checkout the Development Branch
```bash
git checkout dev
```

### 3️⃣ Create Your Own Branch
```bash
git checkout -b your-branch-name
```
### 4️⃣ Get the Environment Variables
Request the .env file from the repository owner and place it in the project root.

### 🐳 Run with Docker
#### First-time Setup
Build and run the container:
```bash
docker build . -t foodo-srv
docker run -p 8000:8000 -v ${pwd}:/usr/src/app --name foodo-backend -d foodo-srv
```

#### Subsequent Runs
Simply start the container:
```bash
docker start -a foodo-backend
```
Stop the container:
```bash
docker stop foodo-backend
```