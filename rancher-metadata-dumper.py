#!/usr/bin/python3.4

# Copyright 2016 Daniel Dent (https://www.danieldent.com/)

import sys
import urllib.parse
import urllib.request
import json
import yaml


def get_self_metadata():
    headers = {
        'User-Agent': "rancher-metadata-dumper/0.1",
        'Accept': 'application/json'
    }
    req = urllib.request.Request('http://rancher-metadata/2015-12-19/self/service/metadata', headers=headers)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf8 '))


def dump_to_file(format_type, content, file_name):
    if format_type == 'JSON':
        dump_to_json(content, file_name)
    elif format_type == 'YAML':
        dump_to_yaml(content, file_name)


def dump_to_json(content, file_name):
    with open(file_name, 'w') as output_file:
        json.dump(content, output_file, indent=2)


def dump_to_yaml(content, file_name):
    with open(file_name, 'w') as output_file:
        yaml.dump(content, output_file, default_flow_style=False)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: " + sys.argv[0] + " [YAML|JSON] output_filename")
        exit(1)

    output_type = sys.argv[1]
    if output_type != 'YAML' and output_type != 'JSON':
        print("Unknown requested output type.")
        exit(1)

    output_filename = sys.argv[2]

    dump_to_file(output_type, get_self_metadata(), output_filename)
