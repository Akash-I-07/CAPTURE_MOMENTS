from collections import UserString
from flask import Flask, flash, redirect, render_template, request, jsonify, session, url_for 
import boto3
import uuid
from datetime import datetime

from flask_mail import Mail, Message

from app import hash_password

# Step 1: Create the Flask app instance
app = Flask(__name__)
# Step 2: Connect to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # Replace with your region

# Tables
photographers_table = dynamodb.Table('photographers')
bookings_table = dynamodb.Table('booking')

# Photographers data
photographers = [
    {
        "id": "p5", "name": "Vikram Singh", "skills": ["Event", "Corporate", "Portrait"],
        "image": "vikram.jpg", "location": "Guntur, Andhra Pradesh", "rating": 4.5,
        "experience": "9 years", "price_range": "₹16,000 - ₹28,000",
        "bio": "Professional event photographer with expertise in corporate events and executive portraits."
    },
    {
        "id": "p6", "name": "Lakshmi Devi", "skills": ["Fashion", "Birthday", "Kids"],
        "image": "lakshmi.jpg", "location": "Nizamabad, Telangana", "rating": 4.8,
        "experience": "5 years", "price_range": "₹10,000 - ₹18,000",
        "bio": "Specializes in children's photography and birthday celebrations with a gentle, patient approach."
    },
    {
        "id": "p7", "name": "Kiran Kumar", "skills": ["Wedding", "Events", "Candid"],
        "image": "kiran.jpg", "location": "Tirupati, Andhra Pradesh", "rating": 4.9,
        "experience": "12 years", "price_range": "₹20,000 - ₹35,000",
        "bio": "Master of candid wedding photography, capturing spontaneous moments and genuine emotions."
    },
    {
        "id": "p3", "name": "Arjun Reddy", "skills": ["Nature", "Wedding", "Birthday"],
        "image": "arjun.jpg", "location": "Vijayawada, Andhra Pradesh", "rating": 4.7,
        "experience": "10 years", "price_range": "₹18,000 - ₹30,000",
        "bio": "Award-winning photographer specializing in nature and outdoor wedding photography with artistic flair."
    },
    {
        "id": "p2", "name": "Priya Sharma", "skills": ["Fashion", "Event", "Model Shoot"],
        "image": "priya.jpg", "location": "Visakhapatnam, Andhra Pradesh", "rating": 4.9,
        "experience": "6 years", "price_range": "₹12,000 - ₹20,000",
        "bio": "Creative fashion photographer known for stunning model shoots and contemporary event coverage."
    },
    {
        "id": "p1", "name": "Rajesh Varma", "skills": ["Wedding", "Portrait", "Traditional"],
        "image": "rajesh.jpg", "location": "Hyderabad, Telangana", "rating": 4.8,
        "experience": "8 years", "price_range": "₹15,000 - ₹25,000",
        "bio": "Specializing in traditional Indian weddings and portrait photography with a focus on capturing authentic emotions."
    },
    {
        "id": "p4", "name": "Meera Krishnan", "skills": ["Wedding", "Traditional", "Family"],
        "image": "meera.jpg", "location": "Warangal, Telangana", "rating": 4.6,
        "experience": "7 years", "price_range": "₹14,000 - ₹22,000",
        "bio": "Expert in capturing traditional South Indian ceremonies and family portraits with cultural authenticity."
    }
    
]

# Availability
availability_data = {
    "p1": ["2025-02-15", "2025-02-20", "2025-02-25"],
    "p2": ["2025-02-18", "2025-02-22", "2025-02-28"],
    "p3": ["2025-02-16", "2025-02-21", "2025-02-26"],
    "p4": ["2025-02-17", "2025-02-23", "2025-03-01"],
    "p5": ["2025-02-19", "2025-02-24", "2025-03-02"],
    "p6": ["2025-02-14", "2025-02-27", "2025-03-03"],
    "p7": ["2025-02-13", "2025-02-29", "2025-03-05"]
}

# Portfolio
portfolio_categories = {
    "Weddings": [
        {"image": "wedding1.jpg", "title": "Traditional Telugu Wedding", "photographer": "Rajesh Varma"},
        {"image": "wedding2.jpg", "title": "South Indian Ceremony", "photographer": "Meera Krishnan"},
        {"image": "wedding3.jpg", "title": "Candid Wedding Moments", "photographer": "Kiran Kumar"},
    ],
    "Nature": [
        {"image": "nature1.jpg", "title": "Araku Valley Sunrise", "photographer": "Arjun Reddy"},
        {"image": "nature2.jpg", "title": "Godavari River", "photographer": "Arjun Reddy"},
    ],
    "Events": [
        {"image": "event1.jpg", "title": "Corporate Conference", "photographer": "Vikram Singh"},
        {"image": "event2.jpg", "title": "Cultural Festival", "photographer": "Priya Sharma"},
    ],
    "Model Shoots": [
        {"image": "model1.jpg", "title": "Fashion Portfolio", "photographer": "Priya Sharma"},
        {"image": "model2.jpg", "title": "Professional Headshots", "photographer": "Vikram Singh"},
    ],
    "Birthdays": [
        {"image": "birthday1.jpg", "title": "Kids Birthday Party", "photographer": "Lakshmi Devi"},
        {"image": "birthday2.jpg", "title": "Family Celebration", "photographer": "Arjun Reddy"},
    ]
}

# Routes
@app.route('/')
def home():
    return render_template('home.html', photographers=photographers[:3])

users = {}

#Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login credentials here
        username = request.form['username']
        password = request.form['password']
        # Example check (replace with DB check)
        if username == 'admin' and password == '1234':
            session['user'] = username
            return redirect('/show-photographers')
        else:
            
            ('Invalid login credentials')
            return redirect('/login')
    return render_template('login.html')

#Signup
@app.route('/signup', methods=['POST'])
def signup():
    # Handle new user registration
    username = request.form['newUsername']
    password = request.form['newPassword']
    # Save user to database or file (not shown here)
    flash('Signup successful! You can now log in.')
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/book', methods=['GET', 'POST'])
def book():
    
    if request.method == 'POST':
        photographer_id = request.form.get('photographer_id')
        date = request.form.get('date')
        event_type = request.form.get('event_type')
        location = request.form.get('location')
        photographer_name = next((p['name'] for p in photographers if p['id'] == photographer_id), 'Unknown')
        flash(f'Booking confirmed with {photographer_name} for {event_type} on {date} at {location}!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('book.html', photographers=photographers, availability_data=availability_data)

@app.route('/confirmation', methods=['POST'])
def confirmation():
    package = request.args.get("package") or request.form.get("package")
    booking = session.get("booking_details")

    if booking:
        msg = Message(
            subject="📸 Booking Confirmed - Capture Moments",
            sender=app.config['MAIL_USERNAME'],
            recipients=[booking["email"]],
            body=f"""Hello {booking['full_name']},

Thank you for booking with Capture Moments!

✔ Photographer ID: {booking['photographer_id']}
📅 Date: {booking['date']}
📦 Package: {package}
📍 Location: {booking['location']}

We’ll follow up with details and confirmations. Feel free to reach out if you need anything.

— The Capture Moments Team"""
        )
        Mail.send(msg)

    return render_template("confirmation.html", booking=booking, package=package)

@app.route('/photographers')
def show_photographers():
    return render_template('photographers.html', photographers=photographers, availability_data=availability_data)

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', portfolio_categories=portfolio_categories)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash('Please login to access dashboard.', 'error')
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=session['user'])

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)