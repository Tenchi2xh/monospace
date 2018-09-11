#!/bin/bash

python -m monospace typeset resources/README.source.md -t html -l
cat resources/README.header.html > README.md
echo "" >> README.md
sed -n "/<pre>/,/<\/pre>/p" resources/README.source.html | sed -e '1s/.*<pre>/<pre>/' -e '$s/<\/pre>.*/<\/pre>/' >> README.md
