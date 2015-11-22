# Assorted functions that are needed frequently.

import my_cnf
import mysql.connector
import sys
import unicodecsv as csv

def connect_as_db_user():
    """
    Open a connection as the database user.
    """

    db_option_group = "client%s" % my_cnf.database
    try:
        cnx = mysql.connector.connect(option_files="my.cnf",
                                      option_groups=db_option_group,
                                      database=my_cnf.database,
                                      raise_on_warnings=False,
                                      get_warnings=True)
        cursor = cnx.cursor()
    except mysql.connector.Error as err:
        print "Connect to MySQL server as db user failed:\n%s" % err
        sys.exit(1)
    return (cnx, cursor)

def is_table_empty(cnx, cursor, table):
    """
    Return True if the given table is empty.
    Use this to check if a table has been populated, to avoid re-running
    the query that populated it.
    """

    cmd = "SELECT COUNT(*) FROM %s;" % table
    count = 0
    try:
        cursor.execute(cmd)
        count = cursor.fetchone()[0]
    except mysql.connector.Error as err:
        print "Select count(*) failed:\n%s" % err
        sys.exit(1)
    return count == 0


def do_modify(cnx, cursor, cmd):
    """
    Execute a command that alters the schema or data, and thus requires
    a commit.
    """
    
    try:
        cursor.execute(cmd)
        exec_warnings = cursor.fetchwarnings()
        cnx.commit()
        commit_warnings = cursor.fetchwarnings()
    except mysql.connector.Error as err:
        print "Query failed:\n%s\n%s" % (cmd, err)
        cnx.close()
        sys.exit(1)
    # The warnings do not seem to be returned, even in cases when warnings
    # are known to occur.
    return (exec_warnings, commit_warnings)

def do_select(cnx, cursor, cmd, csv_file=None, csv_headers=None):
    """
    Execute a select query, i.e. something that returns results.
    Read the results.  Optionally write them to a csv file.
    """

    try:
        cursor.execute(cmd)
        # A commit is not allowed when the cursor has data.
    except mysql.connector.Error as err:
        print "Query failed:\n%s\n%s" % (cmd, err)
        cnx.close()
        sys.exit(1)

    rows = cursor.fetchall()

    if csv_file:
        # Write them out.
        with open(csv_file, "wb") as csv_handle:
            writer = csv.writer(csv_handle, delimiter=";")
            writer.writerow(csv_headers)
            writer.writerows(rows)

    return rows

def do_cmd(cnx, cursor, cmd, commit=False):
    """
    Execute a query that does not return results, and optionally do a commit.
    Queries that do not need a commit include state setting queries that take
    immediate effect, or a direct dump to a file.  Queries that do require a
    commit include inserts.  A commit is not allowed after a select query that
    returns results.
    """

    try:
        cursor.execute(cmd)
        if commit:
            cnx.commit()
    except mysql.connector.Error as err:
        print "Query failed:\n%s\n%s" % (cmd, err)
        cnx.close()
        sys.exit(1)

def populate_table(cnx, cursor, table, cmd, verbose=False):
    """
    Execute a command that will populate a table, if that table is empty.
    This allows re-running a script that may have had an error part-way
    through, without worry that an insert into a table will be repeated.
    """

    # First check if this table is populated.
    if not is_table_empty(table):
        if verbose:
            print "Table %s already contains data." % table
        return

    # Here, it's safe to add data.
    do_modify(cnx, cursor, cmd)