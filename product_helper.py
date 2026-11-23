from database import get_connection

def recommend_products(max_price: float, category: str = None):
    """
    Searches the database for products within the budget.
    Optionally filters by category.
    """
    with get_connection() as connection:
        cursor = connection.cursor()
        
        query = "SELECT name, category, price, specifications FROM products WHERE price <= ?"
        params = [max_price]
        
        if category and category.strip().lower() != "any":
            query += " AND LOWER(category) = ?"
            params.append(category.strip().lower())
            
        query += " ORDER BY price ASC"
        
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        
        products = []
        for row in rows:
            products.append({
                "name": row["name"],
                "category": row["category"],
                "price": row["price"],
                "specifications": row["specifications"]
            })
            
        return products
