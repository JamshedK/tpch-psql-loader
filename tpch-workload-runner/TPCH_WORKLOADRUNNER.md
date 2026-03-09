# TPC-H Workload Runner Guide

This guide explains how to configure and run the manual workload runner in `tpch-workload-runner/`.

## What this runner does

The script `manual_workload_runner.py` reads database and workload settings from a PostgreSQL config file, loads SQL statements from a workload file, and executes them using the configured number of threads.

The test entry point is:

```bash
python tpch-workload-runner/test.py
```

## Important note about the config path

`manual_workload_runner.py` currently uses a hardcoded config path:

```python
config_path = "/home/karimnazarovj/LATuner/config/postgres.ini"
```

You need to change this line so it points to the correct `postgres.ini` file on your machine.

For example, if you want to use the config stored in this repo, update it to point at your actual local path for `tpch-workload-runner/postgres.ini`.

That means the runner does **not** read `tpch-workload-runner/postgres.ini` automatically unless this hardcoded path is updated or the config file is copied to that location.

## Setting up `postgres.ini`

Make sure your `postgres.ini` has both a `[DATABASE]` section and a `[WORKLOAD]` section.

Example:

```ini
[DATABASE]
user=postgres
db=tpcc_50
host=localhost
port=5432
benchmark=tpcc
password=123456
restart_cmd=sudo systemctl restart postgresql
knob_info_path=./knowledge_collection/postgres/knob_info/system_view.json
recover_script=./scripts/recover_postgres.sh

[WORKLOAD]
workload_path=../workloads/tpch_44.sql
threads=1
timeout=320
```

## Fields to update

### Database settings

- `user` — PostgreSQL username.
- `db` — Database name to connect to.
- `host` — Database server host, usually `localhost`.
- `port` — PostgreSQL port, usually `5432`.
- `password` — Password for the PostgreSQL user.

### Workload settings

- `workload_path` — Path to the SQL workload file.
  - This is required.
  - It should point to a file containing the queries you want to execute.
  - Example: `../workloads/tpch_44.sql`
- `threads` — Number of worker threads used to run the queries.
- `timeout` — Maximum runtime in seconds before active queries are canceled.

## How `workload_path` works

The runner reads SQL from the file specified by `workload_path`.

Example workload files already in this repo include:

- `workloads/tpch_22.sql`
- `workloads/tpch_44.sql`
- `workloads/tpch_88.sql`
- `workloads/tpch_154.sql`
- `workloads/tpch_220.sql`
- `workloads/tpch_440.sql`

If you use the example config shown above, the runner will execute queries from `workloads/tpch_44.sql`.

## Installing dependencies

Before running the test, install the Python dependencies from the repo root:

```bash
pip install -r requirements.txt
```

If `psycopg2` is missing in your environment, install it manually:

```bash
pip install psycopg2-binary
```

## Running the test

From the repository root:

```bash
python tpch-workload-runner/test.py
```

This will:

1. Create a `ManualWorkloadRunner`
2. Read the config file from the hardcoded path
3. Load the SQL file from `workload_path`
4. Distribute queries across the configured number of threads
5. Execute the workload and print throughput plus total runtime

## Common issues

### `NoOptionError: No option 'workload_path'`

Your `[WORKLOAD]` section is missing `workload_path`. Add it to `postgres.ini`.

### `ImportError` or missing `psycopg2`

Install dependencies:

```bash
pip install -r requirements.txt
pip install psycopg2-binary
```

### Database connection failed

Check these values in `postgres.ini`:

- `db`
- `user`
- `password`
- `host`
- `port`

Also make sure PostgreSQL is running and the target database exists.

### Workload file not found

Make sure `workload_path` points to a real SQL file and that the path is valid relative to wherever your config file is being used.
