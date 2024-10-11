# Spill the dbt Challenge 02: Library Loan Issues 

## Objective
Identify and fix issues in a dbt model that aggregates late fees for overdue library loans by writing and running tests. Compare the fixed model's output with a provided CSV seed using the dbt-utils package.

## Prerequisites

- Python 3.7 or higher, dbt version 1.3 or higher
- Necessary Python packages installed from `requirements.txt`
- Basic knowledge of SQL, Python and dbt

To install all required packages, run:
```
pip install -r requirements.txt

```

## Steps to Complete the Challenge

### Step 1: Initialize a dbt Project

**1. Find spill_the_dbt in the terminal**
Open your terminal, navigate to the `spill_the_dbt` directory (the root of the repository), using commands below to change directory
```bash
cd spill_the_dbt
```
**2. Create a dbt project**
Next we'll create a new dbt project named challenge_02.

Run the following command:
```bash
dbt init challenge_02
```
When prompted, select `duckdb` as your database adapter.

This will create a new directory named `challenge_02` in your current location.

Change your current directory to challenge_02:
```bash
cd challenge_02
```

**3. Move data and scripts to your dbt project**

Copy the necessary data and scripts to your challenge_02 project.

- Create the data Directory
```bash
mkdir data
```

- Copy the contents of the ch02_data folder to your challenge_02/data directory.

```bash
cp ../requirements/ch02_data/* data/
```
*Note: Adjust the path if your directories are different.*

- You can inspect the data in ch02_data using the provided Python script `read_database.py`.

```bash
python ch02_data/read_database.py
```

This script reads the DuckDB database and displays the available tables.

### Step 2: Configure Your profiles.yml

Edit your `profiles.yml` file (usually located at `~/.dbt/profiles.yml`) to include the following configuration:

```
challenge_02:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: "data/library.db"
```
Ensure that the path points to the `data/library.db` file within your `challenge_02` project directory.

### Step 3: Create a New Model

In your challenge_02 dbt project, we'll create a new model named library_loans.

- Create the Models Directory

```bash
mkdir -p models/library_loans
```
- Copy the provided SQL script customers_with_late_fees.sql to your models directory

```bash
cp data/customers_with_late_fees.sql models/library_loans/customers_with_late_fees.sql
```

### Step 4: Configure the Model in `dbt_project.yml`

In your `dbt_project.yml` file, add the following configuration to set the materialization for your models:

```
models:
  challenge_02:
    library_loans:
      materialized: table
```
This sets the library_loans model to be materialized as a table.

### Step 5: Verify the Model Can Run

Run the following command to ensure the model is correctly set up:
```
dbt run -m library_loans
```
This will create the table `customers_with_late_fees`. 

However, stakeholders have indicated that the data is incorrect and does not match the existing report `solution.csv`.

### Step 6: Add Tests in schema.yml

We need to create tests to identify issues in our source data.

Create schema.yml In the models/library_loans directory, create a schema.yml file

```bash
touch models/library_loans/schema.yml
```

Add tests to schema.yml, to check the following assumptions:

- All id fields should not contain null values
- All books in the factual and fictional ranges should be unique
- Customers should have three tiers of membership: Bronze, Silver and Gold
- We can only loan books from our factual and fictional ranges
- We can only loan books to members from the members table

Here is an example of formating tests in `schema.yml`.

```yml
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
You can learn more about [applying tests](https://docs.getdbt.com/docs/build/data-tests) in the dbt documentation.


Execute the following command to run the tests:
```bash
dbt test -m library_loans
```

You should see output indicating that some tests have failed:

> Completed successfully
> Done. PASS=7 WARN=0 ERROR=2 SKIP=0 TOTAL=9

### Step 7: Create a Staging Layer to Resolve Failed Tests

We will create staging models to clean and prepare the data.

Create three new models in `models/library_loans`:
- loans `stg_loans`
- members `stg_members`
- books `stg_books` 

Note: `stg_books` is the union all of factual and fictional with a column to indicate genre: 'Fact' or 'Fiction'

Update schema.yml the run the test against the new staging tables. Those assumptions to check were:

- All id fields should not contain null values
- All books in the factual and fictional ranges should be unique
- Customers should have three tiers of membership: Bronze, Silver and Gold
- We can only loan books from our factual and fictional ranges
- We can only loan books to members from the members table

Here's is a starting point for your `schema.yml` file
```yml
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

```bash
dbt run -m library_loans
```

dbt run should return:
> Completed successfully
> Done. PASS=4 WARN=0 ERROR=0 SKIP=0 TOTAL=4

```bash
dbt test -m library_loans
```

and dbt test should return:
> Completed successfully
> Done. PASS=7 WARN=0 ERROR=2 SKIP=0 TOTAL=9

Refine the code so all staging tables pass the tests now and in the future. 
- Remove any rows with null ids
- Remove any duplicate entries (SELECT DISTINCT should be sufficient)
- Remove any values not within the accepted values

Note if you need to refer to a staging table use Jinja to reference the table
```sql
SELECT * FROM {{ ref('stg_books') }}
```
Run and test your model with dbt build, you should see:

> Completed successfully
> Done. PASS=13 WARN=0 ERROR=0 SKIP=0 TOTAL=13

### Step 8: Refactor customer_with_late_fees to Use the staging layer

Modify the `customers_with_late_fees.sql` model to use the staging models.
- Use {{ source("source_name", "table_name") }} to reference the source tables
- Use {{ ref('stg_books') }} to reference the staging tables

Split the customer_with_late_fees query into 2 tables: 
- the CTE `customer_withdrawls`
- the final output `customers_with_late_fees`

Run and Test the Model:
```
dbt build -m library_loans
```

dbt build applies both run and test at once, you can learn more about the [dbt build command](https://docs.getdbt.com/reference/commands/build) in the dbt documentation.

dbt build should return:
> Completed successfully
> Done. PASS=14 WARN=0 ERROR=0 SKIP=0 TOTAL=14

### Step 9: Add Custom Generic Tests

We need to add tests for additional assumptions:
- late fees should always be positive or zero, any negative values are refunds which have been already passed on to the customer and should be excluded
- `customers_with_late_fees` should always have 1 row per customer
- member names in `members`, `customer_withdrawls` and `customers_with_late_fees` should not contain digits, warn the user rather than stop the workflow

These tests will require you to create custom generic tests. 

Create a new directory for tests:

```bash
mkdir tests
```
Create a file tests/new_test.sql:

```sql
{% test new_test(model, column_name) %}
  SELECT *
  FROM {{ model }}
  WHERE {{ column_name }} <> 0
{% endtest %}
```
Add Tests to schema.yml

```yml
models:
  - name: customers_with_late_fees
    columns:
      - name: total_late_fees
        tests:
          - not_negative
```
Run the Tests

```bash
dbt test -m customers_with_late_fees
```
If you encounter any tests failing, fix them accordingly.

dbt build should return:
> Completed with 1 warning:
> Done. PASS=18 WARN=1 ERROR=0 SKIP=0 TOTAL=19

### Step 10: Verify Data Correctness with dbt-utils

Install the dbt_utils package to use additional testing capabilities.

Create a  `packages.yml` file in the same level (folder) as your `dbt_project.yml` file, with the following code included.

```yml
packages:
  - package: dbt-labs/dbt_utils
    version: 0.9.2
```
Run `dbt deps` to install the package.
```bash
dbt deps
```

Copy 'solution.csv' from the `data` folder to the `seeds` folder and run `dbt seed` to load it to your database.

```bash
dbt seed
```

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

Save your work to GitHub, share what you've learned with **#SpilltheDBT**, and get ready for the next challenge!