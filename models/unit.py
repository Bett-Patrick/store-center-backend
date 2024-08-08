from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from config import db
from sqlalchemy_serializer import SerializerMixin

class Unit(db.Model, SerializerMixin):
    __tablename__ = 'unit'
    id = Column(Integer, primary_key=True)
    unit_number = Column(String(10), nullable=False)
    features = Column(JSON, nullable=False)
    images = Column(JSON, nullable=True)
    storage_slot_id = Column(Integer, ForeignKey('storage_slot.id'), nullable=False)
    
    
    storage_slot = relationship("Storage_slot", back_populates="units")
    
    serialize_only = ('id', 'unit_number', 'features', 'images', 'storage_slot_id')

    
    
    def __init__(self, unit_number, features, images, storage_slot_id):
        self.unit_number = unit_number
    
        self.features = features
        self.images = images
        self.storage_slot_id = storage_slot_id
    def to_dict(self):
        unit_dict = super().to_dict()
        unit_dict['storage_slot'] = self.storage_slot.to_dict()
        return unit_dict
