import difflib
import subprocess
import re
import os
import itertools

PYTHON_VERSION_REGEX_FROM_PATH = re.compile('.*python(\d\d).*')

def get_pip_list(version):
    """
    :param version: Python version.
    :type version: float
    :return: List of installed packages in python.
    :rtype: list[str]
    """
    cmd = 'pip{:.1f} list'.format(version)
    return subprocess.getoutput(cmd).splitlines(True)

def find_python_versions():
    """
    :return: Local python versions.
    :rtype: frozenset[float]
    """
    python_vesrions = list()
    for i in os.environ['PATH'].split(';'):
        for result in RC.findall(i.lower()):
            if result.isdigit():
                python_vesrions.append(int(result) / 10)
    return frozenset(python_vesrions)

def real_diff(diff):
    """
    :param diff: The diff to check.
    :type diff: str
    :return: True if diff is real (starts with '  ')
    :rtype: bool
    """
    return not diff.startswith('  ')

def find_local_python_diffs():
    """
    """
    differ = difflib.Differ()
    python_versions = find_python_versions()
    python_versions_packages = {python_version: get_pip_list(python_version) for python_version in python_versions}
    for (python_version1, python_version_packages1), (python_version2, python_version_packages2) in itertools.combinations(python_versions_packages.items(), 2):
        print(python_version1, '->', python_version2)
        diffs = differ.compare(python_version_packages1, python_version_packages2)
        real_diffs = filter(real_diff, diffs)
        print(''.join(real_diffs))

if __name__ == '__main__:
    find_local_python_diffs()
