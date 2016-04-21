[![Coverage Status](https://coveralls.io/repos/github/tmillner/selenium-exsource/badge.svg?branch=master)](https://coveralls.io/github/tmillner/selenium-exsource?branch=master)

Selenium + Python boilerplate framework for running tests by providing external (JSON) files as the input/data source. 

It decouples tests from particular environments.

##Install
With [tox](https://tox.readthedocs.org/en/latest/) installed run `tox` in the parent directory. If you don't have tox (which is very useful), run `pip install -r requirements.txt`

After installation you can run tests via the `run.py` command 

##Recommendations
- Create tests in `test/tests` sub-directories.
- Extend the base-class Framework for your test class. The runner peeks in files ending with Test.py, so be sure to name the file accordingly.
- Create the corresponding Json file using the same name of the test file. The json should contain the `contexts` key with an array of environments. Each environment contains it's key & value of data, e.g.
```JSON
{
  "contexts": [
    {"STAGING" : {
        "loginUser": "super@man.com"
      }
    },
    {"PROD" : {
        "loginUser": "super@woman.com"
      }
    }
  ]
}
```
- Script the test to utilize the context data (context map) via `self.contextmap.get("loginUser")`.
- Add groups if necessary to the test class. Use the `GROUPS` list attribute in the test class.
- Run the test(s) via the runner:
```bash
$ chmod +x run.py
$ ./run.py -e STAGING -t "MyTest,MyOtherTest" # example to run 2 tests in staging
$ ./run.py -e PROD -g "smoke" # example to run 1 smoke test in prod
$ ./run.py -e STAGING # example to run all tests in staging
```


##Quick Notes
- The framework supports running tests (TestCase) that don't extend the Framework class. 
- Default logging logs to project root `test.log` file with Debug or greater levels.
- The framework works best when enviornments are using different domains (rather than page names).
- When running tests from the command line, be sure to add the -e option. Python sets the environment for each execution/task only (not globablly)