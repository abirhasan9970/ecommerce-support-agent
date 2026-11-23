from database import get_connection

def track_order(order_id: str):
    """
    Searches the database for the given order_id.
    Returns the order details as a dictionary, or None if not found.
    """
    # Convert to uppercase to make search case-insensitive (e.g., ord-1001 -> ORD-1001)
    clean_order_id = order_id.strip().upper()

    with get_connection() as connection:
        cursor = connection.cursor()
        
        # Use parameterized query (?) to prevent SQL injection
        cursor.execute(
            "SELECT order_id, status, estimated_delivery, items_summary FROM orders WHERE order_id = ?", 
            (clean_order_id,)
        )
        row = cursor.fetchone()

        if row is None:
            return None
            
        # Convert the sqlite3.Row object to a standard Python dictionary
        return {
            "order_id": row["order_id"],
            "status": row["status"],
            "estimated_delivery": row["estimated_delivery"] or "Not available yet",
            "items_summary": row["items_summary"]
        }
