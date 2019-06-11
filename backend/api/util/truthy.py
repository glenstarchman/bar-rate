
def is_true(s):
    if type(s) == type(''):
        s = s.lower()
        if s in ('true', 't', '1'):
            return True
        else:
            return False
    else:
        return s
