## Test vs. Production

There is only one domain for this site - docs.binstar.org - but there is a "test" site located at docs.binstar.org/draft/.  Before being deployed to the primary domain, changes should be deployed to this area of the site.  This can be done by running the /scripts/deploydraft.sh script.


## Site Change Process

Please use the pull request format to submit changes and corrections to the site.

## Running This Site Locally
Pull a copy of the website from github binstar/docs.binstar.org.git
```
# Clone to local machine and switch to master or dev branch
$ git clone git@github.com:binstar/docs.binstar.org.git
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

### Deploying to the draft site:

```
# Navigate to the 'scripts' directory:
cd scripts
# Execute the 'deploydraft.sh' bash script:
./deploydraft.sh
```

Review your changes at http://docs.binstar.org/draft/


### Submitting a PR:

1) From https://github.com/Binstar/docs.binstar.org/, select the branch you created from the branches dropdown menu. 
2) Select the 'Pull Request' option.
3) Include a meaningful message and @-tag whomever should review/merge your changes.
