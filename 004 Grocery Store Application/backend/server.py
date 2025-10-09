

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import traceback

import sql_connection
import products_dao
import orders_dao
import uom_dao


app = Flask(__name__)

# Enable CORS
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})


@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
        return response, 200

# Initialize connection pool
print("="*50)
print("Initializing Grocery Store Flask Server...")
print("="*50)

sql_connection.initialize_connection_pool()


@app.route('/getProducts', methods=['GET'])
def get_products():
    """Get all products"""
    connection = None
    try:
        connection = sql_connection.get_sql_connection()
        if connection is None:
            return jsonify({'error': 'Database connection failed'}), 500
            
        products = products_dao.get_all_products(connection)
        print(f"✓ Retrieved {len(products)} products")
        return jsonify(products), 200
        
    except Exception as e:
        print(f"✗ Error in /getProducts: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
        
    finally:
        if connection:
            sql_connection.close_connection(connection)

@app.route('/insertProduct', methods=['POST'])
def insert_product():
    """Add a new product"""
    connection = None
    try:
        connection = sql_connection.get_sql_connection()
        if connection is None:
            return jsonify({'error': 'Database connection failed'}), 500
            
        request_payload = json.loads(request.form['data'])
        print(f"Inserting product: {request_payload}")
        
        product_id = products_dao.insert_new_product(connection, request_payload)
        
        if product_id > 0:
            print(f"✓ Product inserted with ID: {product_id}")
            return jsonify({
                'product_id': product_id,
                'message': 'Product added successfully!'
            }), 200
        else:
            return jsonify({'error': 'Failed to insert product'}), 500
            
    except Exception as e:
        print(f"✗ Error in /insertProduct: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
        
    finally:
        if connection:
            sql_connection.close_connection(connection)

@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    """Delete a product"""
    connection = None
    try:
        connection = sql_connection.get_sql_connection()
        if connection is None:
            return jsonify({'error': 'Database connection failed'}), 500
            
        product_id = request.form['product_id']
        print(f"Deleting product ID: {product_id}")
        
        success = products_dao.delete_product(connection, product_id)
        
        if success:
            print(f"✓ Product {product_id} deleted")
            return jsonify({'message': 'Product deleted successfully!'}), 200
        else:
            return jsonify({'error': 'Failed to delete product'}), 500
            
    except Exception as e:
        print(f"✗ Error in /deleteProduct: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
        
    finally:
        if connection:
            sql_connection.close_connection(connection)

@app.route('/updateProduct', methods=['POST'])
def update_product():
    """Update a product"""
    connection = None
    try:
        connection = sql_connection.get_sql_connection()
        if connection is None:
            return jsonify({'error': 'Database connection failed'}), 500
            
        request_payload = json.loads(request.form['data'])
        print(f"Updating product: {request_payload}")
        
        success = products_dao.update_product(connection, request_payload)
        
        if success:
            print(f"✓ Product updated")
            return jsonify({'message': 'Product updated successfully!'}), 200
        else:
            return jsonify({'error': 'Failed to update product'}), 500
            
    except Exception as e:
        print(f"✗ Error in /updateProduct: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
        
    finally:
        if connection:
            sql_connection.close_connection(connection)


@app.route('/getUOM', methods=['GET'])
def get_uom():
    """Get all units of measurement"""
    connection = None
    try:
        connection = sql_connection.get_sql_connection()
        if connection is None:
            return jsonify({'error': 'Database connection failed'}), 500
            
        uoms = uom_dao.get_uoms(connection)
        print(f"✓ Retrieved {len(uoms)} UOMs")
        return jsonify(uoms), 200
        
    except Exception as e:
        print(f"✗ Error in /getUOM: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
        
    finally:
        if connection:
            sql_connection.close_connection(connection)



@app.route('/insertOrder', methods=['POST'])
def insert_order():
    """Create a new order"""
    connection = None
    try:
        connection = sql_connection.get_sql_connection()
        if connection is None:
            return jsonify({'error': 'Database connection failed'}), 500
            
        request_payload = json.loads(request.form['data'])
        print(f"Inserting order: {request_payload}")
        
        order_id = orders_dao.insert_order(connection, request_payload)
        
        if order_id > 0:
            print(f"✓ Order inserted with ID: {order_id}")
            return jsonify({
                'order_id': order_id,
                'message': 'Order placed successfully!'
            }), 200
        else:
            return jsonify({'error': 'Failed to insert order'}), 500
            
    except Exception as e:
        print(f"✗ Error in /insertOrder: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
        
    finally:
        if connection:
            sql_connection.close_connection(connection)

@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    """Get all orders"""
    connection = None
    try:
        connection = sql_connection.get_sql_connection()
        if connection is None:
            return jsonify({'error': 'Database connection failed'}), 500
            
        orders = orders_dao.get_all_orders(connection)
        print(f"✓ Retrieved {len(orders)} orders")
        return jsonify(orders), 200
        
    except Exception as e:
        print(f"✗ Error in /getAllOrders: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
        
    finally:
        if connection:
            sql_connection.close_connection(connection)

@app.route('/getOrderDetails', methods=['POST'])
def get_order_details():
    """Get details of a specific order"""
    connection = None
    try:
        connection = sql_connection.get_sql_connection()
        if connection is None:
            return jsonify({'error': 'Database connection failed'}), 500
            
        order_id = request.form['order_id']
        print(f"Fetching details for order ID: {order_id}")
        
        order_details = orders_dao.get_order_details(connection, order_id)
        print(f"✓ Retrieved {len(order_details)} order items")
        return jsonify(order_details), 200
        
    except Exception as e:
        print(f"✗ Error in /getOrderDetails: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
        
    finally:
        if connection:
            sql_connection.close_connection(connection)

@app.route('/deleteOrder', methods=['POST'])
def delete_order():
    """Delete an order"""
    connection = None
    try:
        connection = sql_connection.get_sql_connection()
        if connection is None:
            return jsonify({'error': 'Database connection failed'}), 500
            
        order_id = request.form['order_id']
        print(f"Deleting order ID: {order_id}")
        
        success = orders_dao.delete_order(connection, order_id)
        
        if success:
            print(f"✓ Order {order_id} deleted")
            return jsonify({'message': 'Order deleted successfully!'}), 200
        else:
            return jsonify({'error': 'Failed to delete order'}), 500
            
    except Exception as e:
        print(f"✗ Error in /deleteOrder: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
        
    finally:
        if connection:
            sql_connection.close_connection(connection)

# ==================== UTILITY ENDPOINTS ====================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check"""
    connection = None
    try:
        connection = sql_connection.get_sql_connection()
        db_status = "connected" if connection and connection.is_connected() else "disconnected"
    except:
        db_status = "error"
    finally:
        if connection:
            sql_connection.close_connection(connection)
    
    return jsonify({
        'status': 'Server is running!',
        'database': db_status,
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/', methods=['GET'])
def home():
    """Home/Welcome"""
    return jsonify({
        'message': 'Welcome to Grocery Store API!',
        'version': '1.0',
        'endpoints': {
            'products': '/getProducts',
            'orders': '/getAllOrders',
            'uom': '/getUOM',
            'health': '/health'
        }
    }), 200

# Start the Flask server
if __name__ == "__main__":
    print("="*50)
    print("Starting Grocery Store Flask Server...")
    print("Server will run on: http://127.0.0.1:5000")
    print("="*50)
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(host='127.0.0.1', port=5000, debug=True)
