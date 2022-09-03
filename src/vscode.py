#!/usr/bin/python3

import glob
import json
import os


def workspace_root():
    return os.path.expanduser("~/Library/Application Support/Code/User/workspaceStorage")


def workspaces():
    workspace_files = glob.glob(f"{workspace_root()}/*/workspace.json")

    workspaces = []
    for workspace_file in workspace_files:
        with open(workspace_file) as fp:
            workspaces.append(json.load(fp))

    return workspaces


def workspace_to_item(workspace):
    if 'workspace' in workspace:
        uri_arg = '--file-uri'
        uri = workspace['workspace']
    elif 'external' in workspace:
        uri_arg = '--file-uri'
        uri = workspace['external']
    elif 'folder' in workspace:
        uri_arg = '--folder-uri'
        uri = workspace['folder']
    else:
        return None

    extension = '.code-workspace'
    title = uri.rsplit('/')[-1]
    if title.endswith(extension):
        title = title[:-len(extension)]

    item = {
        'uid': uri,
        'title': title,
        'subtitle': uri,
        'arg': [uri_arg, uri],
    }

    return item


if __name__ == '__main__':
    items = [item for item in [workspace_to_item(
        workspace) for workspace in workspaces()] if item]
    print(json.dumps({'items': items}, indent=2))
