"""
Functions to work with OS process and so on.
"""
import subprocess

def call_subprocess_to_file(commands, filename):
    """
    Given a sequence of `commands` (as accepted by `subprocess.call`'s first argument) execute it
    redirecting output to the given `filename`.
    """
    f = open(filename, 'w')
    subprocess.call(commands, stdout=f)
    f.close()
