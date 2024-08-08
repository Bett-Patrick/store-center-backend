from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from flask_bcrypt import Bcrypt
from config import db


class Delivery(db.Model, SerializerMixin):
    __tablename__ = 'delivery'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    delivery_date = db.Column(db.Date, nullable=False)
    delivery_address = db.Column(db.String(100), nullable=False)
    pickup_location = db.Column(db.String(100))
    order = db.relationship("Order", back_populates="deliveries")

    
  

    serialize_only = ('id', 'order_id', 'delivery_date', 'delivery_address', 'pickup_location')

    def __init__(self, order_id, delivery_date, delivery_address, pickup_location=None):
        self.order_id = order_id
        self.delivery_date = delivery_date
        self.delivery_address = delivery_address
        self.pickup_location = pickup_location
        
        
    def __repr__(self):
        return (f"<Delivery id={self.id}, order_id={self.order_id}, delivery_date={self.delivery_date}, "
                f"delivery_address={self.delivery_address}, pickup_location={self.pickup_location}>")

    def to_dict(self):
        delivery_dict = super().to_dict()
        delivery_dict['order'] = self.order.to_dict()
        return delivery_dict
        
        
       
    