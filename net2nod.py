#!/usr/bin/env python
# coding=utf-8
"""
input: route
output: vehicle information
"""
import os
import subprocess
import sys
from pathlib import Path
import pandas as pd

try:
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))
    from sumolib import checkBinary

except ImportError:
    sys.exit(
        "please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')"
    )

if __name__ == '__main__':
    sumo_cmd = "NETCONVERT -s test0.net.xml --amitran-output test0.nod.xml"
    subprocess.call(sumo_cmd, shell=True)

