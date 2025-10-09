

from datetime import datetime

def insert_order(connection, order):

    cursor = None
    try:
        cursor = connection.cursor(buffered=True)
        
        # Insert main order
        order_query = """
            INSERT INTO orders (customer_name, total, datetime) 
            VALUES (%s, %s, %s)
        """
        
        order_data = (order['customer_name'], order['grand_total'], datetime.now())
        
        cursor.execute(order_query, order_data)
        order_id = cursor.lastrowid
        
        # Insert order details
        order_details_query = """
            INSERT INTO order_details (order_id, product_id, quantity, total_price) 
            VALUES (%s, %s, %s, %s)
        """
        
        order_details_data = []
        for order_detail_record in order['order_details']:
            order_details_data.append([
                order_id,
                int(order_detail_record['product_id']),
                float(order_detail_record['quantity']),
                float(order_detail_record['total_price'])
            ])
        
        cursor.executemany(order_details_query, order_details_data)
        connection.commit()
        
        return order_id
        
    except Exception as e:
        print(f"Error inserting order: {e}")
        connection.rollback()
        return -1
        
    finally:
        if cursor:
            cursor.close()

def get_all_orders(connection):
    cursor = None
    try:
        cursor = connection.cursor(buffered=True)
        
        query = """
            SELECT 
                order_id, 
                customer_name, 
                total, 
                datetime 
            FROM orders 
            ORDER BY datetime DESC
        """
        
        cursor.execute(query)
        
        response = []
        for (order_id, customer_name, total, dt) in cursor:
            response.append({
                'order_id': order_id,
                'customer_name': customer_name,
                'total': float(total),
                'datetime': dt.strftime("%Y-%m-%d %H:%M:%S") if dt else None
            })
        
        return response
        
    except Exception as e:
        print(f"Error in get_all_orders: {e}")
        raise e
        
    finally:
        if cursor:
            cursor.close()

def get_order_details(connection, order_id):

    cursor = None
    try:
        cursor = connection.cursor(buffered=True)
        
        query = """
            SELECT 
                od.order_id,
                od.quantity,
                od.total_price,
                p.name,
                p.price_per_unit,
                u.uom_name
            FROM order_details od
            JOIN products p ON od.product_id = p.product_id
            JOIN uom u ON p.uom_id = u.uom_id
            WHERE od.order_id = %s
        """
        
        cursor.execute(query, (order_id,))
        
        response = []
        for (order_id, quantity, total_price, product_name, price_per_unit, uom_name) in cursor:
            response.append({
                'order_id': order_id,
                'quantity': float(quantity),
                'total_price': float(total_price),
                'product_name': product_name,
                'price_per_unit': float(price_per_unit),
                'uom_name': uom_name
            })
        
        return response
        
    except Exception as e:
        print(f"Error in get_order_details: {e}")
        raise e
        
    finally:
        if cursor:
            cursor.close()

def delete_order(connection, order_id):

    cursor = None
    try:
        cursor = connection.cursor(buffered=True)
        
        # Delete order details first
        query1 = "DELETE FROM order_details WHERE order_id = %s"
        cursor.execute(query1, (order_id,))
        
        # Then delete the main order
        query2 = "DELETE FROM orders WHERE order_id = %s"
        cursor.execute(query2, (order_id,))
        
        connection.commit()
        
        return True
        
    except Exception as e:
        print(f"Error deleting order: {e}")
        connection.rollback()
        return False
        
    finally:
        if cursor:
            cursor.close()
