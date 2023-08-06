#!/bin/sh

python pycdep.py --sandbox sandbox -R sandbox --common-root-folder sandbox --strip-common-root-folder --prefix-length 3 --hierarchy-definition sandbox/hierarchy.txt

