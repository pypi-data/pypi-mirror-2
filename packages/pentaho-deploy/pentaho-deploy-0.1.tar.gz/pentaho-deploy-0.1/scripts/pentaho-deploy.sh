#!/bin/bash

fabfile_path=`python -c 'from pentahodeploy import fabfile; import os; print os.path.abspath(fabfile.__file__).replace("pyc", "py")'`

echo $fabfile_path
fab -f $fabfile_path $@
