# Spill the dbt Challenge 03: Whatever the Weather 

## Objective
In this challenge, you'll run a Python model within dbt to fetch weather readings for different office locations and create an incremental model to store historical weather data.

## Prerequisites
- Python 3.7 or higher, dbt version 1.3 or higher
- Necessary Python packages installed from `requirements.txt`
- Basic knowledge of SQL, Python and dbt

To install all required packages, run:
```
pip install -r requirements.txt

```

## Steps to Complete the Challenge

### Step 1: Run the Python Script and Create a duckdb Database 

First, we'll run a standalone Python script to create an initial DuckDB database with weather data.

Open your terminal, navigate to the `spill_the_dbt` directory, and run the following command:
``` bash
python requirements/ch03_data/extract_weather_data.py
```
This will create a DuckDB database file named `office_weather.db` under `requirements/ch03_data`.

This initial database will be used later in the challenge to simulate existing data.

### Step 2: Initialize a dbt Project

Execute the following command to initialize a new dbt project called challenge_03:
``` bash
dbt init challenge_03
```
When prompted, select `duckdb` as your database.

### Step 3: Prepare the Data and Scripts

Copy the following files to your `challenge_03` project:

- Copy `ch03_data/office_locations.csv` to `challenge_03/seeds/office_locations.csv`.
- Copy `ch03_data/extract_weather_data.py` to `challenge_03/models/office_weather/extract_weather_data.py`.
- Copy `ch03_data/office_weather.db` to `challenge_03/models/data/office_weather.db`.

Ensure that the necessary folders (models/office_weather, seeds, data) exist in your challenge_03 project directory. Create them if they don't.

We will modify the Python script to prepare it for integration with dbt. Open `challenge_03/models/office_weather/extract_weather_data.py` and make the following changes:

Remove the `load_data_to_duckdb(df)` function.
``` python
def load_data_to_duckdb(df):
    """
    Loads the DataFrame into a DuckDB table.
    """
    con = duckdb.connect('requirements/ch03_data/office_weather.db')
    con.execute("CREATE TABLE IF NOT EXISTS weather_data AS SELECT * FROM df LIMIT 0")
    con.execute("INSERT INTO latest_weather_readings SELECT * FROM df")
    con.close()
```

Remove the lines at the end of the script that call `load_data_to_duckdb(all_data_df)` and the print statement.
``` python
# Load the combined DataFrame into DuckDB
load_data_to_duckdb(all_data_df)
print("All data has been successfully loaded into DuckDB.")
```
These changes are necessary because dbt will handle data persistence when we convert this script into a dbt Python model.

Change your current directory to `challenge_03`. Your terminal prompt should reflect this change, for example:
`C:\Users\Username\Documents\GitHub\spill_the_dbt\challenge_03`

### Step 4: Configure profiles.yml and dbt_project.yml

Edit the `profiles.yml` file (usually located at `~/.dbt/profiles.yml`) to point to the `office_weather.db` file within the `data` folder:

``` yml
challenge_03:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: "data/office_weather.db"
```
Ensure that the path points to `data/office_weather.db` within your challenge_03 project directory.

Earlier we've created the model "office_weather", added the python script `extract_weather_data.py`, now let's add it to the `dbt_project.yml`

In your `dbt_project.yml` file, add the following configuration to set the materialization for your models:

``` yml
models:
  challenge_03:
    office_weather:
      materialized: table
```

### Step 5: Seed office_locations, Install dbt_expectations and Configure Tests

#### A. Seeding Data

Run the following command to load office_locations.csv into your DuckDB database:

``` bash
dbt seed
```
#### B. Installing dbt_expectations

Create a `packages.yml` file in the root of your `challenge_03` project (same level as `dbt_project.yml`) with the following content:

``` yml
packages:
  - package: calogica/dbt_expectations
    version: 0.10.4
```
Then, run `dbt deps` to install the package.

``` bash
dbt deps
```

Learn more about [https://hub.getdbt.com/calogica/dbt_expectations/latest/](https://hub.getdbt.com/calogica/dbt_expectations/latest/) on the dbt Package Hub.

#### C. Configuring Tests

In the `models/office_weather` directory, create a `schema.yml` file and add tests for the office_locations seed.

We want that latitude and longitude values are within valid ranges:
- both lat and long to be not null
- for long to be between -180 and 180
- for lat to be between -90 and 90

See [dbt_expectations.expect_column_values_to_be_between](
https://github.com/calogica/dbt-expectations/tree/0.10.4/#expect_column_values_to_be_between) for how to apply a test from this package.

### Step 6: Modify `extract_weather_data.py` to Run as a dbt Python Model

Modify the file `extract_weather_data.py` as follows. 
- **Access Seed Data:** Replace reading from CSV files with `dbt.ref('seed_table_name').to_df()` to access the seeded data.
- **Define the dbt model():** Wrap your transformation code within a function named `def model(dbt, session):` 
- **Return the Final DataFrame:** The function `def model(dbt, session):` should return the final DataFrame, e.g. `return all_data_df`

Your `extract_weather_data.py` should look like:

``` python
import packages...

def fetch_weather_data(latitude, longitude): 
  ...

def flatten_weather_data(data, office_name):
  ...

def model(dbt, session):

    # Fetch office locations from the dbt seed
    office_df = dbt.ref('seed_table_name').to_df()

    ...

    return all_data_df

```
By wrapping the code in `def model(dbt, session):`, we define a dbt Python model. The dbt object provides access to dbt functions, and `session` is the database session.


You can learn more about [Python models](https://docs.getdbt.com/docs/build/python-models) in the dbt documentation.


In the model's `schema.yml` file configure the python code to create a table with the name "latest_weather_readings", rather than the current file name. 

``` yml
models:
  - name: filename
    config:
      alias: new_name
```
You can learn more about configuring an [alias](https://docs.getdbt.com/reference/resource-configs/alias) in the dbt documentation.

Note this can also be achieved by setting a `dbt.config()` within the Python model.


### Step 7: Create Incremental model "all_weather_readings"

New weather readings are available from the API every 15 minutes, we want to track historical readings from the API as a new table but don't want to load duplicate readings into the table. To ensure only new or updated records are add to the table we will build an incremental model. 

You can learn more about how to [Configure incremental models](https://docs.getdbt.com/docs/build/incremental-models) in the dbt documentation.

To do this we'll need a SQL script that has:
- A materialization type to 'incremental'
- A unique key, or composite key, for row level identification
- the `is_incremental()` macro to conditionally filter for new or updated records

To Do
1. Create a sql file `models/office_weather/all_weather_readings.sql`
2. At the beginning of your SQL file, add a `config()` block to set the materialization and unique key:
```
{{ config(
    materialized= ...,
    unique_key= ...  
) }}
```

3. Add the `is_incremental()` macro
```
{% if is_incremental() %}
    WHERE condition
{% endif %}
```

- The `config()` block sets the materialization to `incremental` and specifies the `unique_key`.
- The `is_incremental()` macro checks if the model is running incrementally.
- The `WHERE` clause ensures only new records are added.

### Step 8: Test to Verify No Duplicate Data is Being Loaded

In your `schema.yml` file, add a test for uniqueness on the column(s) you used to form your unique_key for the incremental model. 

Check your test by running the following command:

``` bash
dbt test --select all_weather_readings
```

If that test is successful, run `dbt build` on the model to ensure all tests are passed and the tables are created.

``` bash
dbt build -m office_weather
```
Done. PASS=7 WARN=0 ERROR=0 SKIP=0 TOTAL=7


### Task complete!

This project was building incremental models in dbt, we: 

- Ran a Python model in dbt to call an API
- Created tests using the dbt package `dbt-expectations` 
- Built an incremental model to only loads new data, or data that has changed

Save your work to GitHub, share what you've learned with **#SpilltheDBT**, and get ready for the next challenge!