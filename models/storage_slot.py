from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from sqlalchemy import Integer, ForeignKey, Date, Boolean, String
from flask_bcrypt import Bcrypt
from config import db
import json

class Storage_slot(db.Model, SerializerMixin):
    _tablename_ = 'storage_slot'
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(10), nullable=False)
    square_feet = db.Column(db.Integer, nullable=False)
    availability = db.Column(Boolean, default=True)
    price = db.Column(db.Integer)
    unit_details = db.Column(db.JSON, nullable=False)
    what_can_fit = db.Column(db.JSON, nullable=False)

    units = db.relationship("Unit", back_populates="storage_slot", cascade="all, delete-orphan")

    serialize_only = ('id', 'size', 'square_feet', 'price', 'availability', 'unit_details_str', 'what_can_fit_str')
    
    orders = db.relationship("Order",back_populates= "storage_slot",cascade="all, delete-orphan")
  
    @validates('availability')
    def validate_availability(self, key, value):
        if value is None:
            return True
        return value

    @hybrid_property
    def unit_details_str(self):
        return json.dumps(self.unit_details)

    @hybrid_property
    def what_can_fit_str(self):
        return json.dumps(self.what_can_fit)

    def _init_(self, size, square_feet, price, what_can_fit, unit_details):
        self.size = size
        self.square_feet = square_feet
        self.price = price
        self.unit_details = unit_details
        self.what_can_fit = what_can_fit
    def to_dict(self):
        return {
            'id': self.id,
            'size': self.size,
            'square_feet': self.square_feet,
            'price': self.price,
            'availability': self.availability,
            'unit_details': self.unit_details,
            'what_can_fit': self.what_can_fit
        }