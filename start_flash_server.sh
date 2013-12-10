#!/bin/bash
rm *.flog
python2.7 -m fawnlog.flash_service "$@"
