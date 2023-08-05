import plac

class Cmds(object):
    commands = 'checkout', 'commit', 'status', 'help'

    @plac.annotations(
        name=('a recognized command', 'positional', None, str, commands))
    def help(self, name):
        self.p.subp[name].print_help()

    def checkout(self, url):
        print('checkout', url)

    def commit(self):
        print('commit')

    @plac.annotations(quiet=('summary information', 'flag'))
    def status(self, quiet):
        print('status', quiet)

if __name__ == '__main__':
    plac.call(Cmds(), add_help=False)
