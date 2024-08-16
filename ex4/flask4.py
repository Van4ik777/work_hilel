from flask import Flask, jsonify
from webargs.flaskparser import use_kwargs
from webargs import validate, fields
import sqlite3

app = Flask(__name__)


def connector():
    return sqlite3.connect('Chinook.sqlite')


@app.route("/order_price")
def order_price():
    conn = connector()
    cursor = conn.cursor()

    query = """
        SELECT BillingCountry, SUM(UnitPrice * Quantity) AS TotalPrice 
        FROM Invoice
        JOIN InvoiceLine ON Invoice.InvoiceId = InvoiceLine.InvoiceId 
        GROUP BY BillingCountry
    """

    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    data = [{"BillingCountry": row[0], "TotalPrice": row[1]} for row in results]

    return jsonify(data)

@app.route("/order_price_by_country")
@use_kwargs(
    {
        "country": fields.Str(required=True)
    },
    location="query"
)
def order_price_by_country(country):
    conn = connector()
    cursor = conn.cursor()

    query = """
        SELECT BillingCountry, SUM(UnitPrice * Quantity) AS TotalPrice 
        FROM Invoice
        JOIN InvoiceLine ON Invoice.InvoiceId = InvoiceLine.InvoiceId 
        WHERE BillingCountry = ?
        GROUP BY BillingCountry
    """

    cursor.execute(query, (country,))
    result = cursor.fetchone()
    conn.close()

    if result:
        data = {"BillingCountry": result[0], "TotalPrice": result[1]}
    else:
        data = {"error": "Country not found"}

    return jsonify(data)

@app.route("/get_all_info_about_track")
@use_kwargs(
    {
        "track_id": fields.Int(validate=validate.Range(min=1, max=500), missing=None)
    },
    location="query"
)
def get_all_info_about_track(track_id):
    conn = connector()
    cursor = conn.cursor()
    query = """
        SELECT
            Track.Name AS TrackName,
            Album.Title AS AlbumTitle,
            MediaType.Name AS MediaTypeName,
            Genre.Name AS GenreName,
            Track.Composer,
            Track.Milliseconds,
            Track.Bytes,
            Track.UnitPrice
        FROM Track
        JOIN Album ON Track.AlbumId = Album.AlbumId
        JOIN MediaType ON Track.MediaTypeId = MediaType.MediaTypeId
        JOIN Genre ON Track.GenreId = Genre.GenreId
        WHERE Track.TrackId = ?
    """

    if track_id:
        cursor.execute(query, (track_id,))
        results = cursor.fetchall()
        conn.close()
        keys = ['TrackName', 'AlbumTitle', 'MediaTypeName', 'GenreName', 'Composer', 'Milliseconds', 'Bytes',
                'UnitPrice']
        data = [dict(zip(keys, entry)) for entry in results]
        return jsonify(data)

    query_get_all_time = """SELECT SUM(Milliseconds) AS totalTime FROM Track"""
    cursor.execute(query_get_all_time)

    results = cursor.fetchone()[0]
    total_hours = results / (1000 * 60 * 60)

    conn.close()
    return jsonify({"TotalHours": total_hours})


if __name__ == '__main__':
    app.run(port=5000, debug=True)
