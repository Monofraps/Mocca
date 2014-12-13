import sys

from os import path, getcwd
from lib.MessageFormatter import set_verbosity, mocca_info
from lib.StringInterpolator import interpolate_string
from models.project import Project as ProjectModel
from lib.DotMoccaGrabber import find_mocca_file, validate_mocca_file
from lib.Actors import MoccaProject
from argparse import ArgumentParser

SCRIPT_DIR = path.dirname(path.realpath(__file__))
WORKING_DIR = getcwd()


def parse_args():
    argument_parser = ArgumentParser(description='Mocca meta checkout tool')

    sub_parsers = argument_parser.add_subparsers(title='Sub commands', help='Commands')
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
    dump_parser.add_argument(
        '--interpolate', '-i',
        help="Interpolate project variables",
        action='store_true'
    )
    dump_parser.set_defaults(func=cmd_dump)

    add_var_parser = sub_parsers.add_parser('add-var', help='Adds a project variable to the .mocca file')
    add_var_parser.add_argument(
        "name",
        help="Name of the variable",
        type=str)
    add_var_parser.add_argument(
        "value",
        help="Value of the variable",
        type=str,
        nargs='?',
        default='<(env')
    add_var_parser.set_defaults(func=cmd_add_var)

    argument_parser.add_argument(
        "--mocca_file",
        "-f",
        metavar='file',
        help="Path to the project's .mocca file",
        type=str,
        default=None)
    argument_parser.add_argument(
        '--verbosity',
        help="Verbosity level (0=Errors only, 1=Info and error messages, 2=All messages",
        type=int,
        default=1)

    return argument_parser.parse_args()


def load_mocca_file(mocca_file=None):
    if mocca_file is None:
        mocca_file = find_mocca_file(WORKING_DIR)

    validate_mocca_file(mocca_file)

    # Read project definition from .mocca file
    file_descriptor = open(mocca_file, 'r')
    mocca_project = ProjectModel.from_json_file(file_descriptor)
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
    ProjectModel().to_json_file(file_descriptor)
    file_descriptor.close()


def cmd_dump(args, project):
    mocca_info("Dumping project config of {0}".format(path.join(project.root, '.mocca')))

    string_representatoin = project.model.to_json_string()

    if args.interpolate:
        print(interpolate_string(string_representatoin, project.resolved_variables))
    else:
        print(project.model.to_json_string())


def cmd_add_var(args, project):
    mocca_info("Adding '{0}' to the project".format(args.name))
    project.model.variables.add(args.name, args.value)

    mocca_info("Added '{0}' with value '{1}'{2} to the project configuration".format(
        args.name,
        args.value,
        " which resolves to '{0}'".format(project.model.variables.get(args.name)) if args.value == '<(env' else ''))
    project.save()

if __name__ == '__main__':
    args = parse_args()
    set_verbosity(args.verbosity)

    if args.func is cmd_init:
        args.func(args)
        sys.exit(0)

    project = load_mocca_file(args.mocca_file)
    args.func(args, project)
