
import sys
import logging
import argparse
import shutil
import tempfile

import pkg_resources

import csar

LOG = logging.getLogger(__name__)

def csar_validate_func(namespace):
    try:
        csar.read(namespace.source,
                  namespace.destination,
                  namespace.no_verify_cert)
    finally:
        LOG.debug('Calling rmtree: {}'.format(namespace.destination))
        shutil.rmtree(namespace.destination, ignore_errors=True)

def parse_args(args_list):
    """
    Entry point
    """
    parser = argparse.ArgumentParser(description='CSAR Validation tool')
    parser.add_argument('-v', '--verbose',
                        dest='verbosity',
                        action='count',
                        default=0,
                        help='Set verbosity level (can be passed multiple times)')

    subparsers = parser.add_subparsers(help='csar-validate')

    csar_open = subparsers.add_parser('csar-validate')
    csar_open.set_defaults(func=csar_validate_func)
    csar_open.add_argument(
        'source',
        help='CSAR file location')
    csar_open.add_argument(
        '-d', '--destination',
        help='Output directory to extract the CSAR into',
        required=True)
    csar_open.add_argument(
        '--no-verify-cert',
        action='store_true',
        help="Do NOT verify the signer's certificate")

    return parser.parse_args(args_list)


def init_logging():
#    verbosity = [logging.WARNING, logging.INFO, logging.DEBUG]
#
    logging.basicConfig(level=logging.INFO)

def main():
    args = parse_args(sys.argv[1:])
#    logging.basicConfig(level=logging.DEBUG)
    init_logging()
    return args.func(args)


if __name__ == '__main__':
    main()

