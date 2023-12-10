#!/bin/sh -e
run_in_background() {
    "$@" &
    pid=$!
    echo "Process $pid is running in the background."
    wait $pid
    exit_code=$?
    echo "Process $pid exited with code $exit_code."
    exit $exit_code
}

for job in /jobs/*.kjb; do
    run_in_background /data-integration/kitchen.sh -file $job -level=Normal
done

wait