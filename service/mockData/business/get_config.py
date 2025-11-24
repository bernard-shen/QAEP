#!/usr/bin/python
# -*- coding: UTF-8 -*-
# --Author: Bernard--
import sys
import yaml
import os
from pathlib import Path


BASE_DIR = (Path(__file__)).parent.parent
CONFIG_PATH = BASE_DIR / 'config/env.yaml'


def get_configs(first_name, second_name=None, locator_path=CONFIG_PATH):
    with open(locator_path, 'r', encoding='utf-8') as f:
        data_dict = yaml.safe_load(f.read())
    if second_name:
        return data_dict[first_name][second_name]
    else:
        return data_dict[first_name]


if __name__ == '__main__':
    locations = get_configs("web_env", 'database')
    print(type(locations))
    print(locations)
