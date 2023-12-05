import supervisor

def get_time(f):
    def inner(*arg, **kwarg):
        s_time = supervisor.ticks_ms()
        res = f(*arg, **kwarg)
        e_time = supervisor.ticks_ms()
        print('timeuse: {}'.format(e_time - s_time))
        return res
    return inner
