# Gym Client Data App using Flask, SQLite, and SQLAlchemy

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Config: Use SQLite database for simplicity
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with app
db = SQLAlchemy(app)

# Define a simple model for gym clients
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20))
    membership_start = db.Column(db.Date)
    membership_end = db.Column(db.Date)
    membership_type = db.Column(db.String(50))
    goals = db.Column(db.Text)
    trainer_assigned = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Client {self.full_name}>'

# Home page: show form and list of clients
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        full_name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        membership_start = datetime.strptime(request.form['membership_start'], '%Y-%m-%d')
        membership_end = datetime.strptime(request.form['membership_end'], '%Y-%m-%d')
        membership_type = request.form['membership_type']
        goals = request.form['goals']
        trainer_assigned = request.form['trainer_assigned']

        # Create a new client object
        new_client = Client(
            full_name=full_name,
            email=email,
            phone=phone,
            membership_start=membership_start,
            membership_end=membership_end,
            membership_type=membership_type,
            goals=goals,
            trainer_assigned=trainer_assigned
        )

        # Add and commit to database
        try:
            db.session.add(new_client)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"An error occurred: {e}"

    # GET request: show all clients
    search_query = request.args.get('search')
    if search_query:
        clients = Client.query.filter(Client.full_name.contains(search_query)).all()
    else:
        clients = Client.query.order_by(Client.created_at.desc()).all()

    return render_template('index.html', clients=clients)

# Create database if it doesn't exist
with app.app_context():
    db.create_all()

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
