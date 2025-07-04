# 📸 Capture Moments - Photographer Booking System

**Capture Moments** is a modern web application built using Flask and AWS DynamoDB. It allows users to browse professional photographers, check availability, and book sessions for various event types like weddings, portraits, birthdays, and more.

---
## 🚀 Features

- User authentication (Sign Up / Login / Logout)
- Photographer listings with location, skills, ratings
- Photographer availability calendar
- Booking form with event type, date, location, and special requirements
- Confirmation emails using Flask-Mail
- Admin dashboard (basic)
- Portfolio gallery (categorized)

---

## 🛠️ Technologies Used

- **Backend:** Flask (Python)
- **Database:** AWS DynamoDB
- **Frontend:** HTML, CSS, JS (Jinja2 templating)
- **Mail Service:** Flask-Mail (Gmail SMTP)
- **Deployment-ready:** Built for AWS EC2 with production-ready structure

---

## 📁 Project Structure

```bash
Capture_Moments/
│
├── static/
│   ├── css/styles.css
│   ├── js/script.js
│   └── images/
│       ├── vikram.jpg, meera.jpg ... (photographer images)
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── book.html
│   ├── photographers.html
│   ├── portfolio.html
│   ├── about.html
│   └── confirmation.html
│
├── .env
├── app.py
├── awsint.py  # if you're using a separate file for DynamoDB init (optional)
├── requirements.txt
└── README.md
