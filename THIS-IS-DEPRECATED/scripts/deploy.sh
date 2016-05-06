COMMIT_HASH=`git show --quiet | head -n1`
VERSION=`python -c "print '$COMMIT_HASH'.split()[-1][:8]"`
BUCKET="docs.anaconda.org"

# git tag "$VERSION"
hyde gen -r -c prod.yaml

s3cmd -c ~/.s3cfg sync --recursive deploy/ s3://"$BUCKET"/

# echo "Don't Forget to update the binstar_app Config file! VERSION=$VERSION"
echo
echo "CDN URL is: docs.anaconda.org.s3-website-us-east-1.amazonaws.com"
echo "Website is: docs.anaconda.org"
