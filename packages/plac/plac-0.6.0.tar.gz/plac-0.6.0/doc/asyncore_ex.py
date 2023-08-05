import plac
from importer2 import Importer
from monocle.asyncore_stack.eventloop import evlp
#from monocle.twisted_stack.eventloop import evlp
#from monocle.tornado_stack.eventloop import evlp

if __name__ == '__main__':
    imp = plac.call(Importer)
    i = plac.Interpreter(imp, eventloop=evlp)
    i.interact()
