#!/usr/bin/env python3

import argparse
import tempfile

import elli
from helpers.main_helper import setup_logging, create_spec_converter_z3
from helpers.python_ext import readfile
from synthesis.smt_logic import UFLRA


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Save smt2 queries generated by elli',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('spec', metavar='spec', type=str,
                        help='the specification file (anzu, acacia+, or python format)')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--moore', action='store_true', required=False,
                       default=False,
                       help='assume a Moore model')
    group.add_argument('--mealy', action='store_true', required=False,
                       default=True,
                       help='assume a Mealy model')

    parser.add_argument('--minsize', metavar='minsize', type=int, default=1, required=False,
                        help='start from size')
    parser.add_argument('--maxsize', metavar='maxsize', type=int, default=4, required=False,
                        help='stop at this size')

    parser.add_argument('-v', '--verbose', action='count', default=0)

    args = parser.parse_args()
    assert args.minsize <= args.maxsize

    logger = setup_logging(args.verbose)
    logger.info(args)

    with tempfile.NamedTemporaryFile(dir='./') as smt_file:
        smt_files_prefix = smt_file.name

    ltl3ba, solver_factory = create_spec_converter_z3(UFLRA(),
                                                      False,
                                                      True,
                                                      smt_files_prefix,
                                                      True)
    elli.check_real(readfile(args.spec),
                    readfile(args.spec.replace('.ltl', '.part')),
                    args.moore,
                    ltl3ba, solver_factory,
                    args.minsize, args.maxsize)
    solver_factory.down_solvers()
    exit(0)
