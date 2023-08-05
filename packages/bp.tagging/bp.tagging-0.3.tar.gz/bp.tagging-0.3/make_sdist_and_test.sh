#!/bin/bash
# 
# The code in this file is based on
# http://github.com/srid/modern-package-template/blob/master/deploy-and-verify.sh
# which is copyright by Sridhar Ratnakumar (sridhar.ratna (-at-) gmail.com).

# run the tests
python src/bp/tagging/preferences.py

# set some variables
ENV=~/tmp/bp_tagging_env
VERSION=`python setup.py --version`
SDIST=dist/bp.tagging-$VERSION.tar.gz

# build the distribution
rm -Rf dist
python setup.py sdist

# create an empty virtualenv and install bp.tagging
rm -rf $ENV
virtualenv-2.6 --no-site-packages $ENV
pip -E $ENV install paste pastescript
$ENV/bin/easy_install pip
$ENV/bin/pip install $SDIST

# check and view the documentation
python setup.py checkdocs && python setup.py showdocs

