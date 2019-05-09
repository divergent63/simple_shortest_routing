#!/usr/bin/env python
# coding=utf-8
"""

"""
import os
import subprocess
import sys

from pathlib import Path

try:
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))
    from sumolib import checkBinary

except ImportError:
    sys.exit(
        "please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')"
    )


if __name__ == '__main__':
    sumo_home = os.environ.get("SUMO_HOME")
    # SUMO_HOME=/usr/local/share/sumo-1.1.0         # in Ubuntu Server
    # SUMO_HOME=g:\software\SUMO\sumo-win64-1.0.1\sumo-1.0.1            # in Windows 10

    # input_xml = Path(Path(os.getcwd()).parent).parent / 'data' / 'type_2' / 'conf' / 'fcd_ped.xml'
    input_xml = Path(os.getcwd()) / 'conf' / 'fcd.xml'

    subprocess.call(
        "python " + str(sumo_home) + "/tools/xml/xml2csv.py " + str(input_xml) + " --separator ,",
        shell=True
    )
