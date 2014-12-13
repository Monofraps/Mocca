from os import path, getcwd
from models.project import Project
from lib.DotMoccaGrabber import FindMoccaFile, ValidateMoccaFile
from lib.Actors import MoccaDependency, MoccaProject
from argparse import ArgumentParser
import sys

SCRIPT_DIR = path.dirname(path.realpath(__file__))
WORKING_DIR = getcwd()


def parse_args():
    argumentParser = ArgumentParser(description='Mocca meta checkout tool')

    sub_parsers = argumentParser.add_subparsers(title='Sub commands', help='Commands')
    add_dependency_parser = sub_parsers.add_parser('add', help='Adds a dependency')
    add_dependency_parser.add_argument(
        "path",
        help="Path to where the repo should be checked out",
        type=str)
    add_dependency_parser.add_argument(
        "url",
        help="Repository url",
        type=str)
    add_dependency_parser.add_argument(
        "--target-os", '-t',
        help="The os on which this dependency is required",
        action='append',
        type=str)
    add_dependency_parser.add_argument(
        "--vcs", '-v',
        help="Set the version control system",
        type=str,
        default='git')
    add_dependency_parser.add_argument(
        "--branch", '-b',
        help="The branch to checkout",
        type=str,
        default='master')
    add_dependency_parser.set_defaults(func=cmd_add_dependency)

    sync_parser = sub_parsers.add_parser('sync', help='Syncs dependencies')
    sync_parser.set_defaults(func=cmd_sync)

    init_parser = sub_parsers.add_parser('init', help='Initialize a new mocca project')
    init_parser.set_defaults(func=cmd_init)

    dump_parser = sub_parsers.add_parser('dump', help='Dumps mocca project configuration')
    dump_parser.set_defaults(func=cmd_dump)

    argumentParser.add_argument(
        "--mocca_file",
        "-f",
        metavar='file',
        help="Path to the project's .mocca file",
        type=str,
        default=None)

    return argumentParser.parse_args()


def load_mocca_file(mocca_file=None):
    if mocca_file is None:
        mocca_file = FindMoccaFile(WORKING_DIR)

    ValidateMoccaFile(mocca_file)

    # Read project definition from .mocca file
    file_descriptor = open(mocca_file, 'r')
    mocca_project = Project.FromJsonFile(file_descriptor)
    file_descriptor.close()

    return MoccaProject(mocca_project, path.dirname(path.realpath(mocca_file)))


def cmd_add_dependency(args, project):
    dependency = project.model.dependencies.add()
    dependency.path = args.path
    dependency.url = args.url
    dependency.vcs = args.vcs
    dependency.branch = args.branch

    project.save()


def cmd_sync(args, project):
    project.sync_dependencies()


def cmd_init(args):
    file_descriptor = open(path.join(WORKING_DIR, '.mocca'), 'w')
    Project().ToJsonFile(file_descriptor)
    file_descriptor.close()


def cmd_dump(args, project):
    print(project.model.ToJsonString())

if __name__ == '__main__':
    args = parse_args()
    if args.func is cmd_init:
        args.func(args)
        sys.exit(0)

    project = load_mocca_file(args.mocca_file)
    args.func(args, project)
