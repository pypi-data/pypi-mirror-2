#!/bin/bash
# Script to build the self-bootstraping, indexable enstaller egg.
# The resulting egg is executable, but only on systems which have
# bash installed.

# Build notes:
#   * setuptools needs to be installed to run this script

VER=4.4.1
PY=2.7

SPEC=enstaller.egg-info/spec
mkdir -p $SPEC
sed -e "s/_VER_/$VER/" -e "s/_PY_/$PY/" <<EOF >$SPEC/depend
metadata_version = '1.1'
name = 'enstaller'
version = '_VER_'
build = 1

arch = None
platform = None
osdist = None
python = '_PY_'
packages = []
EOF


EGG=dist/enstaller-$VER-1.egg
rm -rf build dist
python$PY setup.py bdist_egg
sed -e "s/_PY_/$PY/" <<EOF >tmp.sh
#!/bin/bash
python_PY_ -c "import sys, os; sys.path.insert(0, os.path.abspath('\$0')); from egginst.bootstrap import cli; cli()" "\$@"
exit 0
EOF
cat tmp.sh dist/enstaller-*-py*.egg >$EGG
rm -f tmp.sh dist/enstaller-*-py*.egg
chmod +x $EGG

# egginfo --sd $EGG
# repo-upload --force --no-confirm $EGG
