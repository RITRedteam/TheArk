#
# Author: Micah Martin (knif3)
#
# database.py
# 
# Wrap the sqlite database to allow for easy queries and manipulation.
# Simply open the DB and pass it a script to ensure that it will always be created even if
# the DB does not yet exist.
#
# USAGE:
#
# with Database("mydatabase.sqlite", "setup_db.sql") as db:
#     print(db.query("SELECT * FROM table;"))

import os
import sqlite3
import datetime

class Database(object):
    """
    Database handler object
    """
    def __init__(self, location, script=None):
        """
        A sqlite database wrapper. If you pass it a script file it will run that on creation
        Args:
            location (str): The file location of the database
            script (str, optional): The script to run if creating the database
        """
        self.location = location
        exists = os.path.exists(location)

        # if it doesn't exist, and we are not given a script, raise an error
        if not exists and not script:
            raise Exception("Database not found {}.".format(location))
        
        self.conn = sqlite3.connect(location, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.autocommit = True
        if not exists:
            self.execute_script(script)
            print("creating db with {}".format(script))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        """
        Close the connection
        """
        self.cur.close()
        self.conn.close()

    def commit(self):
        """Commit the DB"""
        self.conn.commit()
    
    def query(self, statement, values):
        """
        Handle a precomputed query
        Args:
            statement (string): the precomputed statement to execute
            values (tuple): the values to pass to the statement
        Returns:
            dict : the results of the query
        """
        self.cur.execute(statement, values)
        return self.newcur(self.cur)

    def _qry(self, qry):
        """
        Execute a raw, arbitrary query
        """
        self.cur.execute(qry)
        return self.cur.fetchall()

    def newcur(self, cursor):
        """
        Format the cursor output as json
        """
        output = []
        cols = [c[0] for c in cursor.description]
        for i in cursor.fetchall():
            d = {}
            for j in range(len(cols)):
                d[cols[j]] = i[j]
            output += [d]
        return output

    def execute_script(self, script):
        """
        Execute a script on the database, auto commit if autocommit is enabled
        """
        with open(script) as infile:
            script = infile.read()
        self.cur.executescript(script)
        if self.autocommit:
            self.conn.commit()
        return self.cur

    def get_tables(self):
        """Query information about the tables including column information

        Returns:
            dict: A dictionary with each table name and the column associated with it
        """
        qry = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT IN {}".format(
            '("information_types")'
        )
        self.cur.execute(qry)
        tables = {}
        for table in self.cur.fetchall():
            self.cur.execute("SELECT * FROM {} WHERE 1 = 2".format(table[0]))
            columns = [t[0] for t in self.cur.description]
            tables[table[0]] = columns
        return tables
    
    #### Custom Queries
    def is_ip_taken(self, ip):
        """Check whether or not an IP address is taken by another service

        Args:
            ip (str): The ip address to look for
        Returns:
            bool: Whether the ip is reserved already
        """
        qry = 'SELECT EXISTS(SELECT 1 FROM ips WHERE address = ?);'
        self.cur.execute(qry, (ip,))
        if self.cur.fetchone()[0] == 0:
            return False
        return True
    
    def is_haloname_taken(self, name):
        """Check if a halo name is already taken in the database
        
        TODO: Implement this function
        Args:
            name (str): The name of the halo
        Returns:
            bool: Whether or not the name is in use
        """
        qry = 'SELECT EXISTS(SELECT 1 FROM servers WHERE server_name = ?);'
        self.cur.execute(qry, (name,))
        if self.cur.fetchone()[0] == 0:
            return False
        return True
    
    def add_halo(self, _type, data):
        """Add the settings for a server to the database
        Args:
            _type (str): the type of server that is is, either 'default' or 'redirect'
            data (dict): The JSON data of the API
        Returns:
            bool: Whether or not the server was added
        """
        name = data.get('haloName')
        if _type == 'redirect':
            reserve_addresses = data.get("reserve", True)  # Default to true for redirect servers
        else:
            reserve_addresses = False
        # Add to the servers field
        qry = "INSERT INTO servers VALUES (?, ?, ?, ?)"
        self.cur.execute(qry, (name, _type, reserve_addresses, None))
        if _type == 'redirect':
            qry = "INSERT INTO server_redirects VALUES (?, ?, ?, ?)"
            self.cur.execute(qry, (name,
                             data.get("http", {}).get("server", None),   # server_http_url
                             data.get("http", {}).get("path", "/"),      # server_http_path
                             data.get("tcp", {}).get("server", None)     # server_tcp_url
                            ))
        
            # Add the ports if they are there
            values = [(name, port) for port in data.get("tcp", {}).get("ports", [])]
            qry = "INSERT INTO server_ports VALUES (?)"
            self.cur.executemany(qry, values)
        return True
    
    def add_addresses(self, name, addresses):
        """Insert the addresses into the DB for the server given
        Args:
            name (str): The server to add the IPs under
            addresses (str[]): The ip addresses to add
        Returns:
            bool: if the addresses were added
        """
        qry = "INSERT INTO ips VALUES (?, ?, ?)"
        values = [(name, addr, None) for addr in addresses]
        self.cur.executemany(qry, values)
        return True
    
    def get_addresses(self, name):
        """Return COUNT number of addresses for the server
        Args:
            name (str): the name of the halo
        Returns:
            list[str]: A list of all the ips assigned to the server
        """
        qry = "SELECT address FROM ips WHERE server_name = ?"
        self.cur.execute(qry, (name,))
        return [a[0] for a in self.cur.fetchall() if a]