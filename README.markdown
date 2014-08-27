# To help out 

Edit the html files in the content directory

# Building the docs

First, you will need to have hyde installed.  This can be done using conda

`conda install hyde`

at the top level of the docs repo, run

`hyde gen --regen`

this will create a deploy directory.

From the deploy directory, run

`python -m SimpleHTTPServer`

Now navigate to *localhost:8000* to view a local version of the docs