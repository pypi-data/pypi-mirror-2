import os
import sys


def python23_compat_main():
    try:
        from setuptools import setup
    except ImportError:
        from distutils.core import setup

    from firepython._setup_common import SETUP_ARGS
    setup(**SETUP_ARGS)

    return 0


def paver_main():
    if os.path.exists("paver-minilib.zip"):
        sys.path.insert(0, "paver-minilib.zip")

    import paver.tasks
    return paver.tasks.main()


def main():
    try:
        import paver
        return paver_main()
    except ImportError:
        return python23_compat_main()

if __name__ == '__main__':
    sys.exit(main())
