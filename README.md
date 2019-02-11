[![Build Status](https://ci.centos.org/view/Devtools/job/devtools-fabric8-analytics-release-monitor-f8a-build-master/badge/icon)](https://ci.centos.org/view/Devtools/job/devtools-fabric8-analytics-release-monitor-f8a-build-master/)
# fabric8-analytics-release-monitor
Service for monitoring of latest updates to upstream packages

### Configuration
Release monitor is configurable by following environment variables.

NPM_URL - URL of the NPM registry (must contain the protocol, e.g. `https://`) 

PYPI_URL - URL of the PyPi registry (again starting with `https://`)
 
ENABLE_SCHEDULING - If enabled, notifications about new packages will be sent via selinon into the
ingestion pipeline. Takes either `true` or `yes`.
  
SLEEP_INTERVAL - Interval between fetching latest RSS feeds from registries (in minutes).

### Running

Run it either from the command line using the `run.py` file or using `docker` (`podman?` ;-) ).

### Architecture

The process is very simple. It periodically fetches RSS feeds from the upstream repositories and
only calculates a relative complement of the set of the old updates and new updates.

```
   start
     |
     V
{old} := fetch updates
     |
     |<------------------------|
     |                         |
     V                         |
  wait for the                 |
specified period               |
     |                         |
     V                         |
{new} := fetch updates         |
     |                         |
     V                         |
{updates} := {new} \ {old}     |
     |                         |
     V                         |
schedule({updates})            |
     |                         |
     V                         |
{old} = {new}                  |
     |_________________________|
   

```

---------------------------------

### Footnotes

#### Coding standards

- You can use scripts `run-linter.sh` and `check-docstyle.sh` to check if the code follows [PEP 8](https://www.python.org/dev/peps/pep-0008/) and [PEP 257](https://www.python.org/dev/peps/pep-0257/) coding standards. These scripts can be run w/o any arguments:

```
./run-linter.sh
./check-docstyle.sh
```

The first script checks the indentation, line lengths, variable names, white space around operators etc. The second
script checks all documentation strings - its presence and format. Please fix any warnings and errors reported by these
scripts.

#### Code complexity measurement

The scripts `measure-cyclomatic-complexity.sh` and `measure-maintainability-index.sh` are used to measure code complexity. These scripts can be run w/o any arguments:

```
./measure-cyclomatic-complexity.sh
./measure-maintainability-index.sh
```

The first script measures cyclomatic complexity of all Python sources found in the repository. Please see [this table](https://radon.readthedocs.io/en/latest/commandline.html#the-cc-command) for further explanation how to comprehend the results.

The second script measures maintainability index of all Python sources found in the repository. Please see [the following link](https://radon.readthedocs.io/en/latest/commandline.html#the-mi-command) with explanation of this measurement.

You can specify command line option `--fail-on-error` if you need to check and use the exit code in your workflow. In this case the script returns 0 when no failures has been found and non zero value instead.

#### Dead code detection

The script `detect-dead-code.sh` can be used to detect dead code in the repository. This script can be run w/o any arguments:

```
./detect-dead-code.sh
```

Please note that due to Python's dynamic nature, static code analyzers are likely to miss some dead code. Also, code that is only called implicitly may be reported as unused.

Because of this potential problems, only code detected with more than 90% of confidence is reported.

#### Common issues detection

The script `detect-common-errors.sh` can be used to detect common errors in the repository. This script can be run w/o any arguments:

```
./detect-common-errors.sh
```

Please note that only semantic problems are reported.

#### Check for scripts written in BASH

The script named `check-bashscripts.sh` can be used to check all BASH scripts (in fact: all files with the `.sh` extension) for various possible issues, incompatibilities, and caveats. This script can be run w/o any arguments:

```
./check-bashscripts.sh
```

Please see [the following link](https://github.com/koalaman/shellcheck) for further explanation, how the ShellCheck works and which issues can be detected.
