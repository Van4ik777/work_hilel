import sqlite3


def connector():
    return sqlite3.connect('Chinook.sqlite')


def result_and_close(cursor, conn):
    results = cursor.fetchall()
    conn.close()
    return results


def execute_query(query, params=()):
    conn = connector()
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = result_and_close(cursor, conn)
    return results


def execute_query_fetchone(query, params=()):
    conn = connector()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchone()
    conn.close()
    return result
