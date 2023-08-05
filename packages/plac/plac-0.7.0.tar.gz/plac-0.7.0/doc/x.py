from sql_interface import SqlInterface

if __name__ == '__main__':
    import plac; plac.Interpreter.call(SqlInterface)
