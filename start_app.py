import os

if __name__ == '__main__':
    from parser.settings import HOST, PORT
    os.system(
        command='uvicorn parser.web:app --host %s --port %s' % (HOST, PORT)
    )
