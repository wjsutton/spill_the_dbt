import duckdb
import pandas

# Connection to the database file called 'library.db'
con = duckdb.connect("data/library.db")



# Load the sql_query and run it
fd = open('data/customers_with_late_fees.sql', 'r')
sql_query = fd.read()
fd.close()

sql_query = """
    SELECT book_id FROM main.stg_books GROUP BY book_id HAVING (COUNT(*)>1);
"""

#con.sql(sql_query).show()




# show_data = """
#     COPY customers_with_late_fees TO 'data/late_fees.csv' (HEADER, DELIMITER ',');
# """

# con.sql(show_data)


# show_data = """
#     COPY solution TO 'data/sol_maybe.csv' (HEADER, DELIMITER ',');
# """

show_data = """
    SELECT COUNT(*) FROM solution;
"""

con.sql(show_data).show()

show_data = """
    SELECT COUNT(*) FROM customers_with_late_fees;
"""

con.sql(show_data).show()

show_data = """
    COPY customers_with_late_fees TO 'data/sol_maybe.csv' (HEADER, DELIMITER ',');
"""
con.sql(show_data)

show_data = """
    DROP TABLE solution;
"""
con.sql(show_data)

show_tables = """
    SELECT * FROM pg_catalog.pg_tables;
"""

# See an output of all the tables
con.sql(show_tables).show()

#late_fees_df.to_csv('late_fees.csv', index=False, encoding='utf-8')

# explicitly close the connection
con.close()