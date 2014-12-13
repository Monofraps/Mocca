from . import TermColors

V_ERROR = 0
V_INFO = 1
V_DEBUG = 2

verbosity = V_INFO


def mocca_info(msg):
    """
    Prints a formatted info message to stdout
    :param msg: The message to output
    """

    if _should_log(V_INFO):
        print(colorize_message("{0}> {1}".format('_' * 20, msg), TermColors.INFO))


def mocca_error(msg):
    """
    Prints a formatted error message to stdout
    :param msg: The message to output
    """

    if _should_log(V_ERROR):
        print(colorize_message("{0}> {1}".format('_' * 20, msg), TermColors.FAIL))


def mocca_debug(msg):
    """
    Prints a formatted debug message to stdout
    :param msg: The message to output
    """

    if _should_log(V_DEBUG):
        print("{0}> {1}".format('_' * 20, msg))


def _should_log(verbosity_level):
    """ Returns whether the given verbosity level should be logged """
    return verbosity >= verbosity_level


def colorize_message(msg, color):
    """ Prepends color in front of msg and appends TermColors.ENDC at the end """
    return "{0}{1}{2}".format(color, msg, TermColors.ENDC)


def set_verbosity(new_verbosity):
    global verbosity
    verbosity = new_verbosity

