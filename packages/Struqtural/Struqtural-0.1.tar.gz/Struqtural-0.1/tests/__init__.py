import sys
import nose


if __name__ == '__main__':
    args = sys.argv + ["-s", "-d"]
    nose.run(argv=args)