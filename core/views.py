from django.shortcuts import render
import mysql.connector

def home(request):
    conn = mysql.connector.connect(
        host="localhost",
        user="ubuntu",
        password="root",
        database="nckh"
    )
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM web")
    total_link = cur.fetchone()[0]

    chart_data_pie = {
        "type": "pie",
        "labels": ['Total Links', "Remaining Links"],
        "values": [total_link, 100 - total_link]
    }

    cur.execute("SELECT YEAR(published), COUNT(*) FROM web GROUP BY YEAR(published)")
    rows = cur.fetchall()
    years = [str(row[0]) for row in rows]
    links_counts = [row[1] for row in rows]

    chart_data_bar = {
        "type": "bar",
        "labels": years,
        "values": links_counts
    }
    return render(request, 'core/index.html', {'chart_data_pie' : chart_data_pie, 'chart_data_bar' : chart_data_bar})