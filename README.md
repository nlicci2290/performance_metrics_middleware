# performance_metrics_middleware
Django Middleware for recording performance metrics per request/responses

## Prerequisites
1. Install the C extension module from GitHub:
https://github.com/nlicci2290/cryptohashpy

Installation instructions are contained in the README for cryptohashpy

## Installation
Use the setup.py script to install this module.

```bash
python setup.py install
```

There are three things you need to change in your django configuration:

add the new variable
```txt
MIDDLEWARE_PERFORMANCE_METRICS_FILE = "path_to_file\myfile.csv"
```
update the INSTALLED_APPS variable
```txt
INSTALLED_APPS = [ "performance_metrics_middleware", ... ]
```
update the MIDDLEWARE variable
```txt
MIDDLEWARE = [ "performance_metrics_middleware.PerformanceMetrics.PerformanceMetricsMiddleware", ... ]
```
In order to get the most accurate results, this should be the first middleware module installed.

## Sample projects
Here is a sample django project with this module setup in the settings.py file
https://github.com/nlicci2290/django-webapp

## Running the tests
The unit tests are run with pytest.

Navigate to the performance_metrics_middleware folder and run the UnitTests.py file
```bash
pytest UnitTests.py
```

## Supported environments
This module is supported in both python 2 and 3 on Linux and Windows. 
Module was tested on Windows 10 and CentOS 7.

## License
[MIT](https://choosealicense.com/licenses/mit/)
