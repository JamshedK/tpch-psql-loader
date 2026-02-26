# TPC-H PostgreSQL Loader

A tool for generating and loading [TPC-H](https://www.tpc.org/tpch/) benchmark data into PostgreSQL, along with utilities for generating parameterized query workloads.

> **Note:** These instructions are written for **Ubuntu**.

---

## Prerequisites

### 1. Install PostgreSQL 14

```bash
sudo apt update
sudo apt install -y postgresql-14 postgresql-client-14
```

Start and enable the service:

```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 2. Create the Database and User

Switch to the `postgres` system user and open `psql`:

```bash
sudo -u postgres psql
```

Inside the `psql` shell, set a password for the `postgres` user and create the database:

```sql
ALTER USER postgres WITH PASSWORD '123456';
CREATE DATABASE tpch_1;
\q
```

> You can name the database anything you like (e.g. `tpch_1`, `tpch_10`, etc.), but make sure you use that same name in the Python configuration below.

### 3. Install Python Dependencies

Make sure you have Python 3.10+ installed, then install the required packages:

```bash
pip install -r requirements.txt
```

---

## Setting Up TPC-H `dbgen`

### 4. Download `dbgen`

Clone the TPC-H `dbgen` tool and save it somewhere on your machine. A good place is your home directory:

```bash
cd ~
git clone https://github.com/electrum/tpch-dbgen.git tpch-dbgen
```

Note the full path to this directory — you will need it. For example:

```
/home/<your-username>/tpch-dbgen
```

### 5. Query Templates

This repo includes corrected TPC-H query templates in the `tpch-templates/` folder. When you run the loader, it **automatically** clears any existing templates from `dbgen/queries/` and copies these in — no manual step needed.

> The templates in `tpch-templates/` are corrected versions compatible with PostgreSQL. The originals that ship with `dbgen` may not work out of the box with Postgres.

### 6. Create the Data Output Directory

Create a directory where the generated table data, queries, and refresh functions will be saved:

```bash
mkdir -p /home/<your-username>/tpch-data
```

Again, note this full path — you will need it.

---

## Running the Loader

### 7. Update the Configuration in `test_tpch_generator.py`

Open [test_tpch_generator.py](test_tpch_generator.py) and update the following values to match your setup:

```python
# The database you created in step 2
replica = Replica(
    id=0,
    hostname='localhost',
    port='5432',
    dbname='tpch_1',           # <-- change this to your database name
    user='postgres',
    password='123456'           # <-- change this to your postgres password
)

# The path where you cloned tpch-dbgen (step 4)
dbgen_path = '/home/<your-username>/tpch-dbgen'

# The data output directory you created (step 6)
data_path = '/home/<your-username>/tpch-data'

# Scale factor: 1 = ~1GB of data, 10 = ~10GB, etc.
scale_factor = 1
```

### 8. Run the Loader

```bash
python test_tpch_generator.py
```

This will:
1. Compile `dbgen`
2. Generate TPC-H table data at the specified scale factor
3. Load the data into PostgreSQL
4. Generate the 22 parameterized TPC-H queries

Logs are written to both the console and `tpch_test.log`.

---

## Generating Query Workloads

To generate query workloads (multiple parameterized variants of the 22 TPC-H queries) without reloading the database, use `generate_queries.py` directly. Update `dbgen_path` and `scale_factor` in that file, then run it.

---

## Project Structure

```
tpch-psql-loader/
├── tpch_generator.py       # Core class: generates data and loads it into Postgres
├── generate_queries.py     # Standalone query workload generator
├── generator.py            # Base generator class
├── connection.py           # PostgreSQL connection wrapper
├── replica.py              # Database replica configuration
├── test_tpch_generator.py  # Entry point / example usage
├── schema_keys.sql         # Primary and foreign key definitions
├── indexes.sql             # Index definitions
├── requirements.txt        # Python dependencies
├── tpch-templates/         # Corrected TPC-H query templates (PostgreSQL-compatible)
├── dbgen/queries/          # Placeholder for dbgen's query directory
└── workloads/              # Generated query workload output files
```
