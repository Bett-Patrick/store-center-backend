from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from flask_bcrypt import Bcrypt
from config import db


bcrypt = Bcrypt()

class User(db.Model, SerializerMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String)
    role = db.Column(db.String, nullable=False)
    phone_no = db.Column(db.Integer)
    
    serialize_only = ('id', 'username', 'email', 'phone_no')
    
    orders = db.relationship("Order",back_populates= "user",cascade="all, delete-orphan")
    

    @validates('username')
    def validate_username(self, key, username):
        existing_user = User.query.filter(User.username == username).first()
        if existing_user:
            raise ValueError("Username already exists")
        return username

    @validates('email')
    def validate_email(self, key, email):
        existing_email = User.query.filter(User.email == email).first()
        if existing_email:
            raise ValueError("Email already exists")
        return email

    @validates('role')
    def validate_role(self, key, role):
        try:
            (role)
        except ValueError:
            raise ValueError("Role must be 'admin' or 'user'")
        return role
    

    @hybrid_property
    def password_hash(self):
        raise Exception('Password hashes may not be viewed.')

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)
    
    
    def __init__(self, username, email, role, phone_no=None, password=None):
        self.username = username
        self.email = email
        self.role = role
        self.phone_no = phone_no
        if password:
            self.password = password

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'phone_no': self.phone_no,
            'username ': self.username,
            ' _password_hash':self. _password_hash
            
        }
    def __repr__(self):
        return f'User {self.username}, ID: {self.id}'
