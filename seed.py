#!/usr/bin/env python3
# Standard library imports
from random import randint, choice as rc
from datetime import datetime, timedelta
import random
# Remote library imports
from faker import Faker
# Local imports
from app import app, db
from models.delivery import Delivery
from models.order import Order
from models.storage_slot import Storage_slot
from models.unit import Unit  # Ensure this path matches your project structure
from models.user import User

fake = Faker()

def seed_storage_slots(num_slots=50):
    slot_sizes = {
        "small": {
            "dimensions": ["5'x5'", "5'x10'", "5'x15'"],
            "what_can_fit": [
                "Small items like bags, suitcases, and boxes",
                "Contents of a small one-bedroom apartment",
                "Seasonal decorations",
                "Sports equipment"
            ]
        },
        "medium": {
            "dimensions": ["10'x10'", "10'x15'", "10'x20'"],
            "what_can_fit": [
                "Furniture from a one or two-bedroom apartment",
                "Appliances",
                "Large boxes",
                "Seasonal items and sports equipment"
            ]
        },
        "large": {
            "dimensions": ["15'x15'", "20'x20'", "20'x25'"],
            "what_can_fit": [
                "Contents of a three to four-bedroom house",
                "Major appliances",
                "Large furniture items",
                "Large boxes",
                "Commercial inventory"
            ]
        }
    }

    slots = []
    for _ in range(num_slots):
        size = random.choice(list(slot_sizes.keys()))
        dimension = random.choice(slot_sizes[size]["dimensions"])

        try:
            width, length = map(int, dimension.replace("'", "").split('x'))
            square_feet = width * length
        except ValueError:
            print(f"Error processing dimensions: {dimension}")
            continue

        slot = Storage_slot(
            size=size,
            square_feet=square_feet,
            price=random.randint(50, 200),
            unit_details={"squareFeet": square_feet, "size": dimension},
            what_can_fit=slot_sizes[size]["what_can_fit"],
            availability=True
        )
        slots.append(slot)
        db.session.add(slot)
    db.session.commit()
    return slots

def seed_units(storage_slots):
    features_pool = [
        ["Climate controlled", "24/7 access", "Ground floor"],
        ["Climate controlled", "24/7 access", "Drive-up access"],
        ["Climate controlled", "24/7 access", "Ground floor", "Drive-up access", "Security cameras"]
    ]
    units = []
    for slot in storage_slots:
        for i in range(randint(1, 5)):
            unit = Unit(
                unit_number=f"{slot.size[0].upper()}{random.randint(100, 999)}",
                features=random.choice(features_pool),
                images=[f"https://example.com/images/{slot.size}-{slot.square_feet}sqft-unit-{i+1}.jpg"],
                storage_slot_id=slot.id
            )
            units.append(unit)
            db.session.add(unit)
    db.session.commit()
    return units

def seed_users(num_users=50):
    users = []
    for _ in range(num_users):
        role = rc(["admin", "client", "employee"])
        phone_no = fake.bothify(text='########') 
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            role=role,
            phone_no=phone_no,
            password="password" 
        )
        users.append(user)
        db.session.add(user)
    db.session.commit()
    return users



def seed_orders(num_orders=50):
    users = User.query.all()
    if not users:
        print("No users found, skipping orders seeding")
        return

    slots = Storage_slot.query.all()
    if not slots:
        print("No storage slots found, skipping orders seeding")
        return

    items = ["TV", "Food", "Furniture", "Clothing", "Electronics", "Books", "Toys", "Appliances", "Tools", "Sports Equipment"]

    for _ in range(num_orders):
        start_date = datetime.now() - timedelta(days=random.randint(1, 30))
        end_date = start_date + timedelta(days=random.randint(1, 30))
        user = random.choice(users)
        storage_slot = random.choice(slots)
        item = random.choice(items)
        order = Order(
            user_id=user.id,
            storage_slot_id=storage_slot.id,
            start_date=start_date,
            end_date=end_date,
            item=item,
            is_picked_up=False,
            is_delivered=False
        )
        db.session.add(order)
    db.session.commit()

def seed_deliveries(num_deliveries=20):
    orders = Order.query.all()
    if not orders:
        print("No orders found, skipping deliveries seeding")
        return

    deliveries = []
    for _ in range(num_deliveries):
        delivery_date = datetime.now() + timedelta(days=randint(1, 30))
        order = random.choice(orders)
        delivery = Delivery(
            order_id=order.id,
            delivery_date=delivery_date,
            delivery_address="Nairobi",
            pickup_location=fake.address()
        )
        deliveries.append(delivery)
        db.session.add(delivery)
    db.session.commit()
    return deliveries

if __name__ == '__main__':
    with app.app_context():
        print("Clearing db...")
        Delivery.query.delete()
        Order.query.delete()
        Unit.query.delete()
        Storage_slot.query.delete()
        User.query.delete()

        print("Starting seed...")
        print("Seeding storage slots...")
        storage_slots = seed_storage_slots()
        print("Seeding units...")
        units = seed_units(storage_slots)
        print("Seeding users...")
        users = seed_users()
        print("Seeding orders...")
        orders = seed_orders()
        print("Seeding deliveries...")
        deliveries = seed_deliveries()
        print("Seed completed successfully!")