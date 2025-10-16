class BusinessException(Exception):
    def __init__(self, message: str, **kwargs):
        self.message = message
        super().__init__(**kwargs)

    def __reduce__(self):
        return BusinessException, (self.message,)


class NotFound(Exception):
    def __init__(self, message: str, **kwargs):
        self.message = message
        super().__init__(**kwargs)


class OverdraftLimitExceededException(BusinessException):
    pass


class InsufficientFundsException(BusinessException):
    pass


class DepositLimitExceededException(BusinessException):
    pass


class InfrastructureException(Exception):
    def __init__(self, message: str, **kwargs):
        self.message = message
        super().__init__(**kwargs)
