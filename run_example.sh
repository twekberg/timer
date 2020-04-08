#!/bin/bash
#
# Run an example file
#
# Usage: run_examples.sh example_number
#
# Run the specified example.
#
#------------------------------------------------------------------------------

number=$1
if [ "$number" = "" ]; then
    echo "The example number is required"
    exit 1
fi

example="EXAMPLES/example$number.py"
DISPLAY=localhost:0 python $example
