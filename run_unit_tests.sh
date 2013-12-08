#!/bin/bash

echo "Running flash library tests"
python -m test.test_flashlib
echo "Running flash service tests"
python -m test.test_flash_service
echo "Running client projection tests"
python -m test.test_projection
echo "Running end to end tests"
python -m test.test_end_to_end
echo "Running linkedlist queue tests"
python -m test.test_linkedlist_queue
rm fawnlog/*.pyc
rm test/*.pyc
