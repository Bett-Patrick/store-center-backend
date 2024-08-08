from flask import request,session,jsonify,make_response
from flask_restful import Resource
from config import app, db, api
from models.delivery import Delivery
from models.order import Order
from models.storage_slot import Storage_slot
from models.user import User
from models.unit import Unit



@app.route('/')
def index():
    return '<h1>Project Server</h1>'

class ClearSession(Resource):
    def delete(self):
        session.clear()
        return {}, 204

class OrderResource(Resource):
    def get(self):
       orders = Order.query.all()
       return make_response(jsonify([order.to_dict() for order in orders]), 200)
    
    def post(self):
        data = request.get_json()
        new_order = Order(
            user_id=data['user_id'],
            storage_slot_id=data['storage_slot_id'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            item=data['item'],  
            is_picked_up=data.get('is_picked_up', False),
            is_delivered=data.get('is_delivered', False)
        )
        db.session.add(new_order)
        db.session.commit()
        return make_response(jsonify(new_order.to_dict()), 201)

class OrderByID(Resource):
    def get(self, id):
        order = Order.query.get(id)
        if not order:
            ValueError(404, description="Order not found")
        return make_response(jsonify(order.to_dict()), 200)
    
    def patch(self, id):
        order = Order.query.get(id)
        if not order:
            ValueError(404, description="Order not found")
        
        data = request.get_json()
        if 'user_id' in data:
            order.user_id = data['user_id']
        if 'storage_slot_id' in data:
            order.storage_slot_id = data['storage_slot_id']
        if 'start_date' in data:
            order.start_date = data['start_date']
        if 'end_date' in data:
            order.end_date = data['end_date']
        if 'item' in data: 
            order.item = data['item']
        if 'is_picked_up' in data:
            order.is_picked_up = data['is_picked_up']
        if 'is_delivered' in data:
            order.is_delivered = data['is_delivered']
        
        db.session.commit()
        return make_response(jsonify(order.to_dict()), 200)

    def delete(self, id):
        order = Order.query.get(id)
        if not order:
            ValueError(404, description="Order not found")
        
        db.session.delete(order)
        db.session.commit()
        return '', 204

class DeliveryResource(Resource):
    def get(self):
        deliveries = Delivery.query.all()
        return make_response(jsonify([delivery.to_dict() for delivery in deliveries]), 200)
    
    
    def post(self):
        data = request.get_json()
        new_delivery = Delivery(
            order_id=data['order_id'],
            delivery_date=data['delivery_date'],
            delivery_address=data['delivery_address'],
            pickup_location=data['pickup_location']  
        )
        db.session.add(new_delivery)
        db.session.commit()
        return make_response(jsonify(new_delivery.to_dict()), 201)


class DeliveryByID(Resource):
    def get(self, id):
        delivery = Delivery.query.get(id)
        if not delivery:
            ValueError(404, description="Delivery not found")
        return make_response(jsonify(delivery.to_dict()), 200)
    
    def patch(self, id):
        delivery = Delivery.query.get(id)
        if not delivery:
            ValueError(404, description="Delivery not found")
        
        data = request.get_json()
        if 'order_id' in data:
            delivery.order_id = data['order_id']
        if 'delivery_date' in data:
            delivery.delivery_date = data['delivery_date']
        if 'delivery_address' in data:
            delivery.delivery_address = data['delivery_address']
        if 'pickup_location' in data:  # New field
            delivery.pickup_location = data['pickup_location']
        
        db.session.commit()
        return make_response(jsonify(delivery.to_dict()), 200)

    def delete(self, id):
        delivery = Delivery.query.get(id)
        if not delivery:
            ValueError(404, description="Delivery not found")
        
        db.session.delete(delivery)
        db.session.commit()
        return '', 204

class Storage_Slot(Resource):
    def get(self):
        slots = [slot.to_dict() for slot in Storage_slot.query.all()]
        return make_response(jsonify(slots), 200)
    
    
    def post(self):
        data = request.get_json()
        new_slot = Storage_slot(
            size=data['size'],
            price=data['price'],
            unit_details=data['unit_details'],
            what_can_fit=data['what_can_fit']
        )
        db.session.add(new_slot)
        db.session.commit()
        return make_response(jsonify(new_slot.to_dict()), 201)
    
class UnitResource (Resource):
    def get(self):
        units = Unit.query.all()
        return make_response(jsonify([unit.to_dict() for unit in units]), 200)
    
    def post(self):
        data = request.get_json()
        new_unit = Unit(
            
            features=data['features'],
            images=data['images'],
            storage_slot_id=data['storage_slot_id']
        )
        db.session.add(new_unit)
        db.session.commit()
        return make_response(jsonify(new_unit.to_dict()), 201)
    
class UnitByID(Resource):
    def get(self, id):
        unit = Unit.query.get(id)
        if not unit:
            ValueError(404, description="Unit not found")
        return make_response(jsonify(unit.to_dict()), 200)
    
    def patch(self, id):
        unit = Unit.query.get(id)
        if not unit:
            ValueError(404, description="Unit not found")
        
        data = request.get_json()
        if 'unit_number' in data:
            unit.unit_number = data['unit_number']
        if 'features' in data:
            unit.features = data['features']
        if 'images' in data:
            unit.images = data['images']
        if 'storage_slot_id' in data:
            unit.storage_slot_id = data['storage_slot_id']
        
        db.session.commit()
        return make_response(jsonify(unit.to_dict()), 200)

    def delete(self, id):
        unit = Unit.query.get(id)
        if not unit:
            response_dict = {"error": "Unit not found"}
            return make_response(jsonify(response_dict), 404)
            
        
        db.session.delete(unit)
        db.session.commit()
        return make_response(jsonify({"message": "Unit deleted successfully."}), 200)

class Storage_SlotByID(Resource):
    def get(self, id):
        storage_slot = Storage_slot.query.filter_by(id=id).first()
        if not storage_slot:
            response_dict = {"error": "Storage slot not found"}
            return make_response(jsonify(response_dict), 404)
        
        response_data = {
            'id': storage_slot.id,
            'size': storage_slot.size,
            'availability': storage_slot.availability,
            'price': storage_slot.price,
            'unit_details' : storage_slot.unit_details,
        }
        
        return make_response(jsonify(response_data), 200)

    def patch(self, id):
        storage_slot = Storage_slot.query.filter_by(id=id).first()
        if not storage_slot:
            response_dict = {"error": "Storage slot not found"}
            return make_response(jsonify(response_dict), 404)
        
        data = request.get_json()
        if 'availability' in data:
            storage_slot.availability = data['availability']
        if 'size' in data:
            storage_slot.size = data['size']
        if 'price' in data:
            storage_slot.price = data['price']
        
        try:
            db.session.commit()
            return make_response(jsonify({"message": "Storage slot updated successfully.", "slot": storage_slot.to_dict()}), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": "Failed to update storage slot.", "details": str(e)}), 400)

    def delete(self, id):
        storage_slot = Storage_slot.query.filter_by(id=id).first()
        if not storage_slot:
            response_dict = {"error": "Storage slot not found"}
            return make_response(jsonify(response_dict), 404)
        
        try:
            db.session.delete(storage_slot)
            db.session.commit()
            return make_response(jsonify({"message": "Storage slot deleted successfully."}), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": "Failed to delete storage slot.", "details": str(e)}), 400)

   

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')  
        user = User.query.filter(User.username == username).first()
        
        if user and user.authenticate(data['password']):
            session['user_id'] = user.id
            return user.to_dict(), 200
        
        return {}, 401
    


class Signup(Resource):
    
    def post(self):
        json = request.get_json()
        user = User(
            username=json['username'],
            email=json['email']
        )
        user.password_hash = json['password']
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201
 
class Logout(Resource):
    def delete(self):
        session.pop('user_id',None)
        return {},204

class CheckSession(Resource):
    def get(self):
        user_id = session['user_id']
        if user_id is not None:
            user = User.query.filter(User.id == user_id).first()
            if user is not None:
                return user.to_dict()
        
        return {},204
    
class UserResource(Resource):
    def get(self):
        users = User.query.all()
        return [user.to_dict() for user in users], 200

    def post(self):
        data = request.get_json()
        new_user = User(
            username=data['username'],
            email=data['email'],
            # password_hash=data['password'],
            phone_no= data['phone_no'],
            role= data['role']
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user.to_dict(), 201

    def patch(self, id):
        user = User.query.get(id)
        if not user:
            return {'error': 'User not found'}, 404

        data = request.get_json()
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.password_hash = data['password']

        db.session.commit()
        return user.to_dict(), 200

    def delete(self, id):
        user = User.query.get(id)
        if not user:
            return {'error': 'User not found'}, 404

        db.session.delete(user)
        db.session.commit()
        return {}, 204

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(OrderResource, '/orders')
api.add_resource(OrderByID, '/orders/<int:id>')
api.add_resource(UnitResource, '/units')
api.add_resource(UnitByID, '/units/<int:id>')

api.add_resource(DeliveryResource, '/deliveries')
api.add_resource(DeliveryByID, '/deliveries/<int:id>')
api.add_resource(Storage_Slot, '/storage_slots')
api.add_resource(Storage_SlotByID, '/storage_slots/<int:id>')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(UserResource, '/users', endpoint='users')

if __name__ == '__main__':
    app.run( debug=True)
