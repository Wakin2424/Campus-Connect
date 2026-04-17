🎓 Campus Connect

Campus Connect is a student-only academic platform designed to enhance collaboration and learning within universities.
It enables students to ask and answer academic questions, share notes, buy and sell study materials, and form study groups, all in one centralized system.

The platform focuses on verified student participation, ensuring content relevance, trust, and academic integrity.

📌 Features

📚 Academic Q&A

Ask course-specific questions

View answers, likes, and engagement metrics

Filter by course or subject

📝 Notes & Handouts

Upload and access academic notes

View file size, ratings, views, and likes

🛒 Marketplace

Buy and sell textbooks and academic materials

Category-based product listing

Multiple payment options

👥 Study Groups

Join and participate in study groups

Verified users can create groups

Group discussions and collaboration

🔔 Notifications

Alerts for likes, responses, requests, and updates

✅ User Verification

Only verified users can create groups or perform sensitive actions

🏗️ System Architecture

Backend: Django (Python)

Database: PostgreSQL

Frontend: HTML, CSS, JavaScript

Authentication: Custom Django User Model

Deployment: Docker & Docker Compose

🧪 Technologies Used

Python (Django)

PostgreSQL

Docker & Docker Compose

HTML5 / CSS3 / JavaScript

Git & GitHub

⚙️ Installation & Setup (Using Docker)

Campus Connect uses Docker to ensure a consistent development environment across different machines.

🔹 Prerequisites

Make sure you have the following installed:

Docker

Docker Compose

Git

🔹 Step 1: Clone the Repository
git clone https://github.com/BlairKimani/Campus-Connect.git
cd campus-connect

🔹 Step 2: Configure Environment Variables

Create a .env file in the project root and add:

DEBUG=True
SECRET_KEY=your-secret-key
POSTGRES_DB=campus_connect
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

🔹 Step 3: Build and Run Containers
docker-compose up --build


This will:

Build the Django backend container

Start the PostgreSQL database container

Apply database migrations automatically

🔹 Step 4: Apply Migrations (If Needed)
docker-compose exec web python manage.py migrate

🔹 Step 5: Create Superuser
docker-compose exec web python manage.py createsuperuser

🔹 Step 6: Access the Application

Web App:
👉 http://localhost:8000

Admin Panel:
👉 http://localhost:8000/admin

📂 Project Structure (Overview)
campus-connect/
│ 
├── accounts/        # Custom user authentication 
├── qa/              # Questions & answers 
├── notes/           # Notes & handouts 
├── market/          # Marketplace 
├── groups/          # Study groups 
├── notifications/   # User notifications 
├── docker-compose.yml 
├── Dockerfile 
└── README.md 

🚀 Future Improvements

Real-time notifications

Advanced search & recommendation system

Mobile application

AI-powered answer ranking

Payment gateway integration

📄 License

This project is intended for educational and academic purposes.
You are free to modify and extend it for learning and research.
