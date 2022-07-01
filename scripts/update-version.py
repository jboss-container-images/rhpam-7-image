#!/usr/bin/python3
# This script will to help to manage ibm bamoe components modules version, it will update all needed files
# Example of usage:
#   # move the current version to the next one or rcX
#   python3 scripts/update-version.py -v 7.15.1 --confirm
#
#   # to only see the proposed changes (dry run):
#   python3 scripts/update-version.py -v 7.15.1
#
# Version pattern is: X.YY.Z
# Dependencies:
#  ruamel.yaml

import argparse
import os
import re
import sys

from ruamel.yaml import YAML

# All ibm bamoe modules that will have the given version updated.
MODULES = {"businesscentral/modules/businesscentral", "businesscentral-monitoring/modules/businesscentral-monitoring",
          "controller/modules/controller", "dashbuilder/modules/dashbuilder", "kieserver/modules/kieserver",
          "process-migration/modules/process-migration", "smartrouter/modules/smartrouter"}

VERSION_REGEX = re.compile(r'7[.]\d{2}[.]\d{1}\b')
SHORTENED_VERSION_REGEX = re.compile(r'\b\s\d[.]\d{2}\b')


def yaml_loader():
    """
    default yaml Loader
    :return: yaml object
    """
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 1024
    yaml.indent(mapping=2, sequence=2, offset=0)
    return yaml


def get_shortened_version(version):
    return '.'.join([str(elem) for elem in str(version).split(".")[0:2]])


def update_version(version, confirm):
    """
    Update ibm bamoe components module.yaml to the given version.
    :param version: version to set into the module
    :param confirm: if true will save the changes otherwise will print the proposed changes
    """

    modules = []
    for md in MODULES:
        modules.append(os.path.join(md + "/", "module.yaml"))

    print("Modules to be updated: {0}".format(modules))

    try:
        for module2update in modules:
            with open(module2update) as m:
                lines = ""
                for line in m:
                    if 'backend' not in line:
                        li = SHORTENED_VERSION_REGEX.sub(" " + get_shortened_version(version), line)
                        li = VERSION_REGEX.sub(version, li)
                        lines += li
                    else:
                        lines += line

                data = yaml_loader().load(lines)

                if not confirm:
                    print("Applied changes on module [{0}]: \n".format(module2update))
                    print(data)
                    print("\n----------------------------------\n")

            if confirm:
                with open(module2update, 'w') as m:
                    yaml_loader().dump(data, m)

    except TypeError:
        raise


def update_main_readme(version, confirm):
    """
    Update ibm bamoe version on the main README file to the given version.
    :param version: version to set into the module
    :param confirm: if true will save the changes otherwise will print the proposed changes
    """

    readme = 'README.md'
    print("Updating file: {0}".format(readme))

    try:

        with open(readme) as rpa:
            # replace all occurrences of shortened version first
            plain = SHORTENED_VERSION_REGEX.sub(" " + get_shortened_version(version), rpa.read())
            # then update all full version everywhere
            plain = VERSION_REGEX.sub(version, plain)

            if not confirm:
                print("Applied changes on {0} [{1}]: \n".format(readme, rpa))
                print(plain)
                print("\n----------------------------------\n")

        if confirm:
            with open(readme, 'w') as rpa:
                rpa.write(plain)

    except TypeError:
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='IBM BAMOE Version Manager')
    parser.add_argument('-v', dest='t_version', help='update everything to the next version')
    parser.add_argument('--confirm', default=False, action='store_true', help='if not set, script will not update the '
                                                                              'ibm bamoe modules. (Dry run)')
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    else:
        # validate if the provided version is valid.
        # e.g. 7.15.0
        pattern = "d.d{2}.d"
        if VERSION_REGEX.match(args.t_version):
            print("Modules version will be updated to {0}".format(args.t_version))
            update_version(args.t_version, args.confirm)
            update_main_readme(args.t_version, args.confirm)

        else:
            print("Provided version {0} does not match the expected regex - {1}".format(args.t_version, pattern))
