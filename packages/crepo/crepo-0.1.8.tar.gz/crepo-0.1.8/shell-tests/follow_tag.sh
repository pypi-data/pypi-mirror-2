#!/bin/bash -x

set -e

BINDIR=$(readlink -f $(dirname $0))
CREPO=$BINDIR/../crepo.py

TESTDIR=${TESTDIR:-/tmp/follow_tag.$$}
mkdir -p $TESTDIR
cd $TESTDIR


################
# REPO A
################
mkdir repo_a
pushd repo_a
git init
echo "First commit" > file_a
git add . && git commit -a -m '1'

echo "Second commit" > file_b
git add . && git commit -a -m '2'
git tag commit_b

echo "Third commit" >> file_a
git add . && git commit -a -m '3'

REPO_A=`pwd`

popd

##############
# Run crepo in a new dir
##############
mkdir tests
pushd tests

cat > manifest.json <<EOF
{   /* comment here! */
  "remotes":
    {"origin": { "fetch": "$TESTDIR/%(name)s" }},
/* multi
line
comment*/
  "projects":
    {"repo_a": { "track-tag": "commit_b" }}
}
EOF

$CREPO sync

## Check that the checkout is correct
pushd repo_a
test "$(git symbolic-ref HEAD)" == "refs/heads/commit_b"
test $(git remote) == "origin"
test -f file_a
popd
