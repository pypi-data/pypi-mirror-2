# ishelve2.py
import shelve, os, sys, plac

class ShelveInterface(object):
    "A minimal interface over a shelve object"
    commands = 'set', 'show', 'showall', 'delete'
    @plac.annotations(
        configfile=('path name of the shelve', 'option'))
    def __init__(self, configfile='~/conf.shelve'):
        self.fname = os.path.expanduser(configfile)
        self.intro = 'Operating on %s. Available commands:\n%s' % (
            self.fname, '\n'.join(c for c in self.commands))
    def __enter__(self):
        self.sh = shelve.open(self.fname)
        return self
    def set(self, name, value):
        "set name value"
        yield 'setting %s=%s' % (name, value)
        self.sh[name] = value
    def show(self, *names):
        "show given parameters"
        for name in names:
            yield '%s = %s' % (name, self.sh[name]) # no error checking
    def showall(self):
        "show all parameters"
        for name in self.sh:
            yield '%s = %s' % (name, self.sh[name])
    def delete(self, name=None):
        "delete given parameter (or everything)"
        if name is None:
            yield 'deleting everything'
            self.sh.clear()
        else:
            yield 'deleting %s' % name
            del self.sh[name] # no error checking
    def __exit__(self, etype, exc, tb):
        self.sh.close()

main = ShelveInterface # the main 'function' can also be a class!

if __name__ == '__main__':
    i = plac.Interpreter(main())
    i.interact()
