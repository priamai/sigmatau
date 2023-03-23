"""
Module Docstring
"""

__author__ = "Paolo Di Prodi"
__version__ = "0.1.0"
__license__ = "Apache GPL 2"

import argparse
import os
import logging
from pathlib import Path
from .schemas import *

# create logger
logger = logging.getLogger('sigmatau')
logger.setLevel(logging.INFO)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

def main(args):
    """ Main entry point of the app """
    sigma = args.sigma
    tau = args.tau
    stats = args.stats

    if args.folder:
        logger.info(f'Scanning folder {args.folder}')
        logger.info(f'Sigma = {args.sigma}')
        logger.info(f'Tau = {args.tau}')
        p = Path(args.folder).glob('**/*.yml')
        files = [x for x in p if x.is_file()]
        total_files = len(files)
        valid_sigma = 0
        valid_tau = 0
        for file in files:
            logger.info(file.name)
            if tau:
                try:
                    s = SigmaTau.parse_file(file)
                    missing = [k for k, v in s.dict().items() if v is None]
                    logger.info(f'Total missing fields {len(missing)}')
                    valid_tau += 1
                except Exception as e:
                    logger.error(e)
            if sigma:
                try:
                    s = Sigma.parse_file(file)
                    missing = [k for k, v in s.dict().items() if v is None]
                    logger.info(f'Total missing fields {len(missing)}')
                    valid_sigma += 1
                except Exception as e:
                    logger.error(e)

        logger.info(f'Total files {total_files}')
        logger.info(f'Total valid sigma files {valid_sigma}')
        logger.info(f'Total valid tau files {valid_tau}')
    else:
        logger.warning("Folder to scan is missing")
def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")

def run():
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument('-folder', type=dir_path)

    # Optional argument flag which defaults to False
    parser.add_argument("-s", "--sigma", action="store_true", default=False)
    parser.add_argument("-t", "--tau", action="store_true", default=False)
    parser.add_argument("-ss", "--stats", action="store_true", default=False)

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)

if __name__ == "__main__":
    run()