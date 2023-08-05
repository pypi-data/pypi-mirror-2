# This file is part of the egoboost package which is release under the MIT
# License. You can find the full text of the license in the LICENSE file.
# Copyright (C) 2010 Sebastian Rahlf <basti at redtoad dot de>

"""
Storage for download stats.
"""

import csv
import datetime
import re
import simplejson
import StringIO
import sqlite3
import time


class DB (object):

    """
    Database wrapper object for storing/retrieving data from a SQLite db.
    """

    def __init__(self, path, create_table=True):
        self.conn = sqlite3.connect(path, 
            detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self.path = path

        # create table if it does not exist already
        if create_table:
            cur = self.conn.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS downloads (
                date DATE,
                package TEXT,
                version TEXT,
                filename TEXT,
                downloads INTEGER, 
                source TEXT,
                CONSTRAINT unique_row UNIQUE (date, package, version, filename, 
                    downloads, source) ON CONFLICT IGNORE
            )''')
            self.conn.commit()

    def __del__(self):
        # close DB connection on garbage collection
        self.conn.close()

    def __repr__(self):
        return '<ego-boost DB at %s>' % self.path

    def __iter__(self):
        # collect downloads for per package per date
        cur = self.conn.cursor()
        cur.execute("SELECT date, source, package, version, filename, "
                    "downloads FROM downloads;")
        for row in cur.fetchall():
            yield row

    def add(self, package, data, source, date=None):
        """
        Adds download data for package. ``data`` is of format ::

            {
                '0.2.0': {
                    'python-amazon-product-api-0.2.0.tar.gz': 68,
                    'python-amazon-product-api-0.2.0.win32-py2.5.exe': 15,
                    'python-amazon-product-api-0.2.0.win32-py2.5.msi': 17,
                    'python-amazon-product-api-0.2.0.win32-py2.6.exe': 17,
                    'python-amazon-product-api-0.2.0.win32-py2.6.msi': 19},
                '0.2.1': {
                    'python-amazon-product-api-0.2.1.tar.gz': 130},
                '0.2.2': {
                    'python-amazon-product-api-0.2.2.tar.gz': 101,
                    'python-amazon-product-api-0.2.2.win32.exe': 29},
                '0.2.3': {'python-amazon-product-api-0.2.3.tar.gz': 90,
                    'python-amazon-product-api-0.2.3.win32-py2.5.exe': 7}
            }
        
        which is, incidentally, the very same format that comes out of the 
        ``get_*_downloads`` functions.
        """
        if date is None:
            date = datetime.date.today()

        def build_rows():
            "Prepares data for executemany()."
            for version, files in data.items():
                # ignore meta data
                if type(files) != dict:
                    continue
                for filename, count in files.items():
                    yield {
                        'date' : date, 
                        'version' : version, 
                        'package' : package, 
                        'version' : version, 
                        'filename' : filename, 
                        'downloads' : count, 
                        'source' : source
                    }
            
        cur = self.conn.cursor()
        cur.executemany('''INSERT INTO downloads (
            date, package, version, filename, downloads, source) VALUES (
            :date, :package, :version, :filename, :downloads, :source)''',
            build_rows())
        self.conn.commit()

    def date_range(self):
        """
        Returns first and last date for which data has been stored.
        """
        cur = self.conn.cursor()
        cur.execute('''SELECT MIN(date) as "first [date]", 
            MAX(date) as "last [date]" FROM downloads;''')
        return cur.fetchone()

    def count(self):
        """
        Returns total row count.
        """
        cur = self.conn.cursor()
        cur.execute('SELECT COUNT(*) FROM downloads;')
        return cur.fetchone()[0]

    def get_packages(self, ignore_versions=True):
        """
        Gets all packages.
        """
        cur = self.conn.cursor()
        if ignore_versions:
            cur.execute('SELECT DISTINCT package FROM downloads;')
        else:
            cur.execute('SELECT DISTINCT package || " " || version FROM downloads;')
        return [pkg[0] for pkg in cur.fetchall()]

    def tocsv(self, ignore_versions=True):
        """
        Returns download statistics as CSV data. Example::

            date,python-amazon-product-api,python-weewar
            2010-05-04,7834,0
            ...
            2010-05-13,7886,2792
            2010-05-14,7897,2792
        """
        first, last = self.date_range()

        # abort processing for no data
        if not (first or last):
            return ''

        span = (last - first).days
        current = first

        # write CSV headers
        buffer = StringIO.StringIO()
        writer = csv.writer(buffer)
        packages = self.get_packages(ignore_versions)
        writer.writerow(['date'] + packages)

        # collect downloads for per package per date
        cur = self.conn.cursor()
        while current <= last:
            if ignore_versions:
                sql = """SELECT date, package, SUM(downloads)
                FROM downloads 
                WHERE date = ? 
                GROUP BY date, package;
                """
            else:
                sql = """
                SELECT date, package || ' ' || version, SUM(downloads)
                FROM downloads 
                WHERE date = ? 
                GROUP BY date, package, version;
                """

            cur.execute(sql, (current, ))
            data = dict((pkg, count) for date, pkg, count in cur.fetchall())
            writer.writerow([current] + [data.get(pkg, 0) for pkg in packages])
            current += datetime.timedelta(days=+1)

        buffer.flush()
        return buffer.getvalue()


def read_json(fp):
    """
    Loads download data from JSON file. Newer versions store meta data as well::

        {u'0.2.3': {...}, 
        '_package': 'python-amazon-product-api', 
        '_source': 'pypi', 
        '_date': datetime.date(2010, 6, 10)}

    Older versions store this data in the file name itself (eg. 
    ``pypi-20100610-python-amazon-product-api.json``). A ``ValueError`` is 
    raised if this data cannot be extracted.
    """
    blocks = simplejson.load(fp)
    if type(blocks) == dict:
        blocks = [blocks]
    # Old versions have meta data in file name. If no meta data can be found
    # (ie. _source, _date, _package) try to extract it from the file name.
    for data in blocks:
        if not '_date' in data:
            filename = fp.name
            m = re.search('(?P<_source>\w+)-(?P<_date>\d{8})-'
                        '(?P<_package>[\w-]+)', filename)
            if not m:
                raise ValueError('No meta data found!')
            data.update(m.groupdict())
            data['_date'] = datetime.date(
                *time.strptime(data['_date'], '%Y%m%d')[:3])
    return data


if __name__ == '__main__':

    # load/create database
    db = DB('/tmp/test.db')
    first, last = db.date_range()
    print '%i rows from %s to %s.' % (db.count(), first, last)

    # show data
    print db.tocsv(False)

#    # fetch data and store in db
#    from utils import get_downloads
#    data = get_downloads('http://bitbucket.org/basti/python-amazon-product-api/')
#    db.add('python-amazon-product-api', data, 'bitbucket')

#    # import old data from JSON files
#    import os, os.path
#    for filename in os.listdir('data'):
#        print 'Loading %s...' % filename
#        try:
#            data = read_json(open(os.path.join('data', filename)))
#            db.add(data['_package'], data, data['_source'], data['_date'])
#        except ValueError, e:
#            print 'ERROR:', e

