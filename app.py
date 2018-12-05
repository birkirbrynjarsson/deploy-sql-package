import os
import subprocess

import argparse

def parseargs():
    parser = argparse.ArgumentParser(
        prog='AGR Database Deployment',
        description='Database deployment script for AGR db development'
    )
    parser.add_argument('configfile', type=argparse.FileType('r'), help='config file for deployment with SqlPackage')
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


def deployDB(config):
    sqlPackage = getSqlPackage()        
    print(sqlPackage)
    subprocess.run(['ls', '-al'])
    # for line in config:
    #     print(line.strip())



if __name__ == '__main__':
    args = parseargs()
    deployDB(args.configfile.readlines())