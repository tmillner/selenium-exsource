#!/usr/bin/python
#  If running this in virtualenv use the python in it's dir e.g.
#  python run.py
import sys
from test.tests.classes import Run


if __name__ == '__main__':
    def get_optionarg(opt):
        try:
            arg = None
            for i in range(len(sys.argv)):
                if opt == sys.argv[i]:
                    arg = sys.argv[i+1]
                    break
            return arg
        except IndexError as err:
            exit(str.format("Specify an arg after option.\n{}", err.message))

    env = get_optionarg("-e")
    groups = get_optionarg("-g")
    tests = get_optionarg("-t")
    helpme = next((arg for arg in sys.argv if arg == "-h"), None)

    if helpme is not None:
        print Run().help()
        exit()

    if groups is not None and tests is not None:
        exit("Sorry, I don't do magic. Specify either a test or group only.")

    if env is not None:
        Run().setEnv(env)

    if groups is None and tests is None:
        print Run().run()
    elif groups is not None:
        print Run().groups(groups)
    elif tests is not None:
        print Run().tests(tests)
    else:
        tests = Run().get_testmatches(tests=tests, groups=groups)
        print Run().run(tests)
