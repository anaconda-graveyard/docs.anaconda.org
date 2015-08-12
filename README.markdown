## Test vs. Production

There is only one domain for this site - docs.anaconda.org - but there is a "test" site located at docs.anaconda.org/draft/.  Before being deployed to the primary domain, changes should be deployed to this area of the site.  This can be done by running the /scripts/deploydraft.sh script.


## Site Change Process

Please use the pull request format to submit changes and corrections to the site.

## Running This Site Locally
Pull a copy of the website from github Anaconda-Server/docs.anaconda.org.git
```
# Clone to local machine and switch to master or dev branch
$ git clone git@github.com:Anaconda-Server/docs.anaconda.org.git
$ git checkout master
```
We use the Hyde engine which uses django template structure for creating pages.
```
$ conda install hyde
```

You will have to generate the static content that comprises the site at least once on installation:

**``` hyde gen ```**.

This will generate static content, stored in the 'deploy' directory.

After making changes you can view the updated content one of three ways:
* **```hyde gen ```** - recommended for minor changes - will regenerate sections of site where a diff indicates changes.
* **```hyde gen --regen```** - recommended for significant changes and/or the addition of new media assets to the site - will regenerate entire site.
* or add the **```?regen```** querystring to the page url in your browser window,  - recommended for localized changes - will update only that specific page.


To serve the site locally & review your changes, from the root of the website repo execute from the command line:
```
$ hyde serve -p 8080
```
You can then view the changes locally by opening your browser and going to **http://localhost:8080**.

**Note:** If you get an error try check to make sure you are in the root of the repository or check to make sure you installed Hyde correctly.

## Making Changes to the Site

After your changes are complete, you can push them to github on a new branch, deploy them to the 'draft' site for review, and submit a PR:

### Pushing to Github on a New Branch:

```
# Create a new branch
git checkout -b content/adding-examples
# Add your changed files to this new branch
$ git add /content/_examples/new_page.html
# Including a meaningful commit message
$ git commit -m 'adding more examples'
# Pull in any changes since you last pulled
$ git pull
# Push your branch to github.
$ git push
```

## Deploying to S3

The docs.anaconda.org site is housed in an S3 bucket.  In order to deploy to this bucket, you need the `sc3md` tool, relevant S3 credentials, and an appropriate `s3cfg` configuration file.

1. Install s3cmd from this [site](http://s3tools.org/download)
  * **Note**: if you are using a conda environment to build/deploy, remember to install s3cmd into this environment.
2. For S3 credentials, email it-help@continuum.io.
3. To configure your s3cmd instance, issue the following command:

  ```
  s3cmd --configure
  ```

Complete the prompts which follow using the S3 credentials you've received from the Documentation or AS team.  At a minimum you must supply an Access Key & a Secret Key; you may configure additional variables and options as desired.

After you have installed & configured the s3cmd tool, you will be able to perform publishes to the S3 bucket.


### Deploying to the draft site:

```
# Navigate to the 'scripts' directory:
cd scripts
# Execute the 'deploydraft.sh' bash script:
./deploydraft.sh
```

Review your changes at http://docs.anaconda.org/draft/

### Deploying to the production site:

```
# Navigate to the 'scripts' directory:
cd scripts
# Execute the 'deploy.sh' bash script:
./deploy.sh
```

Review your changes at http://docs.anaconda.org/

### Submitting a PR:

1) From https://github.com/Anaconda-Server/docs.anaconda.org/, select the branch you created from the branches dropdown menu.
2) Select the 'Pull Request' option.
3) Include a meaningful message and @-tag whomever should review/merge your changes.
