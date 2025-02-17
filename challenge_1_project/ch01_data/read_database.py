import duckdb

# Connection to the database file called 'lego.db'
con = duckdb.connect("ch01_data/lego.db")

show_tables = """
    SELECT * FROM pg_catalog.pg_tables;
"""

# See an output of all the tables
con.sql(show_tables).show()

# Load the sql_query and run it
fd = open('ch01_data/ch01_sql_script.sql', 'r')
sql_query = fd.read()
fd.close()

con.sql(sql_query).show()

# explicitly close the connection
con.close()