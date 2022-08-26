"""Supporting functions for the GitHub Actions `check-release-number
composite action

The functions this file can be used to check whether a version increment
follows Semantic Versioning conventions.
"""

import argparse
import sys


class Version:
    """Stores a program version

    This object stores a 3-digit program version based on Semantic Versioning
    (https://semver.org/) and simplifies retrieving any or all of the major,
    minor, and patch version numbers
    """

    print_leading_v = False

    def __init__(self, major, minor, patch):
        self._major = self.__check_input(major)
        self._minor = self.__check_input(minor)
        self._patch = self.__check_input(patch)

    def __eq__(self, value: object):
        if not isinstance(value, Version):
            return False

        if (self._major != value._major) or (self._minor != value._minor) \
                or (self._patch != value._patch):
            return False

        return True

    @property
    def major(self):
        """Returns the major version number"""
        return self._major

    @property
    def minor(self):
        """Returns the minor version number"""
        return self._minor

    @property
    def patch(self):
        """Returns the patch version number"""
        return self._patch

    def __str__(self):
        return (f'{"v" if self.print_leading_v else ""}'
                f'{self.major}.{self.minor}.{self.patch}')

    def __check_input(self, value):
        # Check that input is a number
        try:
            value_float = float(value)
        except:
            raise TypeError('Input must be a number')

        # Check that input is a positive integer
        if value_float < 0:
            raise ValueError('Input must be positive')

        if value_float.is_integer():
            return int(value_float)

        raise TypeError('Input must be an integer')

    def increment(self, increment_type: str):
        """Increments the stored version

        Increments the version currently stored in the object, and returns
        a new ``Version`` object with the incremented version
        """
        if increment_type.lower() == 'major':
            return Version(self.major + 1, 0, 0)
        elif increment_type.lower() == 'minor':
            return Version(self.major, self.minor + 1, 0)
        elif increment_type.lower() == 'patch':
            return Version(self.major, self.minor, self.patch + 1)
        else:
            raise ValueError('Argument "increment_type" must be one '
                             'of "major," "minor," or "patch"')


def check_version_file_increment(old_version_str: str, new_version_str: str):
    """Checks whether a given version increment is valid"""
    # Parse version
    v0 = parse_version(old_version_str)
    v1 = parse_version(new_version_str)

    # Check whether new version is valid
    valid_version = (v1 in valid_versions(v0))

    return valid_version, v0, v1


def parse_version(version: str):
    """Converts a string in the form 'v#.#.#' to a Version object"""
    # Strip leading and trailing whitespace
    version = version.strip()

    # Remove leading 'v'
    if version.lower().startswith('v'):
        version = version[1:]

    # Convert to `Version` object
    version_numbers = [float(i) for i in version.split('.')]
    return Version(*version_numbers)


def valid_versions(current_version: Version):
    """Lists acceptable incremented versions

    Returns a list of valid versions, where valid versions have been
    either a major, minor, or patch version number incremented by 1 from
    the inputted old version
    """
    if not isinstance(current_version, Version):
        raise TypeError(
            'Argument "current_version" must be of type "utils.Version"')

    return [
        current_version.increment('major'),
        current_version.increment('minor'),
        current_version.increment('patch'),
    ]


if __name__ == '__main__':
    description = (
        'Checks whether the user has incremented the version following '
        'Semantic Versioning (https://semver.org/). More specifically,'
        'this script checks whether one and only one of the version numbers '
        '(major, minor, patch) have been incremented by exactly one (and '
        'any following version numbers set to zero).'
    )
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-o', '--old-version', required=True,
                        help='String containing previous software version')
    parser.add_argument('-n', '--new-version', required=True,
                        help='String containing new software version')
    args = parser.parse_args()

    # Check whether version increment is valid
    valid, old_version, new_version = check_version_file_increment(
        old_version_str=args.old_version,
        new_version_str=args.new_version
    )

    # Configure versions to be displayed with the leading "v"
    Version.print_leading_v = True

    # Display results in terminal
    RED = '\033[1;31m'
    GREEN = '\033[1;32m'
    PLAIN = '\033[0m'

    if valid:
        print(f'{GREEN}Version increment from {old_version} '
              f'to {new_version} is valid{PLAIN}')
    else:
        print(f'{RED}Version increment from {old_version} to '
              f'{new_version} is not valid{PLAIN}')
        print(f'{RED}Valid versions: '
              f'{[str(i) for i in valid_versions(old_version)]}{PLAIN}')
        sys.exit(1)
