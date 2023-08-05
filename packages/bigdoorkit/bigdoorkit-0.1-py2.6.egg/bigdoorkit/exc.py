class BigdoorError(Exception):
    """The base type of Bigdoor Exception"""

class MissingClient(BigdoorError):
    """Raised when there is no client available to service
    the request.
    """
