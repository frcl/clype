import argparse

from clype.utils import parse_annotations


class _AbstractCli(object):

    def __init__(self, name):
        self.argparser = None
        self.argparser = argparse.ArgumentParser(name)

    def run(self):
        """Start the command line interface"""
        args = self.argparser.parse_args()

        self.main(**(args.__dict__)) # pylint: disable=no-member


class SimpleCli(_AbstractCli):
    """A simple command line interface generated from type annotations
    of a function."""

    def __init__(self, func):
        super(SimpleCli, self).__init__(func.__name__)
        self.main = func

        parse_annotations(func, self.argparser)


class SubcommandCli(_AbstractCli):
    """A command line interface with subcommands generated from type annotations
    of a set of functions."""

    def __init__(self, name):
        super(SubcommandCli, self).__init__(name)
        self.commands = {}
        self.subparsers = self.argparser.add_subparsers(title='commands',
                                                        metavar='command')

    def main(self, **args):
        cmd = args['func']
        del args['func']
        cmd(**args)

    def command(self, func):
        """Creade a subcommand in the command line interface from a function"""
        self.commands[func.__name__] = func
        subp = self.subparsers.add_parser(func.__name__,
                                          help=func.__doc__)
        subp.set_defaults(func=func)
        parse_annotations(func, subp)
        return func
