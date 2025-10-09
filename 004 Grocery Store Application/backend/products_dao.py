
from datetime import datetime

def get_all_products(connection):

    cursor = None
    try:
        cursor = connection.cursor(buffered=True)
        
        query = """
            SELECT 
                products.product_id, 
                products.name, 
                products.uom_id, 
                products.price_per_unit,
                uom.uom_name 
            FROM products 
            INNER JOIN uom ON products.uom_id = uom.uom_id
            ORDER BY products.name
        """
        
        cursor.execute(query)
        
        response = []
        for (product_id, name, uom_id, price_per_unit, uom_name) in cursor:
            response.append({
                'product_id': product_id,
                'name': name,
                'uom_id': uom_id,
                'price_per_unit': float(price_per_unit),
                'uom_name': uom_name
            })
        
        return response
        
    except Exception as e:
        print(f"Error in get_all_products: {e}")
        raise e
        
    finally:
        if cursor:
            cursor.close()

def insert_new_product(connection, product):

    cursor = None
    try:
        cursor = connection.cursor(buffered=True)
        
        query = """
            INSERT INTO products (name, uom_id, price_per_unit) 
            VALUES (%s, %s, %s)
        """
        
        data = (product['product_name'], product['uom_id'], product['price_per_unit'])
        
        cursor.execute(query, data)
        connection.commit()
        
        product_id = cursor.lastrowid
        return product_id
        
    except Exception as e:
        print(f"Error inserting product: {e}")
        connection.rollback()
        return -1
        
    finally:
        if cursor:
            cursor.close()

def delete_product(connection, product_id):

    cursor = None
    try:
        cursor = connection.cursor(buffered=True)
        
        query = "DELETE FROM products WHERE product_id = %s"
        
        cursor.execute(query, (product_id,))
        connection.commit()
        
        return True
        
    except Exception as e:
        print(f"Error deleting product: {e}")
        connection.rollback()
        return False
        
    finally:
        if cursor:
            cursor.close()

def update_product(connection, product):
    cursor = None
    try:
        cursor = connection.cursor(buffered=True)
        
        query = """
            UPDATE products 
            SET name = %s, uom_id = %s, price_per_unit = %s 
            WHERE product_id = %s
        """
        
        data = (
            product['product_name'], 
            product['uom_id'], 
            product['price_per_unit'], 
            product['product_id']
        )
        
        cursor.execute(query, data)
        connection.commit()
        
        return True
        
    except Exception as e:
        print(f"Error updating product: {e}")
        connection.rollback()
        return False
        
    finally:
        if cursor:
            cursor.close()

def get_product_by_id(connection, product_id):
    cursor = None
    try:
        cursor = connection.cursor(buffered=True)
        
        query = """
            SELECT 
                products.product_id, 
                products.name, 
                products.uom_id, 
                products.price_per_unit,
                uom.uom_name 
            FROM products 
            INNER JOIN uom ON products.uom_id = uom.uom_id
            WHERE products.product_id = %s
        """
        
        cursor.execute(query, (product_id,))
        row = cursor.fetchone()
        
        if row:
            return {
                'product_id': row[0],
                'name': row[1],
                'uom_id': row[2],
                'price_per_unit': float(row[3]),
                'uom_name': row[4]
            }
        return None
        
    except Exception as e:
        print(f"Error getting product by ID: {e}")
        return None
        
    finally:
        if cursor:
            cursor.close()
