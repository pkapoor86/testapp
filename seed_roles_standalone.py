from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

with app.app_context():
    db.create_all()  # Ensure the roles table exists
    for role_name in ['Admin', 'User']:
        if not Role.query.filter_by(name=role_name).first():
            db.session.add(Role(name=role_name))
            print(f"Created role: {role_name}")
        else:
            print(f"Role already exists: {role_name}")
    db.session.commit()
    print("Roles seeded successfully.")