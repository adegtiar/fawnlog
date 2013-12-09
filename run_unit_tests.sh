#!/bin/bash

echo "Running flash library tests"
python -m test.test_flashlib
echo "Running flash unit tests"
python -m test.test_flash_unit
echo "Running flash service tests"
python -m test.test_flash_service
echo "Running projection tests"
python -m test.test_projection
echo "Running client tests"
python -m test.test_client
echo "Running end to end tests"
python -m test.test_end_to_end
echo "Running linkedlist queue tests"
python -m test.test_linkedlist_queue
echo "Running ips count tests"
python -m test.test_ips_count
echo "Running sequencer tests"
python -m test.test_sequencer
rm fawnlog/*.pyc
rm test/*.pyc
