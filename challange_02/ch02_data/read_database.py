import duckdb

# Connection to the database file called 'library.db'
con = duckdb.connect("ch02_data/library.db")

show_tables = """
    SELECT * FROM pg_catalog.pg_tables;
"""

# See an output of all the tables
con.sql(show_tables).show()

# Load the sql_query and run it
fd = open('ch02_data/customers_with_late_fees.sql', 'r')
sql_query = fd.read()
fd.close()

con.sql(sql_query).show()

# explicitly close the connection
con.close()
