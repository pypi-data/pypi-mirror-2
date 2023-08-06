#
# Copyright (c) 2006-2011, Prometheus Research, LLC
# See `LICENSE` for license information, `AUTHORS` for the list of authors.
#


from htsql_pgsql.connect import ConnectPGSQL


class TimeoutConnectPGSQL(ConnectPGSQL):

    statement_timeout = 60

    def open_connection(self, with_autocommit=False):
        connection = super(TimeoutConnectPGSQL, self).open_connection(
                                    with_autocommit=with_autocommit)
        cursor = connection.cursor()
        cursor.execute("""
            SET SESSION STATEMENT_TIMEOUT TO %s
        """ % (self.statement_timeout*1000))
        return connection


