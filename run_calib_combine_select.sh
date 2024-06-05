#!/bin/bash
# This script runs a Python script

# Define the path to the Python script
PYTHON_SCRIPT1="run_calib_combine_select.py"
PYTHON_SCRIPT2="collect_json_plots.py"

# Check if the Python script exists
if [ ! -f "$PYTHON_SCRIPT1" ]; then
    echo "Error: $PYTHON_SCRIPT1 not found!"
    exit 1
fi

# Check if an argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <input>"
    exit 1
fi

# Capture the input argument
INPUT_ARG=$1

# Run the Python script with the input argument
# The input argument is passed to the Python script using a here document
python3 "$PYTHON_SCRIPT1" <<< "$INPUT_ARG" > /dev/null 2>&1

# Capture the exit status of the Python script
EXIT_STATUS=$?

# Check if the first Python script ran successfully
if [ $EXIT_STATUS -ne 0 ]; then
    echo "Python script $PYTHON_SCRIPT1 exited with status $EXIT_STATUS"
    exit $EXIT_STATUS
fi

echo "Python script $PYTHON_SCRIPT1 ran successfully"

# Run the second Python script with the input argument
# The input argument is passed to the Python script using a here document
python3 "$PYTHON_SCRIPT2" <<< "$INPUT_ARG" > /dev/null 2>&1

# Capture the exit status of the second Python script
EXIT_STATUS=$?

# Check if the second Python script ran successfully
if [ $EXIT_STATUS -ne 0 ]; then
    echo "Python script $PYTHON_SCRIPT2 exited with status $EXIT_STATUS"
    exit $EXIT_STATUS
fi

echo "Python script $PYTHON_SCRIPT2 ran successfully"