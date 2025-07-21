# Unit Tester

[![Static Badge](https://img.shields.io/badge/Python-254F72?style=for-the-badge)](https://www.python.org/downloads/)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/Alex-Au1/CampusBookingWebApp/unit-tests.yml?style=for-the-badge&label=Unit%20Tests)](https://github.com/Alex-Au1/CampusBookingWebApp/actions/workflows/unit-tests.yml)

A unit tester to test the backend SQL queries of the app

<br>

## Requirements
- [Python 3.6 and up](https://www.python.org/downloads/)

<br>

## How to Run

Run the following command:

<br>

### Poetry
```bash
poetry run unit_test [command name]
```

<br>

For the different command names see the list below

## Commands
| Command | Description |
| --- | --- |
| produceOutputs | Produces the expected outputs for the tests
| runSuite | Compares the ran results with the expected results of the test
| printOutputs | Prints out the expected outputs for the tests

<br>

## Command Options

Most of the options/arguments are based off the options/arguments from Python's [unittest](https://docs.python.org/3/library/unittest.html) package

### Positional Arguments
| Argument Name | Description |
| --- | --- |
| command | The command to run the unit tester |
| tests | a list of any number of test modules, classes and test methods. |

<br>

### Options
| Options | Description |
| --- | --- |
| -h, --help | show this help message and exit |
| -v, --verbose | Verbose output |
| -q, --quiet | Quiet output |
| --locals | Show local variables in tracebacks |
| -f, --failfast | Stop on first fail or error |
| -c, --catch | Catch Ctrl-C and display results so far |
| -b, --buffer | Buffer stdout and stderr during tests |
| -k TESTNAMEPATTERNS | Only run tests which match the given substring |
| -e ENV, --env ENV | The environment mode to run the tester. <br> If this option is not specified, then will run the tester against the datasets of every environment mode <br> <br> The available environment modes are: <br> - toy <br> - dev <br> -prod |
| -u USERNAME, --username USERNAME | Override the username to the database |
| -p PASSWORD, --password PASSWORD | Override the password to the database |
| -ho HOST, --host HOST | Override the host to the database |
| -po PORT, --port PORT | Override the port to the database |

<br>

## Running a Specific Test Suite

Sometimes, you only want to verify whether a single module is working correctly. You can do this by running the following command:

```bash
poetry run unit_test [commandName] [TestSuiteName]
```

<br>

## Running a Specific Test

For easier debugging or to save time, you may only want to run a single test. You can do this by running the following command:

```bash
poetry run unit_test [commandName] [TestSuiteName].[TestName]
```
