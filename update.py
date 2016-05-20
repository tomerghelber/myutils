import subprocess
import os
import re
import logging
import sys

REGEX = re.compile('(.+) \(Current: [\d\.]+ Latest: [\d\.]+ \[\w+\]\)')

updater_logger = logging.getLogger('updater')

def get_out_off_date_packages() -> frozenset:
    """
    Gets all the packages which connected to pip and out off date.

    :side-effect: prints

    :rtype: frozenset
    """
    updater_logger.info("Getting packages")
    pip_output_lines = subprocess.check_output(['pip', 'list', '-o']).decode().splitlines()
    packages = set()
    for line in pip_output_lines:
        regex_result = REGEX.findall(line)
        if 0 != len(regex_result):
            packages.add(regex_result[0])
    return frozenset(packages)


def package_updater(package_name: str):
    """
    Gets an package name and its version and update it.

    :side-effect: prints

    :type package_name: str
    :param package_name package name to update.
    """
    updater_logger.info('Checking package "{0:s}"'.format(package_name))
    try:
        updater_logger.info("\tUpdating.")
        output = subprocess.check_output(["pip", "install", "-U", package_name]).decode()
        if "Requirement already up-to-date" in output:
            logging.info("\tUp to date.")
        else:
            updater_logger.info("\tUpdated.")
            updater_logger.info(output)
    except subprocess.CalledProcessError:
        updater_logger.error("\tFailed to update.")


def set_logger():
    import logging.config
    d = {
        'version': 1,
        'formatters': {
            'detailed': {
                'class': 'logging.Formatter',
                'format': '%(asctime)s - %(levelname)-7s - %(name)s(%(threadName)s):  %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'detailed',
            },
        },
        'loggers': {
            'updater': {
                'level': 'INFO',
                'handlers': ['console']
            }
        },
    }
    logging.config.dictConfig(d)


def main():
    set_logger()
    updater_logger.info("Starting")
    packages = get_out_off_date_packages()
    if packages:
        for package in packages:
            package_updater(package)
        updater_logger.info("Finished")
    else:
        updater_logger.info("All Up to date")


if "__main__" == __name__:
    main()
