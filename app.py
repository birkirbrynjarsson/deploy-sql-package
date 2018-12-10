import json
import os
from pathlib import Path
import platform
from shutil import which
import subprocess
import sys

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
        sys.exit()
    return sqlpackage


def getSqlCmdExecutable():
    sqlcmd = which('sqlcmd')
    if not sqlcmd and platform.system() == 'Windows':
        programFiles = os.getenv('ProgramFiles')
        sqlcmd = '{}\\Microsoft SQL Server\\110\\Tools\\Binn\\SQLCMD.exe'.format(programFiles)
    if not sqlcmd or not os.path.isfile(sqlcmd):
        print('It looks like SqlCmd isn\'t installed, it can be downloaded from Microsoft\'s website or from within Visual Studio!')
        sys.exit()
    return sqlcmd


def convertSqlPackageFilePathsForWindows(sqlPackageArguments):
    for key in sqlPackageArguments:
        if str(key) in ['SourceFile', 'sf', 'TargetFile', 'tf', 'DiagnosticsFile', 'df', 'DeployScriptPath', 'dsp', 'Profile', 'pr',]:
            sqlPackageArguments[key] = str(Path(sqlPackageArguments[key]))


# Takes as input a dictionary of SqlPackage arguments and returns them as a single string
def getSqlPackageArguments(arguments):
    if platform.system() == 'Windows':
        convertSqlPackageFilePathsForWindows(arguments)
    args = []
    for arg in arguments:
        if type(arguments[arg]) is dict:
            for value in arguments[arg]:
                args.append('/{}:{}={}'.format(arg, value, arguments[arg][value]))
        else:
            args.append('/{}:{}'.format(arg, arguments[arg]))
    return args


def getSqlCmdArguments(arguments):
    args = []
    for arg in arguments:
        if arg == 'Action':
            continue
        args.append('-' + arg)
        args.append(arguments[arg])
    return args


def deploy(jsondata, force=False):
    sqlPackage = getSqlPackageExecutable()
    sqlcmd = getSqlCmdExecutable()
    for config in jsondata:
        if jsondata[config]['Action'].lower() == 'sqlcmd':
            process = [sqlcmd] + getSqlCmdArguments(jsondata[config])
        else:
            process = [sqlPackage] + getSqlPackageArguments(jsondata[config])
        print('\n\n--- : {}:\n\t{}\n\n'.format(config, process))
        execution = subprocess.run(process)
        if execution.returncode and not force:
            print('{} - deployment step failed!\nExiting...'.format(config))
            sys.exit()



if __name__ == '__main__':
    args = parseargs()
    deploy(json.load(args.configfile), args.force)