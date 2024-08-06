from flask import Flask, jsonify
from webargs.flaskparser import use_kwargs
from webargs import validate, fields
import sqlite3

app = Flask(__name__)

@app.route("/order_price")
@use_kwargs(
    {
        "country": fields.Str(load_default=None)
    },
    location="query"
)
def order_price(country):
    conn = sqlite3.connect('Chinook.sqlite')
    cursor = conn.cursor()
    query = ("""
        SELECT BillingCountry, SUM(UnitPrice * Quantity) AS TotalPrice FROM Invoice
        JOIN  InvoiceLine ON Invoice.InvoiceId = InvoiceLine.InvoiceId 
        """)
    if country:
        query += """WHERE BillingCountry = ?"""

    query += """GROUP BY BillingCountry"""

    if country:
        cursor.execute(query, (country,))
    else:
        cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return results


@app.route("/get_all_info_about_track")
@use_kwargs(
    {
        "track_id": fields.Int(min=1, max=500, min_inclusive=True, max_inclusive=True, missing=None)
    },
    location="query"
)
def get_all_info_about_track(track_id):
    conn = sqlite3.connect('Chinook.sqlite')
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

    query_get_all_time = """SELECT SUM(Milliseconds) AS totalTime From Track"""

    if track_id:
        cursor.execute(query, (track_id,))
        results = cursor.fetchall()
        conn.close()
        keys = ['TrackName', 'AlbumTitle', 'MediaTypeName', 'GenreName', 'Composer', 'Milliseconds', 'Bytes',
                'UnitPrice']
        data = [dict(zip(keys, entry)) for entry in results]
        return jsonify(data)
    else:
        cursor.execute(query_get_all_time)
        results = cursor.fetchone()[0]
        total_hours = results / (1000 * 60 * 60)
        conn.close()
        return jsonify({"TotalHours": total_hours})


if __name__ == '__main__':
    app.run(
        port=5000, debug=True
    )