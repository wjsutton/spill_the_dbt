# Spill the dbt Challenge 02: Library Loan Issues 

## Objective
Identify and fix issues in a dbt model that aggregates late fees for overdue library loans by writing and running tests. Compare the fixed model's output with a provided CSV seed using the dbt-utils package.

## Prerequisites
- Python installed
- Necessary packages installed from `requirements.txt`
- Basic knowledge of SQL and dbt

## Steps to Complete the Challenge

### Step 1: Navigate to the "spill_the_dbt" Folder

Open your terminal and navigate to the `spill_the_dbt` directory in your working directory:
```
cd spill_the_dbt
```

### Step 2: Initialize a dbt Project

Execute the following command to initialize a new dbt project called challenge_02:
```
dbt init challenge_02
```
When prompted, select `duckdb` as your database.

### Step 3: Move the Data Folder

Move the `ch02_data` folder located in the `requirements` directory to your dbt project folder `challenge_02`:
```
mkdir challenge_02/data
cp requirements/ch02_data/* challenge_02/data
```
inspect the data in the library.db with the Python script `read_database.py`

### Step 4: Configure Your profiles.yml

Edit the `profiles.yml` file in the `.dbt` folder, typically found `C:\Users\username\.dbt` to point to the `library.db` file within the `data` folder:

```
challenge_02:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: "data/library.db"
```

### Step 5: Create a New Model

In your `challenge_02` dbt project, create a new model named `library_loans` and move the provided SQL script (`customers_with_late_fees.sql`) to this model folder:

```
mkdir -p models/library_loans
cp data/customers_with_late_fees.sql models/library_loans/customers_with_late_fees.sql
```

### Step 6: Configure the Model in `dbt_project.yml`

Edit the `dbt_project.yml` file to configure the new model and set its materialization to `table`:

```
models:
  challenge_02:
    library_loans:
      materialized: table
```

### Step 7: Verify the Model can run

Run the following command to ensure the model is correctly set up:
```
dbt run -m library_loans
```
This will create the table `customers_with_late_fees`, however, stakeholders say that the data is wrong and doesn't match the existing report `solution.csv`

### Step 8: Add Tests in schema.yml

In creating the SQL code we have made several assumptions about the source data we should test for.

Create a `sources.yml` file in the `models/library_loans` directory to add the following generic tests:

- All id fields should not contain null values
- All books in the factual and fictional ranges should be unique
- Customers should have three tiers of membership: Bronze, Silver and Gold
- We can only loan books from our factual and fictional ranges
- We can only loan books to members from the members table


```
version: 2

sources:
  - name: library
    schema: main
    tables:
      - name: books_factual
        columns:
          - name: book_id
            data_tests:
              - unique
              - not_null
      - name: books_fictional
```

Execute the following command to test the source tables
```
dbt test -m library_loans
```

You should see:

> Completed successfully
> Done. PASS=7 WARN=0 ERROR=2 SKIP=0 TOTAL=9

### Step 9: Create a staging layer to resolve failed tests

Create three staging tables:
- loans `stg_loans`
- members `stg_members`
- books `stg_books` (the union all of factual and fictional with a column to indicate genre: 'Fact' or 'Fiction')

Reapply the source tests to the new staging tables in the `schema.yml` and implement this below the sources code block.

```
version: 2

sources:
  - name: library
    schema: main
    tables:
      - name: books_factual
      - name: books_fictional
      - name: loans
      - name: members

models:
  - name: stg_books
    columns:
      - name: book_id
        data_tests:
          - unique
          - not_null
  ```
Then run and test your dbt model.

dbt run should return:
> Completed successfully
> Done. PASS=4 WARN=0 ERROR=0 SKIP=0 TOTAL=4

and dbt test should return:
> Completed successfully
> Done. PASS=7 WARN=0 ERROR=2 SKIP=0 TOTAL=9

Refine the code so all staging tables pass the tests now and in the future. 
- Remove any rows with null ids
- Remove any duplicate entries (SELECT DISTINCT should be sufficient)
- Remove any values not within the accepted values

Note if you need to refer to a staging table use Jinja to reference the table
```
SELECT * FROM {{ ref('stg_books') }}
```
Run and test your model with dbt build, you should see:

> Completed successfully
> Done. PASS=13 WARN=0 ERROR=0 SKIP=0 TOTAL=13

### Step 10: Reconfigure the customer_with_late_fees query to use the staging layer

Use {{ source("source_name", "table_name") }} to reference the source tables
Use {{ ref('stg_books') }} to reference the staging tables

Split the customer_with_late_fees query into 2 tables: 
- the CTE `customer_withdrawls`
- the final output `customers_with_late_fees`

execute dbt build to do dbt run + dbt test in one go
```
dbt build -m library_loans
```

dbt build should return:
> Completed successfully
> Done. PASS=14 WARN=0 ERROR=0 SKIP=0 TOTAL=14

### Step 11: Testing and refining the output

There are assumptions we need to test for:
- late fees should always be positive or zero, any negative values are refunds which have been already passed on to the customer and should be excluded
- `customers_with_late_fees` should always have 1 row per customer
- member names in `members`, `customer_withdrawls` and `customers_with_late_fees` should not contain digits, warn the user rather than stop the workflow

These tests will require you to create custom generic tests. 
Create a new folder under `tests` for `generic` and create SQL scripts to identify any data that fails the test criteria, and then add them to your `schema.yml` file.

```
{% test test_name(model, column_name) %}
    SELECT *
    FROM {{ model }}
    WHERE {{ column_name }} < 0
{% endtest %}
```

If any tables fail a test, fix them.
dbt build should return:
> Completed with 1 warning:
> Done. PASS=18 WARN=1 ERROR=0 SKIP=0 TOTAL=19

### Step 12: Verify data is correct with dbt-utils

Install the dbt_utils Package by creating a  `packages.yml` file in the same level (folder) as your `dbt_project.yml` file.

```
packages:
  - package: dbt-labs/dbt_utils
    version: 0.9.2
```
Run `dbt deps` to install the package.

Copy 'solution.csv' from the `data` folder to the `seeds` folder.
Run `dbt seed` to load it to your database.
Update `schema.yml` to include an equal_rowcount test. 

```
version: 2

models:
  - name: customers_with_late_fees
    tests:
      - dbt_utils.equal_rowcount:
          compare_model: ref('solution')

seeds:
  - name: solution

```
Note this uses the term `tests` which is the older version of `data-tests`.

dbt build should return
> Completed with 1 warning:
> Done. PASS=19 WARN=1 ERROR=0 SKIP=0 TOTAL=20

### Task complete!

This project was a look at testing in dbt, we: 

- Configured standard generic tests to stop pipelines running
- Created our own generic tests to warn about issues
- Installed a dbt package `dbt-utils` for more tests

In future challenges, we'll explore more of the functionality of dbt. 

Save your work to GitHub, and I'll see you in the next challenge!