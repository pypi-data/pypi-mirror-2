
import re

import subprocess
import tempfile

version_regex = re.compile('bibutils suite version (.*) date', re.MULTILINE)

def checkBibutilsVersion(min_version=4.6):
    """ Ensure that a certain Bibutils version is installed"""

    fp_out = tempfile.mktemp()
    pipe = subprocess.Popen('bib2xml --version', shell=True, stderr=subprocess.PIPE)
    output = pipe.stderr.read()
    mo = version_regex.search(output)
    if mo:
        s = mo.group(1)

        try:
            version = float(s)
        except TypeError:
            version = None
        if version and version >= min_version: 
            return version
        else:
            raise RuntimeError('Minimum requirement is Bibtutils %s, found %s' % (min_version, version))

    raise RuntimeError('Unable to determine Bibtutils version')




