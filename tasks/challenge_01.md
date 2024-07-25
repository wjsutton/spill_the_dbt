# Spill the dbt Challenge 01: Lego Data Analysis

## Objective
Set up a dbt project to analyze Lego data using a provided DuckDB database, SQL script, and Python script.

## Prerequisites
- Python installed
- Necessary packages installed from `requirements.txt`
- Basic knowledge of SQL and dbt

Install all packages from `requirements.txt` with
```
pip install -r requirements.txt

```

## Steps to Complete the Challenge

### Step 1: Navigate to the "spill_the_dbt" Folder

Open your terminal and navigate to the `spill_the_dbt` directory in your working directory:
```
cd spill_the_dbt
```

### Step 2: Initialize a dbt Project

Execute the following command to initialize a new dbt project called challenge_01:
```
dbt init challenge_01
```
When prompted, select `duckdb` as your database.

### Step 3: Move the Data Folder

Move the `ch01_data` folder located in the `requirements` directory to your dbt project folder `challenge_01`:
```
cp requirements/ch01_data challenge_01
```
inspect the data in ch01_data with the python script `read_database.py`

### Step 4: Configure Your profiles.yml

Edit the `profiles.yml` file in the `.dbt` folder to point to the `lego.db` file within the `ch01_data` folder:

```
challenge_01:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: "ch01_data/lego.db"
```
Note: path is the filepath to your duckdb database file from where you run the dbt model.

### Step 5: Create a New Model

In your `challenge_01` dbt project, create a new model named `lego` and move the provided SQL script (`ch01_sql_script.sql`) to this model folder:

```
mkdir -p models/lego
cp ch01_data/ch01_sql_script.sql models/lego/lego.sql
```

### Step 6: Configure the Model in `dbt_project.yml`

Edit the `dbt_project.yml` file to configure the new model and set its materialization to `table`:

```
models:
  challenge_01:
    lego:
      materialized: table
```

### Step 7: Verify the Model can run

Run the following command to ensure the model is correctly set up:
```
dbt run -m lego
```
If you encounter any errors fix them. 
You should see:

> Completed successfully
> Done. PASS=1 WARN=0 ERROR=0 SKIP=0 TOTAL=1

### Step 8: Add Tests in schema.yml

Create a `schema.yml` file in the `models/lego` directory to add tests ensuring the columns [theme_name, set_name, set_year] have no null values:

```
version: 2

models:
  - name: lego
    columns:
      - name: column_name # replace with actual column name
        data_tests:
          - not_null
```

### Step 9: Modularise the SQL and add Ref Functions

Edit the sql script so a table is created (materialized) for the UNIQUE_PARTS CTE and another table for the output of the query. This will involve splitting the script into two queries. 

The SQL table created will take the name of the filename, this can be corrected using the alias function. 

Edit your second query to use `ref` functions to join to the result of the first query (unique_parts):

```
-- In models/lego/lego.sql
select * from {{ ref('unique_parts') }} -- Adjust as necessary
```

Run the following command to ensure the model is correctly set up:
```
dbt run -m lego
```

If you encounter any errors fix them. 
You should see:

> Completed successfully
> Done. PASS=2 WARN=0 ERROR=0 SKIP=0 TOTAL=2


### Step 10: Generate Docs

Generate the documentation site
```
dbt docs generate
dbt docs serve
```

Navigate to the lego table and verify it depends on unique_parts (the new SQL table you created in Step 9)

### Step 11: Run the Entire Workflow

Execute the following command to run the entire workflow:
```
dbt build -m lego
```
Note dbt run will create the tables, dbt build will run tests and create tables.

If you encounter any errors fix them. 
You should see:

> Completed successfully
> Done. PASS=5 WARN=0 ERROR=0 SKIP=0 TOTAL=5

###  Step 12: Verify the Table Creation

Use the provided Python script to verify that the tables have been created correctly. 
```
python ch01_data/read_database.py
```
You should see:
- an output of 10 table names from the database
- an output of the lego table showing lego themes, set, unique_part and a count of parts


### Task complete!

This project was an introduction to working with dbt, we: 

- Set up a dbt Project
- Created and Configured a Model
- And Ran and Tested the Model

In future challenges, we'll explore more of the functionality of dbt. 

Save your work to GitHub, and I'll see you in the next challenge!