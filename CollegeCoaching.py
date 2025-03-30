from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coaching.db'
db = SQLAlchemy(app)

# Models
class SuccessStory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    university = db.Column(db.String(100), nullable=False)
    testimonial = db.Column(db.Text)
    year = db.Column(db.Integer)

class ContactForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)

# Sample success stories data
success_stories = [
    {
        "student_name": "Sarah",
        "university": "Harvard University",
        "testimonial": "Fahad's guidance was instrumental in my acceptance to Harvard.",
        "year": 2023
    },
    {
        "student_name": "Ahmed",
        "university": "Stanford University",
        "testimonial": "The essay strategy sessions were game-changing!",
        "year": 2023
    },
    {
        "student_name": "Maria",
        "university": "MIT",
        "testimonial": "Couldn't have done it without Fahad's mentorship.",
        "year": 2022
    }
]

# Routes
@app.route('/')
def home():
    return render_template('home.html', 
                         success_stories=success_stories,
                         stats={
                             'success_rate': '85%',
                             'students_helped': '500+',
                             'top_schools': '20+'
                         })

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    services = {
        'essay_review': {
            'title': 'Essay Review & Strategy',
            'description': 'Comprehensive essay guidance and editing',
            'price': '$299'
        },
        'full_package': {
            'title': 'Complete Application Package',
            'description': 'End-to-end application support',
            'price': '$1999'
        },
        'hourly': {
            'title': 'Hourly Consultation',
            'description': 'Personalized 1:1 coaching',
            'price': '$150/hour'
        }
    }
    return render_template('services.html', services=services)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        new_contact = ContactForm(name=name, email=email, message=message)
        db.session.add(new_contact)
        db.session.commit()
        
        return redirect(url_for('thank_you'))
    return render_template('contact.html')

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=3000, debug=True)
