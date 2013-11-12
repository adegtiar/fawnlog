#!/bin/bash

echo "Running flash library tests"
python -m test.test_flash
python -m test.test_get_token_service
# python -m test.test_projection
rm fawnlog/*.pyc
