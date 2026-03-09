# BenchBase Helper Guide

This guide walks you through setting up and running a TPC-C benchmark using [BenchBase](https://github.com/cmu-db/benchbase).

---

## Step 1: Install BenchBase

Navigate into the `scripts/` folder and run the install script. This will clone the BenchBase repo, check out a stable commit, build it, and extract it — all in the directory you're currently in.

```bash
cd scripts
sh install_benchbase.sh postgres
```

> **Note:** This requires `git` and Java 21 (JDK). The script will install them via `apt` if they're not already present. Make sure you're on a Debian/Ubuntu-based system or have those dependencies available.

---

## Step 2: Build and Load the Database

Once BenchBase is installed, run the build script to create and load the TPC-C schema into your database:

```bash
sh build_benchbase.sh postgres tpcc
```

This runs `benchbase.jar` with `--create=true --load=true`, which creates the schema and loads the data. The `--execute=false` flag means it won't run the benchmark yet — just sets everything up.

---

## Step 3: Configure the Benchmark

Before executing the benchmark, open the config file:

```
tpcc-benchbase-loader/sample_tpcc_config.xml
```

Here are the key fields you need to set:

### Database Connection

```xml
<url>jdbc:postgresql://localhost:5432/YOUR_DB_NAME?sslmode=disable&amp;ApplicationName=tpcc&amp;reWriteBatchedInserts=true</url>
<username>your_username</username>
<password>your_password</password>
```

- **`url`** — Update `YOUR_DB_NAME` to match the name of your PostgreSQL database.
- **`username`** — Your PostgreSQL username (e.g., `postgres`).
- **`password`** — Your PostgreSQL password.

---

### Scale Factor

```xml
<scalefactor>50</scalefactor>
```

- This controls the **size of the dataset**.
- A scale factor of **1 ≈ 100 MB** of data (1 warehouse).
- A scale factor of **50** means 50 warehouses, roughly **5 GB** of data.
- Start small (e.g., `1` or `5`) when testing.

---

### Terminals

```xml
<terminals>16</terminals>
```

- This is the **number of concurrent threads** (virtual users) running transactions.
- More terminals = more concurrency = more load on the database.
- Set this based on how many cores/threads your system can handle.

---

### Work Configuration

```xml
<work>
    <time>120</time>
    <rate>unlimited</rate>
    <weights>45,43,4,4,4</weights>
</work>
```

- **`time`** — Duration of the benchmark run in **seconds** (e.g., `120` = 2 minutes).
- **`rate`** — Controls the transaction rate.
  - Set to `unlimited` to run as many transactions as possible (maximum throughput mode).
  - Set to a number (e.g., `1000`) to cap transactions per second.
- **`weights`** — The percentage mix of the 5 TPC-C transaction types: `NewOrder, Payment, OrderStatus, Delivery, StockLevel`. The defaults (`45,43,4,4,4`) follow the TPC-C spec.

---

## Step 4: Run the Benchmark

Once the config is set, go back to the BenchBase directory and execute:

```bash
java -jar benchbase.jar -b tpcc -c config/postgres/sample_tpcc_config.xml --execute=true
```
