

class BarRateValidationException(Exception):
    def __init__(self, errors):
        self.errors = errors

    def __str__(self):
        return "ValidationException: %s" % (str(self.errors))
