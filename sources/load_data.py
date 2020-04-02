import yaml
from os.path import join
import pandas as pd


def load_config():
    try:
        with open(join("documents", "config.yaml")) as yaml_file:
            try:
                doc = yaml.load(yaml_file, Loader=yaml.FullLoader)
            except:
                doc = yaml.load(yaml_file)
        return doc
    except:
        raise Exception("Can't load config file")


def load_words():
    try:
        return pd.read_csv(join("documents", "Word_bank.csv"), encoding='utf-8')
    except:
        raise Exception("Can't load Word_bank.csv file")


def change_to_int(value):
    try:
        return int(value)
    except ValueError:
        return value


def load_trials():
    try:
        with open(join("documents", "trials.csv"), encoding='utf-8') as f:
            csv_list = [[val.strip() for val in r.split(",")] for r in f.readlines()]
        (_, *header), *data = csv_list
        csv_dict = []
        for _, *values in data:
            csv_dict.append({key: change_to_int(value) for key, value in zip(header, values)})
        return csv_dict
    except:
        raise Exception("Can't load trials.csv file")


def load_training_trials(file_name):
    try:
        with open(join("documents", file_name), encoding='utf-8') as yaml_file:
            try:
                doc = yaml.load(yaml_file, Loader=yaml.FullLoader)
            except:
                doc = yaml.load(yaml_file)
        return doc
    except:
        raise Exception("Can't load {} file".format(file_name))
