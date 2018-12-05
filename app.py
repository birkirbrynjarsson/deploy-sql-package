import json
import os
import subprocess

import argparse

def parseargs():
    parser = argparse.ArgumentParser(
        prog='AGR Database Deployment',
        description='Database deployment script for AGR db development'
    )
    parser.add_argument('configfile', type=argparse.FileType('r'), help='JSON deployment configuration file passed to SqlPackage')
    return parser.parse_args()


# Checks if SqlPackage is installed and returns its path
def getSqlPackage():
    programFiles = os.getenv('ProgramFiles')
    sqlpackage = '{}\\Microsoft SQL Server\\150\\DAC\\bin\\SqlPackage.exe'.format(programFiles)
    if not os.path.isfile(sqlpackage):
        print('SqlPackage.exe was not found at: {}'.format(sqlpackage))
        print('SqlPackage can be downloaded from Microsoft\'s website!')
        quit()
    return sqlpackage


# Takes as input a dictionary of SqlPackage arguments and returns them as a single string
def getSqlPackageArguments(arguments):
    args = []
    for arg in arguments:
        if isinstance(arguments[arg], dict):
            for value in arguments[arg]:
                args.append('/{}:{}={}'.format(arg, value, arguments[arg][value]))
        else:
            args.append('/{}:{}'.format(arg, arguments[arg]))
    return ' '.join(args)


def deployDB(configfile):
    sqlPackage = getSqlPackage()
    configurations = json.load(configfile)
    
    for config in configurations:
        args = getSqlPackageArguments(configurations[config])
        print(config)
        # subprocess.run([sqlPackage, args])



if __name__ == '__main__':
    args = parseargs()
    deployDB(args.configfile)