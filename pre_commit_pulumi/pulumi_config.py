"""
** pulumi-config **
This hook is used to re-format the pulumi stack config files
"""

import argparse
from pathlib import PurePath
from subprocess import Popen, PIPE
import uuid

def get_stack(filepath_str: str):
    """
    From the filename, extract the directory and the stack name.

    Parameters
    ----------
    filename : str
        filepath to the pulumi stack configuration file

    Returns
    -------
    tuple
        directory, stack
    """
    filepath = PurePath(filepath_str)
    directory = filepath.parent
    filename = filepath.name
    # pulumi configs are always called 'Pulumi.<stack>.yaml'
    stack = filename.split(".")[1]
    return directory, stack

def remove_config(directory, stack):
    """
    Remove a dummy config value. When 'pulumi config rm' is called, it reformats the file to try to find the config value.
    We use this as a "formatter" for the config

    Parameters
    ----------
    directory : str
        Directory of the pulumi stack configuration file. Pulumi command has to run from this directory.
    stack : str
        Stack name to give to the pulumi command.

    Returns
    -------
    Popen
        Popen process of the pulumi command.
    """
    return Popen(["pulumi", "config", "--stack", stack, "rm", str(uuid.uuid4())], stderr=PIPE, stdout=PIPE, cwd=directory)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs='+')
    args = parser.parse_args()
    remove_config_procs = []
    # Run the commands in parallel
    for filename in args.files:
        directory, stack = get_stack(filename)
        remove_config_procs.append(remove_config(directory, stack))
    # Wait for all the commands to finish
    for proc in remove_config_procs:
        proc.wait()
