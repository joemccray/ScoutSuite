#!/usr/bin/env python

import argparse
import ast
import json
import os
import sys

from dateutil.parser import parse
from dateutil.tz import tzutc

from ScoutSuite.core.console import print_exception


def process_raw_response(args):
    """
    Processes a raw response from a cloud provider's API.

    :param args:
    :return:
    """

    try:
        with open(args.raw_response_file, 'r') as f:
            raw_response = f.read()
    except Exception as e:
        print_exception(f'Could not open raw response file: {e}')
        sys.exit(1)

    try:
        processed_response = _process_raw_response(raw_response, args)
    except Exception as e:
        print_exception(f'Could not process raw response: {e}')
        sys.exit(1)

    try:
        with open(args.processed_response_file, 'w') as f:
            json.dump(processed_response, f, indent=4, default=str)
    except Exception as e:
        print_exception(f'Could not write processed response to file: {e}')
        sys.exit(1)


def _process_raw_response(raw_response, args):
    """
    Processes a raw response from a cloud provider's API.

    :param raw_response:
    :param args:
    :return:
    """

    # The AWS CLI returns a string that can be converted to a dictionary after some cleanup
    if args.provider == 'aws':
        # The raw response is a string representation of a dictionary, with some values that need to be fixed
        # The date values are in the format "datetime.datetime(YYYY, MM, DD, HH, MM, SS, tzinfo=tzutc())"
        # The other values are either strings, integers, or booleans
        cleaned_value = raw_response.replace('datetime.datetime', '')
        cleaned_value = cleaned_value.replace('(', '"')
        cleaned_value = cleaned_value.replace(')', '"')
        cleaned_value = cleaned_value.replace(' ', '')
        cleaned_value = cleaned_value.replace(',tzinfo=tzutc()', '')
        object_value_dict = ast.literal_eval(cleaned_value)
    elif args.provider == 'azure':
        # The raw response is a JSON object that can be directly converted to a dictionary
        # Some values need to be fixed, such as strings that are actually dictionaries
        # The raw response also contains a lot of unnecessary information
        cleaned_value = raw_response.replace('\'', '"')
        cleaned_value = cleaned_value.replace('True', 'true')
        cleaned_value = cleaned_value.replace('False', 'false')
        cleaned_value = cleaned_value.replace('None', 'null')
        cleaned_value = cleaned_value.replace(' {}', ' \'{}\'')
        object_value_dict = ast.literal_eval(cleaned_value)
    elif args.provider == 'aliyun':
        # The raw response is a JSON object that can be directly converted to a dictionary
        # Some values need to be fixed, such as strings that are actually dictionaries
        # The raw response also contains a lot of unnecessary information
        object_value_dict = json.loads(raw_response)
    else:
        raise Exception(f'Unknown provider: {args.provider}')

    return object_value_dict


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Processes a raw response from a cloud provider\'s API.')
    parser.add_argument('--provider', required=True, help='The cloud provider (aws, azure, aliyun)')
    parser.add_argument('--raw-response-file', required=True, help='The path to the raw response file')
    parser.add_argument('--processed-response-file', required=True, help='The path to the processed response file')
    args = parser.parse_args()

    process_raw_response(args)
