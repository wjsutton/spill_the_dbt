import duckdb

# Connection to the database file called 'lego.db'
con = duckdb.connect("data/office_weather.db")

show_tables = """
    SELECT * FROM pg_catalog.pg_tables;
"""

# See an output of all the tables
con.sql(show_tables).show()

show_tables = """
    SELECT * FROM all_weather_readings;
"""

# See an output of all the tables
con.sql(show_tables).show()

# explicitly close the connection
con.close()