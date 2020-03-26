"""
    This file maps the ISO 639 standard language dictionary to the IETF language codes
    to produce a dictionary mapping IETF language code keys to ISO 639 language English
    names
"""
from pathlib import Path
import csv
import os


def main(iso_path, ietf_path):
    iso_path = Path(iso_path).absolute().resolve()
    iso_codes = read_iso(iso_path)
    ietf_path = Path(ietf_codes_path).absolute().resolve()
    ietf_codes = read_ietf(ietf_path)

    return format_dict(iso_codes, ietf_codes)


def read_iso(iso_path):
    if os.path.isfile(iso_path):
        iso_codes = {}
        with open(iso_path, encoding='UTF8') as f:
            reader = csv.reader(f)
            for row in reader:
                code = row[0]
                english = row[1]

                if code == 'alpha2' and english == 'English':
                    continue

                iso_codes[code] = english

        return iso_codes


def read_ietf(ietf_path):
    if os.path.isfile(ietf_path):
        ietf_codes = {}
        with open(ietf_path, encoding='UTF8') as f:
            reader = csv.reader(f)
            for row in reader:
                ietf = row[0]
                iso = row[1]
                territory = row[2]

                if ietf == 'lang' and iso == 'langType':
                    continue

                ietf_codes[ietf] = {'langType': iso, 'territory': territory}
        return ietf_codes


def format_dict(iso_dict, ietf_dict):
    formatted_dict = {}
    for i in ietf_dict:
        lang = ietf_dict[i]['langType']
        territory = ietf_dict[i]['territory']

        if lang not in iso_dict:
            continue
        label = iso_dict[lang]
        if len(territory.strip()) > 0:
            label = label + '-{}'.format(territory)
            if 'zh-Hans' in i:
                label = label + '-Simplified'
            if 'zh-Hant' in i:
                label = label + '-Traditional'

        formatted_dict[i] = label
    return formatted_dict


if __name__ == '__main__':
    iso_codes_path = Path('')
    ietf_codes_path = Path('')
    code_dict = main(iso_codes_path, ietf_codes_path)
