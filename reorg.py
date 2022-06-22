#!/usr/bin/env python3

import argparse
import os
import shutil
import sqlite3
from pathlib import Path
from sqlite3 import Error


""" DB code based on: https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/
"""

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def get_path_by_file_id(conn, file_id):
    """
    Query files by fileID
    :param conn: the Connection object
    :param file_id:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT relativePath FROM Files WHERE fileID=?", (file_id,))

    rows = cur.fetchall()

    for row in rows:
        return(list(row)[0])


def main():
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("dst_dir", type=Path)

    p = parser.parse_args()

    # construct path to Manifest.db
    database = os.getcwd() + r"/Manifest.db"

    # create a database connection
    conn = create_connection(database)

    # walk files in the backup and create a new tree of files mentioned in Manifest.db
    for root, dirs, files in os.walk("."):
        for file in files:
            if len(file) == 40:
                 src_file = os.path.join(root, file)
                 dst_file = str(p.dst_dir) + '/' + get_path_by_file_id(conn, file)
                 if dst_file:
                     Path( os.path.dirname(dst_file) ).mkdir( parents=True, exist_ok=True )
                     shutil.copy2(src_file, dst_file)


if __name__ == '__main__':
    main()
