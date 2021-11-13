import sys


class Service:
    def __init__(self, config):
        self.config = config

    def print_log(self, src, ltype, message):
        if ltype == 0:
            sys.stdout.write("\r"+"\033[1m\033[34m{}".format(src) + "\033[1m\033[31m {}".format("::") +
                             "\033[1m\033[33m {}".format("DEBUG") + "\033[1m\033[31m {}".format("::") +
                             "\033[1m\033[37m {}".format(message))
            sys.stdout.flush()
        elif ltype == 1:
            print("\033[1m\033[34m{}".format(src) + "\033[1m\033[31m {}".format("::") +
                  "\033[1m\033[35m {}".format("CRITICAL") + "\033[1m\033[31m {}".format("::") +
                  "\033[1m\033[37m {}".format(message))
        else:
            print("\033[1m\033[34m{}".format(src) + "\033[1m\033[31m {}".format("::") +
                  "\033[1m\033[37m {}".format("INFO") + "\033[1m\033[31m {}".format("::") +
                  "\033[1m\033[37m {}".format(message))
