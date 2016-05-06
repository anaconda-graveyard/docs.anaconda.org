#!/bin/bash

docsdir='/srv/deploy/wakaridocs/'

if [ ! -d ${docsdir} ]; then
  echo 'Docs directory not found ['${docsdir}'].  Please create it.'
  exit 1
fi

echo 'Generating site...'
hyde gen -r

echo 'Deploying site to '${docsdir}'...'
rm -rf ${docsdir}*
mv deploy/* ${docsdir}

