# Spill the dbt Challenge 01: Lego Data Analysis

## Objective

In this challenge, you'll set up a dbt project to analyze Lego data using a provided DuckDB database, SQL script, and Python script. You'll create dbt models, configure your project, and learn how to run and test your models.

## Prerequisites

- Ensure you have [Python](https://www.python.org/) installed on your machine that is compatible with dbt. Check [What version of Python can I use?](https://docs.getdbt.com/docs/core/pip-install)
- A virtual environment setup and Python packages installed from `requirements.txt`
- Basic knowledge of SQL, Python and dbt

**Create a virtual environment**
```
python -m venv dbt-env
```
**Activate your virtual environment**
Windows:
```
dbt-env\Scripts\activate
```
Mac / Linux
```
source dbt-env/bin/activate
```
**Install the required packages**
``` bash
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
Next we'll create a new dbt project named challenge_01.

Run the following command:
```bash
dbt init challenge_01
```
When prompted, select `duckdb` as your database adapter.

This will create a new directory named `challenge_01` in your current location.

Change your current directory to challenge_01:
```bash
cd challenge_01

```

**3. Move data and scripts to your dbt project**

Copy the necessary data and scripts to your challenge_01 project.

- Copy the entire requirements/ch01_data folder to your challenge_01 project directory.

```bash
cp -r ../requirements/ch01_data ./
```
*Note: Adjust the path if your directories are different.*

- You can inspect the data in ch01_data using the provided Python script `read_database.py`.

```bash
python ch01_data/read_database.py
```

This script reads the DuckDB database and displays the available tables.

### Step 2: Configure Your profiles.yml

Edit your `profiles.yml` file (usually located at `~/.dbt/profiles.yml`) to include the following configuration:

```yml
challenge_01:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: "ch01_data/lego.db"
```
Ensure that the path points to the `ch01_data/lego.db` file within your `challenge_01` project directory.

### Step 3: Create a New Model

In your `challenge_01` dbt project,  we'll create a new model named lego.

Create the Models Directory:
```bash
mkdir -p models/lego
```

Copy the provided SQL script ch01_sql_script.sql to your models directory:
```bash
cp ch01_data/ch01_sql_script.sql models/lego/lego.sql
```

### Step 4: Configure the Model in `dbt_project.yml`

In your `dbt_project.yml` file, add the following configuration to set the materialization for your models:

```yml
models:
  challenge_01:
    lego:
      materialized: table
```
This sets the lego model outputs to be materialized as tables in the database.

### Step 5: Verify the Model can run

Run the following command to ensure the model is correctly set up:

```bash
dbt run -m lego
```
If you encounter any errors, fix them accordingly.

You should see output indicating that the model has run successfully:

> Completed successfully
> Done. PASS=1 WARN=0 ERROR=0 SKIP=0 TOTAL=1

### Step 6: Add Tests in schema.yml

Create a `schema.yml` file in the `models/lego` directory to add tests ensuring the columns [theme_name, set_name, set_year] have no null values:

```yml
version: 2

models:
  - name: lego
    columns:
      - name: column_name # replace with actual column name
        data_tests:
          - not_null
```

### Step 7: Modularise the SQL and add Ref Functions

We will split the existing SQL script into two models to create modular components. This practice enhances maintainability and allows for easier testing.

**1. Create a new SQL model for the UNIQUE_PARTS CTE.**

Open `lego.sql` and copy the SQL code for the UNIQUE_PARTS CTE into a new file, ` unique_parts.sql`. Ensure that `unique_parts.sql` selects the data you need and ends with a SELECT statement.

**2. Modify lego.sql to Reference unique_parts.sql**

In lego.sql, modify the query to reference unique_parts using the ref function.

```sql
SELECT *
FROM {{ ref('unique_parts') }}
WHERE -- your conditions
```
This tells dbt to use the unique_parts model as a dependency.

You can learn more about [model references](https://docs.getdbt.com/reference/dbt-jinja-functions/ref) in the dbt documentation.

**3. Ensure the model runs**

Run the following command to ensure the model is correctly set up:
```
dbt run -m lego
```

If you encounter any errors fix them. 
You should see:

> Completed successfully
> Done. PASS=2 WARN=0 ERROR=0 SKIP=0 TOTAL=2


### Step 8: Generate Docs

Generate the documentation site to visualize your models and their dependencies.

Run:
```bash
dbt docs generate
dbt docs serve
```
This will generate documentation for your project and serve it locally.

- Open the generated site in your browser (usually at http://localhost:8080). 
- Navigate to the lego model and verify it depends on unique_parts.

You can learn more about [dbtdocs commands](https://docs.getdbt.com/reference/commands/cmd-docs) in the dbt documentation.

### Step 9: Run the Entire Workflow

Run the following command to build and test your models:
```
dbt build -m lego
```
This command will:

- Run your models
- Run your tests
- Generate documentation

If you encounter any errors, fix them accordingly.

You should see output indicating that your models ran successfully and that tests passed:

> Completed successfully
> Done. PASS=5 WARN=0 ERROR=0 SKIP=0 TOTAL=5

###  Step 10: Verify the Table Creation

Use the provided Python script to verify that the tables have been created correctly.
```bash
python ch01_data/read_database.py
```
You should see:

- An output of table names from the database, including your newly created models.
- An output of the lego table showing Lego themes, sets, unique parts, and a count of parts.


### Task complete!

This project was an introduction to working with dbt, we: 

- Set up a dbt Project
- Created and Configured a Model
- Ran, Tested, and Documented the Model

Save your work to GitHub, share what you've learned with **#SpilltheDBT**, and get ready for the next challenge!
