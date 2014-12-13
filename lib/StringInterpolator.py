import re


variable_pattern = re.compile('{{(\S*)}}')


def interpolate_string(string, environment):
    global variable_pattern

    for variable in re.findall(variable_pattern, string):
        if variable not in environment.keys():
            raise RuntimeError("Could not resolve value for {0}".format(string))

        string = re.sub('{{{{{0}}}}}'.format(variable), environment[variable], string)

    return string
