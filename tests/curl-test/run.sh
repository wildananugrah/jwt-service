#!/bin/bash
for i in {1..10}; do
   ./test.sh &
done
wait
