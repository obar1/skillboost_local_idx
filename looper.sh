#!/bin/bash
MAGIC_N=11 # lol :)

set -x # verbose

[ -z "$1" ] && exit 1
[ -z "$2" ] && exit 1
[ -z "$3" ] && exit 1

TEMPLATE_TYPE=$1
_FROM=$2
_TO=$3
PYTHON=$(which python3)  # Change if using a different Python interpreter

for (( i=_FROM; i<=_TO; i++ ))
do
    echo "Launching process with itin=$i..."
    (
        $PYTHON -m uv run py_fetch_skillboost.py "$TEMPLATE_TYPE" "$i"
        echo $!
        sleep $MAGIC_N
    ) # & - uncomment this if you are sure of it, it seems SB is not happy of it :P
     
    if (( i % $MAGIC_N == 0 )); then
      sleep $MAGIC_N  # Additional sleep for multiples of $MAGIC_N
    fi

done
echo "check with HTOP or similar..."

