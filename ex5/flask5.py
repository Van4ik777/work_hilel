from flask import Flask, jsonify
from webargs import fields
from webargs.flaskparser import use_kwargs
from databasehandler import databasehandler as db
app = Flask(__name__)


@app.route('/order_price', methods=['GET'])
@use_kwargs(
    {
        "country": fields.Str(load_default=None)
    }, location="query"
)
def order_price(country):
    query = """
        SELECT BillingCountry, SUM(UnitPrice * Quantity) AS TotalPrice 
        FROM Invoice
        JOIN InvoiceLine ON Invoice.InvoiceId = InvoiceLine.InvoiceId 
    """
    if country:
        query += "WHERE BillingCountry = ? "

    query += "GROUP BY BillingCountry"

    if country:
        results = db.execute_query(query, (country,))
    else:
        results = db.execute_query(query)

    data = [{"BillingCountry": row[0], "TotalPrice": row[1]} for row in results]

    return jsonify(data)


@app.route('/get_city_by_genre', methods=['GET'])
@use_kwargs(
    {
        "genre": fields.Str(required=True)
    }, location="query"
)
def get_city_by_genre(genre):
    query = """
    SELECT BillingCity, PurchaseCount
    FROM (
        SELECT
            BillingCity,
            COUNT(*) AS PurchaseCount,
            RANK() OVER (ORDER BY COUNT(*) DESC) AS city_rank
        FROM Invoice
        JOIN InvoiceLine ON Invoice.InvoiceId = InvoiceLine.InvoiceId
        JOIN Track ON InvoiceLine.TrackId = Track.TrackId
        JOIN Genre ON Track.GenreId = Genre.GenreId
        WHERE Genre.Name = ?
        GROUP BY BillingCity
    ) AS RankedCities
    WHERE city_rank = 1;
    """

    results = db.execute_query(query, (genre,))


    if results:
        return jsonify({"cities": [{"city": row[0], "purchase_count": row[1]} for row in results]})
    else:
        return jsonify({"error": "Genre not found"})


if __name__ == '__main__':
    app.run(port=5000, debug=True)
