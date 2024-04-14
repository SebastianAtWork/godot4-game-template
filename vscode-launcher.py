#!/usr/bin/env python3

import argparse
import os
import os.path
import shutil
import sys
from glob import glob

def find_workspace(project_path):
    workspaces = glob(os.path.join(project_path, "*.code-workspace")) + \
        glob(os.path.join(project_path, ".vscode", "*.code-workspace"))

    if len(workspaces) > 1:
        print("Multiple workspaces found (%s). Opening file in the first one: %s" % (workspaces, workspaces[0]), file=sys.stderr)

    if len(workspaces) > 0:
        return workspaces[0]

    return None

def localize_path(path):
    if os.name == "nt":
        return path.replace('/', '\\')
    return path

def launch_vscode(code_path, code_args):
    if os.name == 'nt':
        # Under Windows, paths with spaces need to be quoted.
        code_args = [('"%s"' % x if ' ' in x else x) for x in code_args]

    os.execv(code_path, code_args)

def main():
    parser = argparse.ArgumentParser(description='Launches VS Code, favoring the workspace')
    parser.add_argument('--code', '-c', default='code', help="The path to VS Code")
    parser.add_argument('--project', '-p', help="The path to the project")
    parser.add_argument('file', help="The file to open")
    input = parser.parse_args()

    file_path = localize_path(input.file)

    code_path = shutil.which(localize_path(input.code))
    if code_path is None:
        print("Unable to find path to %s" % input.code)
        sys.exit(1)

    workspace = None
    if input.project:
        project_path = localize_path(input.project)
        workspace = find_workspace(localize_path(project_path))
        if workspace is None:
            workspace = project_path

    code_args = [
        os.path.basename(code_path),
        workspace,
        '-g',
        file_path
    ]

    launch_vscode(code_path, code_args)

if __name__ == '__main__': main()