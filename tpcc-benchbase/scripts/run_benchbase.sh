#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BENCHNAME=$1
OUTPUTDIR=$2
OUTPUTLOG=$3

mkdir -p "$OUTPUTDIR" "$OUTPUTLOG"

cd "$SCRIPT_DIR/../benchbase/target/benchbase-postgres"
java -jar benchbase.jar -b "$BENCHNAME" -c "config/postgres/sample_${BENCHNAME}_config.xml" \
    --execute=true --directory="$OUTPUTDIR" > "${OUTPUTLOG}/${BENCHNAME}.log"