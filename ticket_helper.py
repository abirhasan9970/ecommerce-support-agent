import uuid
from datetime import datetime
from database import get_connection

def create_support_ticket(customer_name: str, message: str, issue_type: str):
    ticket_id = "TKT-" + str(uuid.uuid4())[:8].upper()
    created_at = datetime.now().isoformat()
    status = "Open"

    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO tickets (ticket_id, customer_name, message, issue_type, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (ticket_id, customer_name, message, issue_type, status, created_at)
        )
        connection.commit()

    return ticket_id
