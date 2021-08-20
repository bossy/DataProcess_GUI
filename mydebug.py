from inspect import getframeinfo, stack

MYDEBUG = True


def dbg_print(message):
    if MYDEBUG:
        caller = getframeinfo(stack()[1][0])
        print("%s:%d - %s" % (caller.filename, caller.lineno, message))
