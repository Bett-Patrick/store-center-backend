from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from sqlalchemy import Integer, ForeignKey, Date, Boolean
from flask_bcrypt import Bcrypt
from config import db

bcrypt = Bcrypt()

class Order(db.Model, SerializerMixin):
    __tablename__ = 'order'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    storage_slot_id = db.Column(db.Integer, db.ForeignKey('storage_slot.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    is_picked_up = db.Column(Boolean, default=False, nullable=False)
    is_delivered = db.Column(Boolean, default=False, nullable=False)
    item = db.Column(db.String, nullable=False)
    
    deliveries = db.relationship('Delivery', backref='order')
    
    serialize_only = ('id', 'user_id', 'storage_slot_id', 'start_date', 'end_date', 'is_picked_up', 'is_delivered', 'item')
    
    storage_slot = db.relationship("Storage_slot", back_populates="orders")
    user = db.relationship("User",back_populates="orders")
    deliveries = db.relationship("Delivery", back_populates="order", cascade="all, delete-orphan")
    
    def __init__(self, user_id, storage_slot_id, start_date, end_date, item, is_picked_up, is_delivered):
        self.user_id = user_id
        self.storage_slot_id = storage_slot_id
        self.start_date = start_date
        self.end_date = end_date
        self.item = item
        self.is_picked_up = is_picked_up
        self.is_delivered = is_delivered

    def to_dict(self):
        order_dict = super().to_dict()
        order_dict['storage_slot'] = self.storage_slot.to_dict()
        order_dict['user'] = self.user.to_dict()
        return order_dict
