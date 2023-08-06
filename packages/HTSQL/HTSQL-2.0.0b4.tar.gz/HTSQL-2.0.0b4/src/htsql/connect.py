#
# Copyright (c) 2006-2010, Prometheus Research, LLC
# Authors: Clark C. Evans <cce@clarkevans.com>,
#          Kirill Simonov <xi@resolvent.net>
#


"""
:mod:`htsql.connect`
====================

This module declares the database connection adapter.
"""


from __future__ import with_statement
from .adapter import Adapter, Utility, adapts
from .domain import Domain


class DBError(Exception):
    """
    Raised when a database error occurred.

    `message` (a string)
        The error message.

    `dbapi_error` (an exception)
        The original DBAPI exception.
    """

    def __init__(self, message, dbapi_error):
        assert isinstance(message, str)
        assert isinstance(dbapi_error, Exception)

        self.message = message
        self.dbapi_error = dbapi_error

    def __str__(self):
        return self.message

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self)


class ErrorGuard(object):
    """
    Guards against DBAPI exception.

    This class converts DBAPI exceptions to :exc:`DBError`.  It is designed
    to be used in a ``with`` clause.

    Usage::

        connect = Connect()
        try:
            with ErrorGuard(connect):
                connection = connect.open_connection()
                cursor = connection.cursor()
                ...
        except DBError:
            ...

    `connect` (:class:`Connect`)
        An instance of the connection utility.
    """

    def __init__(self, connect):
        self.connect = connect

    def __enter__(self):
        # Enters the `with` clause.
        pass

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # Exits from the `with` clause.

        # If no exception occurred, we are done.
        if exc_type is None:
            return

        # Get an exception instance.  Depending on the form of
        # the `raise` command, `exc_value` could be either an
        # exception object or its argument.  If latter, we need
        # to create an exception instance.
        if isinstance(exc_value, Exception):
            exception = exc_value
        elif exc_value is None:
            exception = exc_type()
        elif isinstance(exc_value, tuple):
            exception = exc_type(*exc_value)
        else:
            exception = exc_type(exc_value)

        # Ask the connection adapter to convert the exception.
        error = self.connect.normalize_error(exception)

        # If we got a new exception, raise it.
        if error is not None:
            raise error


class ConnectionProxy(object):
    """
    Wraps a DBAPI connection object.

    The proxy supports common DBAPI methods by passing them to
    the connection object.  Any exceptions raised when the executing
    DBAPI methods are converted to :exc:`DBError`.

    `connection`
        A raw DBAPI connection object.

    `guard` (:class:`ErrorGuard`)
        A DBAPI exception guard.
    """

    def __init__(self, connection, guard):
        self.connection = connection
        self.guard = guard

    def cursor(self):
        """
        Returns a database cursor.

        This method actually produces a :class:`CursorProxy` instance.
        """
        with self.guard:
            cursor = self.connection.cursor()
            return CursorProxy(cursor, self.guard)

    def commit(self):
        """
        Commit the current transaction.
        """
        with self.guard:
            return self.connection.commit()

    def rollback(self):
        """
        Rollback the current transaction.
        """
        with self.guard:
            return self.connection.rollback()

    def close(self):
        """
        Close the connection.
        """
        with self.guard:
            return self.connection.close()


class CursorProxy(object):
    """
    Wraps a DBAPI cursor object.

    The proxy supports common DBAPI methods by passing them to
    the cursor object.  Any exceptions raised when the executing
    DBAPI methods are converted to :exc:`DBError`.

    `cursor`
        A raw DBAPI cursor object.

    `guard` (:class:`ErrorGuard`)
        A DBAPI exception guard.
    """

    def __init__(self, cursor, guard):
        self.cursor = cursor
        self.guard = guard

    @property
    def description(self):
        """
        The format of the result rows.
        """
        return self.cursor.description

    @property
    def rowcount(self):
        """
        The number of rows produced or affected by the last statement.
        """
        return self.cursor.rowcount

    def execute(self, statement, *parameters):
        """
        Execute one SQL statement.
        """
        with self.guard:
            return self.cursor.execute(statement, *parameters)

    def executemany(self, statement, *parameters):
        """
        Execute an SQL statement against all parameters.
        """
        with self.guard:
            return self.cursor.executemany(statement, *parameters)

    def fetchone(self):
        """
        Fetch the next row of the result.
        """
        with self.guard:
            return self.cursor.fetchone()

    def fetchmany(self, *size):
        """
        Fetch the next set of rows of the result.
        """
        with self.guard:
            return self.cursor.fetchmany(*size)

    def fetchall(self):
        """
        Fetch all remaining rows of the result.
        """
        with self.guard:
            return self.cursor.fetchall()

    def __iter__(self):
        """
        Iterates over the rows of the result.
        """
        with self.guard:
            for row in self.cursor:
                yield row

    def close(self):
        """
        Close the cursor.
        """
        with self.guard:
            return self.cursor.close()


class Connect(Utility):
    """
    Declares the connection interface.

    The connection interface is a utility to open database connections.

    Usage::

        connect = Connect()
        try:
            connection = connect()
            cursor = connection.cursor()
            cursor.execute(...)
            cursor.fetchall()
            ...
        except DBError:
            ...
    """

    def __call__(self, with_autocommit=False):
        """
        Returns a connection object.

        The connection object is an instance of :class:`ConnectionProxy`
        and supports common DBAPI methods.

        If the database parameters for the application are invalid,
        the method may raise :exc:`DBError`.

        `with_autocommit` (Boolean)
            If set, the connection is opened in the autocommit mode.
        """
        # Create a guard for DBAPI exceptions.
        guard = ErrorGuard(self)
        # Open a raw connection while intercepting DBAPI exceptions.
        with guard:
            connection = self.open_connection(with_autocommit)
        # Return a proxy object.
        proxy = ConnectionProxy(connection, guard)
        return proxy

    def open_connection(self, with_autocommit=False):
        """
        Returns a raw DBAPI connection object.

        `with_autocommit` (Boolean)
            If set, the connection is opened in the autocommit mode.
        """
        # Override when subclassing.
        raise NotImplementedError()

    def normalize_error(self, exception):
        """
        Normalizes a DBAPI exception.

        When `exception` is a DBAPI exception, returns an instance of
        :exc:`DBError`; otherwise, returns ``None``.

        `exception`
            An exception object.
        """
        # The default implementation.
        return None


class Normalize(Adapter):

    adapts(Domain)

    def __init__(self, domain):
        self.domain = domain

    def __call__(self, value):
        return value


