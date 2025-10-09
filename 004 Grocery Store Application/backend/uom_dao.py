def get_uoms(connection):

    cursor = None
    try:
        cursor = connection.cursor(buffered=True)
        
        query = "SELECT * FROM uom ORDER BY uom_name"
        
        cursor.execute(query)
        
        response = []
        for (uom_id, uom_name) in cursor:
            response.append({
                'uom_id': uom_id,
                'uom_name': uom_name
            })
        
        return response
        
    except Exception as e:
        print(f"Error in get_uoms: {e}")
        raise e
        
    finally:
        if cursor:
            cursor.close()

def get_uom_by_id(connection, uom_id):
    cursor = None
    try:
        cursor = connection.cursor(buffered=True)
        
        query = "SELECT * FROM uom WHERE uom_id = %s"
        cursor.execute(query, (uom_id,))
        
        row = cursor.fetchone()
        
        if row:
            return {
                'uom_id': row[0],
                'uom_name': row[1]
            }
        return None
        
    except Exception as e:
        print(f"Error getting UOM by ID: {e}")
        return None
        
    finally:
        if cursor:
            cursor.close()
