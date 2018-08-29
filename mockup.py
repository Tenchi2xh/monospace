#!/usr/bin/env python3

import re
import sys
import itertools

with open("mockup.page1", "r") as f:
    lines1 = f.read().splitlines()

with open("mockup.page2", "r") as f:
    lines2 = f.read().splitlines()

def length(line):
    csi = r"\033\[.*?m"
    plain = re.sub(csi, "", line)
    return len(plain)

max_length1 = length(max(lines1, key=length))
max_length2 = length(max(lines2, key=length))
max_lines = max(len(lines1), len(lines2))


for l1, l2 in itertools.zip_longest(lines1, lines2):
    if not l1: l1 = ""
    if not l2: l2 = ""
    spaces1 = " " * (max_length1 - length(l1))
    spaces2 = " " * (4 + max_length2 - length(l2))
    line = "  " + l1 + spaces1 + l2 + spaces2
    if len(sys.argv) > 1:
        print("\033[7m%s\033[m" % line)
    else:
        print(line)
