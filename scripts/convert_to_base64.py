"""Validate json from file and convert to base64 format
"""
import argparse
import base64
import json
import sys


def validate_json_and_covert_to_base64(input_file):
    """Read json from *input_file*, validate and convert to base64
    """
    input_str = input_file.read()
    input_str_validated = json.dumps(json.loads(input_str))
    return base64.b64encode(input_str_validated.encode()).decode()


def main(arguments):
    """Main script

    Try validate json and encode to base64
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'input_file', help="Input file", type=argparse.FileType('r'))
    args = parser.parse_args(arguments)
    # Validate json and convert to base64
    base64_encoded_result = validate_json_and_covert_to_base64(args.input_file)
    print(base64_encoded_result)
    # Close file handlers
    args.input_file.close()


if __name__ == '__main__':
    main(sys.argv[1:])
