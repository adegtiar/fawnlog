#!/bin/bash

echo "Running flash library tests\n"
python -m test.test_flashlib
echo "Running get token service tests\n"
python -m test.test_get_token_service
echo "Running flash service tests\n"
python -m test.test_flash_service
echo "Running client projection tests\n"
python -m test.test_projection
echo "Running end to end tests\n"
python -m test.test_end_to_end
rm fawnlog/*.pyc
rm test/*.pyc
