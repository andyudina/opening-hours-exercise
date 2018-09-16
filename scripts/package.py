"""Create zip package from /src folder and installed 3d party packages
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile


def create_zip_package(output_file_name):
    """Zip source code from /src and dependencies
    """
    # Create temp directory
    dirpath = tempfile.mkdtemp()
    # Copy src directory to temp directory
    shutil.copytree('./src', os.path.join(dirpath, 'src'))
    # Install dependencies to the same directory
    subprocess.check_call(
        [
            sys.executable, '-m',
            'pip', 'install', '-r', 'requirements.txt',
            '-t', dirpath]
    )
    shutil.make_archive(
        output_file_name,
        'zip',
        root_dir=dirpath)
    # Remove temp dir
    shutil.rmtree(dirpath)


def main(arguments):
    """Main script

    Zip source code and dependencies
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'output_file', help="Output file", type=str)
    args = parser.parse_args(arguments)
    # Package source code
    create_zip_package(args.output_file)


if __name__ == '__main__':
    main(sys.argv[1:])
