# sql-packages
Automated database deployment tool that runs 'SqlPackage' from 'Microsoft' based on a JSON configuration file

## Requirements

`sql-packages` requires an installation of [_SqlPackage_](https://docs.microsoft.com/en-us/sql/tools/sqlpackage-download?view=sql-server-2017)
from _Microsoft_

It should be accessible from a `PATH`-directory or installed at `%ProgramFiles%\Microsoft Sql Server\150\DAC\bin\SqlPackage.exe` on _Windows_.

## Installation

Download the latest build for your OS

## Usage

The executable requires a `.json` configuration file as input,
each root element of the JSON document runs a single execution of `sqlpackage`
with the arguments defined within.  
All the possible `sqlpackage` arguments can be found on [_Microsoft's_ website](https://docs.microsoft.com/en-us/sql/tools/sqlpackage?view=sql-server-2017)

Run the executable with your deployment configuration:

```bash
sqlpackages deploy-config.json
```

Example configuration file: `deply-config.json`

```json
{
    "Production": {
        "Action": "Publish",
        "SourceFile": "development/dev_prod/bin/Debug/dev_prod.dacpac",
        "TargetDatabaseName": "prod",
        "TargetServerName": "localhost",
        "TargetUser": "SA",
        "TargetPassword": "12345678!",
        "p": {
            "IncludeCompositeObjects": true,
            "CompareUsingTargetCollation": true,
            "CreateNewDatabase": true
        }
    },
    "Staging": {
        "Action": "Publish",
        "SourceFile": "development/dev_stg_nav/bin/Debug/dev_stg_nav.dacpac",
        "TargetDatabaseName": "stg_nav",
        "TargetServerName": "localhost",
        "TargetUser": "SA",
        "TargetPassword": "12345678!",
        "p": {
            "IncludeCompositeObjects": true,
            "CompareUsingTargetCollation": true,
            "CreateNewDatabase": true
        }
    }
}
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
