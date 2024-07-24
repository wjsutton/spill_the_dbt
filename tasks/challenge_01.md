# Spill the dbt Challenge 01: Lego Data Analysis

## Objective
Set up a dbt project to analyze Lego data using a provided DuckDB database, SQL script, and Python script.

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

Execute the following command to initialize a new dbt project called challenge_01:
```
dbt init challenge_01
```
When prompted, select `duckdb` as your database.

### Step 3: Move the Data Folder

Move the `ch01_data` folder located in the `requirements` directory to your dbt project folder `challenge_01`:
```
mv ../requirements/ch01_data challenge_01
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
      path: "path_to_your_project_folder/challenge_01/ch01_data/lego.db"
```

### Step 5: Create a New Model

In your `challenge_01` dbt project, create a new model named `lego` and move the provided SQL script (`ch01_sql_script.sql`) to this model folder:

```
mkdir -p models/lego
mv ../ch01_data/ch01_sql_script.sql models/lego/lego.sql
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

### Step 8: Add Tests in schema.yml

Create a `schema.yml` file in the `models/lego` directory to add tests ensuring the dataset has no null values:

```
version: 2

models:
  - name: lego
    columns:
      - name: column_name # replace with actual column name
        tests:
          - not_null
```

### Step 9: Add Ref Functions and Generate Docs

Edit your model to use `ref` functions for the source tables and generate documentation:

```
-- In models/lego/lego.sql
select * from {{ ref('your_source_table') }} -- Adjust as necessary
```

Generate the documentation site
```
dbt docs generate
dbt docs serve
```

### Step 10: Run the Entire Workflow

Execute the following command to run the entire workflow:
```
dbt build -m lego
```

###  Step 11: Verify the Table Creation

Use the provided Python script to verify that the table has been created correctly. 
```
python read_database.py
```

### Task complete!

Save your work to GitHub!