## Overview

There is only one domain for this site - docs.anaconda.org - but there is a "test" site located at docs.anaconda.org/draft/.

Although some parts of the continuum.io site have traditionally been pushed to a test server each Tuesday and to the main server each Thursday, any contributor is welcome to deploy changes to docs.anaconda.org/draft and to docs.anaconda.org at any time.

The process for editing docs.anaconda.org contains a few steps. Overview: clone this repository locally, install dependencies, create a new branch, make your changes, test them locally with Hyde, run deploydraft.sh to push the changes to docs.anaconda.org/draft, once you're satisfied with them push your new branch to GitHub, make a pull request, and merge your new branch into the master branch, then run deploy.sh to push your changes to docs.anaconda.org.

## Clone this repository locally:

If you do not already have a GitHub working directory, go to your home directory and make one.

```
cd
mkdir githubwork
```

Go to your GitHub working directory:

``cd ~/githubwork``

Clone the repository:

``git clone git@github.com:Anaconda-Server/docs.anaconda.org.git``

This creates a local copy of this repository.

## Install dependencies:

```
cd docs.anaconda.org
conda env create
source activate docs.anaconda.org
```

Running `conda env create` without any arguments creates a new environment using the environment.yml file in the current directory, which was downloaded from the repository itself.

You only need to clone the repository and install dependencies once, but all the following steps will be done each time you make a new change.

## Update packages:

```
conda update --all
```

Running `hyde gen --regen` calls commands such as `anaconda worker -h` to build the Command Reference section of the documentation. If a new version of anaconda or anaconda-client or anaconda-build has been released since you installed the docs.anaconda.org environment, then building the site in your environment will produce docs reflecting the old versions you have installed, not the current versions, and this is a common source of errors. To prevent this, always update your packages before building the site.

## Create a new branch:

Enter the repository and make sure the master branch is selected:

```
cd ~/githubwork/docs.anaconda.org
git checkout master
```

Make a new branch, replacing make-some-change with a branch name that describes the change you are making:

``git checkout -b make-some-change``

## Make your changes:

Use local editors to change the docs files as necessary. Edit the source files in the content directory, not the Hyde output files in the deploy directory.

## Test your changes locally with Hyde:

We use the Hyde engine which uses django template structure for creating pages.

You will have to run Hyde to generate the static content that comprises the site at least once:

``hyde gen``

This will generate static content, stored in the 'deploy' directory.

To review the changes in a browser, we run Hyde as a local web server.

Go to the root of the website repository, which contains the site.yaml file and the deploy directory:

``cd ~/githubwork/docs.anaconda.org``

Run the Hyde server on port 8080:

``hyde serve -p 8080``

Now open a browser and go to the URL ``http://localhost:8080`` to review the changes.

**NOTE:** If you get an error check to make sure you are in the root of the repository and check to make sure you installed Hyde correctly.

Each time you make changes, you will want to regenerate the Hyde content and review the changes in a browser. There are three ways to regenerate the content.

1) When the Hyde server is running, you can load a page in a browser window with ``?regen`` added to the end of the URL. This is a "querystring" that tells Hyde to regenerate that specific page, and this method is recommended for localized changes.

2) You can shut down the Hyde server with control-c in the terminal window, run ``hyde gen``, and restart the hyde server with ``hyde serve -p 8080``. This regenerates sections of the site where a diff indicates changes, and is recommended for minor changes.

3) You can shut down the Hyde server with control-c in the terminal window, run ``hyde gen --regen``, and restart the hyde server with ``hyde serve -p 8080``. This regenerates the entire site and is recommended for significant changes and/or the addition of new media assets to the site. If in doubt, you can always use this method.

Once you are satisfied with your changes, close the browser and shut down the Hyde server with control-c in the terminal window.

## Run deploydraft.sh to push the changes to docs.anaconda.org/draft

docs.anaconda.org (including docs.anaconda.org/draft) is hosted on Amazon Simple Storage Service (S3) buckets. When it was first set up the bucket was named docs.anaconda.org. However, we have since learned that bucket names containing periods can only work with http and not https. A new bucket named docs-anaconda-org was created, but as of 2015 Aug 13 we have not yet successfully migrated to it and are currently using docs.anaconda.org and http only for both uploading and downloading. This means that when you run ``s3cmd --configure`` you will have to set the "Use HTTPS Protocol" option to no.

To deploy to the S3 bucket, you need the `s3cmd` tool, relevant S3 credentials, and an appropriate `s3cfg` configuration file.

The `s3cmd` tool was installed when you created the environment.

For S3 credentials, email it-help at continuum.io. They are different for each user and not shared with a group, and they are the same as the Access Key and Secret Key used for Amazon Web Services (AWS).

You will need gnupg (also known as gpg). MacPorts is a good way to install it on OS X. A .pkg file is available at http://guide.macports.org/#installing.macports . After installing, close and re-open your terminal, then run ``sudo port selfupdate`` then ``sudo port install gnupg`` and then ``type gpg`` and copy the path that shows the location of gpg.

To configure your s3cmd instance and create the s3cfg file, run ``s3cmd --configure`` and complete the prompts, using your S3 credentials as the Access Key and Secret Key. Leave the "Encryption password" blank. For "Path to GPG program" paste the path you found with ``type gpg``. Set "Use HTTPS Protocol" to "No". Leave "HTTP Proxy server name" blank.

Now you should be able to use the deploydraft.sh and deploy.sh scripts.

Go to the root directory of the website repository and run the deploydraft.sh script:

```
cd ~/githubwork/docs.anaconda.org
./scripts/deploydraft.sh
```

Review your changes at http://docs.anaconda.org/draft/ .

## Push your new branch to GitHub

Add the new files to the staging area to be committed until ``git status`` shows that all added or modified files are staged:

``git add newfile.html``

Commit the changes and write a meaningful commit message:

``git commit``

Push your new branch to GitHub:

``git push origin make-some-change``

## Make a pull request, and merge your new branch into the master branch

1) From https://github.com/Anaconda-Server/docs.anaconda.org/, select the branch you created from the branches dropdown menu.

2) Select the 'Pull Request' option.

3) Include a meaningful message and @-tag whomever should review/merge your changes.

## Run deploy.sh to push your changes to docs.anaconda.org

Once your changes are merged into the master branch on GitHub, update your local copy:

```
cd ~/githubwork/docs.anaconda.org
git checkout master
git pull
```

Regenerate the content with Hyde:

``hyde gen --regen``

Go to the root directory of the website repository and run the deploy.sh script:

```
cd ~/githubwork/docs.anaconda.org
./scripts/deploy.sh
```

Review your changes at http://docs.anaconda.org/ .

## Renaming files and removing files from past versions

If you rename a file on the site from alpha.html to bravo.html and run the scripts, they will upload the new bravo.html, but the old alpha.html file will still be on the server with the outdated and probably incorrect content. To delete such a file, you may edit the scripts to change 's3cmd -c ~/.s3cfg sync --recursive deploy/ s3://"$BUCKET"/' to 's3cmd -c ~/.s3cfg sync --recursive --delete-removed deploy/ s3://"$BUCKET"/' and change 's3cmd -c ~/.s3cfg sync --recursive deploy/ s3://"$BUCKET"/draft/' to 's3cmd -c ~/.s3cfg sync --recursive --delete-removed deploy/ s3://"$BUCKET"/draft/' and then run them, which will delete removed files such as alpha.html. However, running deploy.sh with this modification will also remove the entire draft section of the site. When you are done, please change the scripts back to their earlier version.
