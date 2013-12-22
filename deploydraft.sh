#!/bin/bash

docsdir='/srv/deploy/wakaridocsdraft/'
deploydir='deploy'
deployfile='deploy.zip'

if [ ! -f ${deployfile} ]; then
  echo 'Deploy file not found ['${deployfile}'].'
  exit 1
fi

if [ ! -d ${docsdir} ]; then
  echo 'Docs directory not found ['${docsdir}'].  Please create it.'
  exit 1
fi

echo 'Deploying site to '${docsdir}'...'
rm -rf ${docsdir}*
rm -rf ${deploydir}
tar xvf ${deployfile}
mv ${deploydir}/* ${docsdir}

