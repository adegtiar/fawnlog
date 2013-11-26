#!/bin/bash

echo "Running flash library tests"
python -m test.test_flashlib
echo "Running get token service tests"
python -m test.test_get_token_service
echo "Running flash service tests"
python -m test.test_flash_service
echo "Running client projection tests"
python -m test.test_projection
echo "Running end to end tests"
python -m test.test_end_to_end
rm fawnlog/*.pyc
rm test/*.pyc
