#!/bin/bash

echo "Running flash library tests"
python -m test.test_flash
echo "Running get token service tests"
python -m test.test_get_token_service
echo "Running flash service tests"
python -m test.test_flash_service
python -m test.test_projection
rm fawnlog/*.pyc
rm test/*.pyc
