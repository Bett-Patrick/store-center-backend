
# STORE-CENTER



## Project Overview
The Storage Center Management System is a web application designed to manage storage facilities. It allows users to create and manage storage slots, orders, and users. The application is built using a combination of React, Tailwind CSS for the frontend, Node.js for the backend server, Flask for the API, and PostgreSQL for the database.

## Features
- User authentication and authorization
- CRUD operations for storage slots, orders,units and  delivery
- Real-time availability tracking of storage slots
- Responsive UI built with React and Tailwind CSS

## Technologies Used
- **Frontend:** React, Tailwind CSS
- **Backend:** Node.js, Flask
- **Database:** PostgreSQL


### Entities:

1. **User**: Represents users of the system.
   - Attributes: `user_id` (primary key), `username`, `email`, `password`, 'phone_no',etc.

2. **Unit**: Represents units available for order.
   - Attributes: `unit_id` (primary key), `unit_number`, `features`, `images`, `storage_slot_id`, etc.

3. **Order**: Represents orders where items are ordered.
   - Attributes: `order_id` (primary key), `storage_slot_id`, `user_id`, `item `, etc.

4.   **Deliveries**: Represent the transactions where users order specific items to be delivered from the storage center. Each delivery record keeps track of the essential details regarding the delivery process.
 - Attributes: `delivery_id` (primary key), `price`, `user_id`, `item `, etc.

5. **Storage Slot** represents a specific storage unit or compartment within the storage center where items can be stored. Each storage slot has attributes that define its characteristics and current status.
 - Attributes: `storage_slot_id' (primary key), `storage_slot_id`, `availability`, `size `, etc.


## Usage
Once the backend (Flask and Node.js servers) and the frontend (React) are running, you can access the application by navigating to `http://localhost:3000` in your web browser.