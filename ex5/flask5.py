from flask import Flask, jsonify
from webargs.flaskparser import use_kwargs
from webargs import fields
import sqlite3

app = Flask(__name__)


def connector():
    return sqlite3.connect('Chinook.sqlite')


@app.route("/order_price")
@use_kwargs(
    {
        "genre": fields.Str(required=True)
    },
    location="query"
)
def order_price(country):
    conn = connector()
    cursor = conn.cursor()
    query = """
        SELECT BillingCountry, SUM(UnitPrice * Quantity) AS TotalPrice 
        FROM Invoice
        JOIN InvoiceLine ON Invoice.InvoiceId = InvoiceLine.InvoiceId 
    """
    if country:
        query += "WHERE BillingCountry = ? "

    query += "GROUP BY BillingCountry"

    if country:
        cursor.execute(query, (country,))
    else:
        cursor.execute(query)

    results = cursor.fetchall()
    conn.close()

    data = [{"BillingCountry": row[0], "TotalPrice": row[1]} for row in results]

    return jsonify(data)





if __name__ == '__main__':
    app.run(port=5000, debug=True)
