class SonWorldException(Exception):
    """
    SonWorld base exception. Handled at the outermost level.
    All other exception types are subclasses of this exception type.
    """


class OperationalException(SonWorldException):
    """
    Requires manual intervention and will stop the bot.
    Most of the time, this is caused by an invalid Configuration.
    """


class TemporaryError(SonWorldException):
    """
    Temporary network or conection related error.
    This could happen when an exchange is congested, unavailable, or the user
    has networking problems. Usually resolves itself after a time.
    """
