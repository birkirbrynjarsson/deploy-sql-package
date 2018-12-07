import json
import os
import platform
from shutil import which
import subprocess

import argparse

def parseargs():
    parser = argparse.ArgumentParser(
        prog='SQL Server Database Deployment with SqlPackage',
        description='MSSQL Database deployment tool that runs executions of SqlPackage from a JSON configuration input file'
    )
    parser.add_argument('configfile', type=argparse.FileType('r'), help='JSON deployment configuration file passed to SqlPackage')
    parser.add_argument('-f', '--force', dest='force', action='store_true', help='forces continuation of deployment script, ignoring any failing SqlPackage execution')
    # args set as global variable
    return parser.parse_args()


# Checks if SqlPackage is installed and returns its path
def getSqlPackageExecutable():
    sqlpackage = which('sqlpackage')
    if not sqlpackage and platform.system() == 'Windows':
        programFiles = os.getenv('ProgramFiles')
        sqlpackage = '{}\\Microsoft SQL Server\\150\\DAC\\bin\\SqlPackage.exe'.format(programFiles)
    if not sqlpackage or not os.path.isfile(sqlpackage):
        print('It looks like SqlPackage isn\'t installed, it can be downloaded from Microsoft\'s website!')
        quit()
    return sqlpackage


# Takes as input a dictionary of SqlPackage arguments and returns them as a single string
def getSqlPackageArguments(arguments):
    args = []
    for arg in arguments:
        if type(arguments[arg]) is dict:
            for value in arguments[arg]:
                args.append('/{}:{}={}'.format(arg, value, arguments[arg][value]))
        else:
            args.append('/{}:{}'.format(arg, arguments[arg]))
    return args


def deployDB(configfile, force=False):
    sqlPackage = getSqlPackageExecutable()
    configurations = json.load(configfile)
    
    for config in configurations:
        args = getSqlPackageArguments(configurations[config])
        sqlPackageWithArgs = [sqlPackage] + args
        print('\n\n\n--- : {}:\n\t{}\n\n'.format(config, sqlPackageWithArgs))
        execution = subprocess.run(sqlPackageWithArgs)
        if execution.returncode and not force:
            print('{} - deployment step failed!\nExiting...'.format(config))
            quit()



if __name__ == '__main__':
    args = parseargs()
    deployDB(args.configfile, args.force)