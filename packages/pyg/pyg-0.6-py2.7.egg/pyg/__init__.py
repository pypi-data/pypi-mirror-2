__version__ = '0.6'


def main():
    import sys
    import urllib2

    try:
        ## If Python fails to import pyg we just add this directory to
        ## sys.path so we don't worry wheter Pyg is installed or not.
        import pyg
    except ImportError:
        sys.path.insert(0, '..')
    from pyg.parser.parser import init_parser, load_options
    from pyg.core import PygError, InstallationError, AlreadyInstalled
    from pyg.log import logger

    try:
        parser = init_parser(__version__)
        args = parser.parse_args()
        if args.verbose:
            logger.level = logger.VERBOSE
        if args.debug:
            logger.level = logger.DEBUG
        load_options()
        parser.dispatch()
    except (PygError, InstallationError, ValueError) as e:
        sys.exit(1)
    except AlreadyInstalled:
        sys.exit(0)
    except urllib2.HTTPError as e:
        sys.exit('HTTPError: {0}'.format(e.msg))
    except urllib2.URLError as e:
        sys.exit('urllib error: {0}'.format(e.reason))
    sys.exit(0)

if __name__ == '__main__':
    main()
