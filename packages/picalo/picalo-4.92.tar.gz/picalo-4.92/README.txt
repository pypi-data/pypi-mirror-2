

                          Picalo
                          
                  Data Analysis Library
                  
                  http://www.picalo.org/

Picalo is a Python library to help anyone who works with data files, 
especially those who work with data in relational/spreadsheet format.  
It is primarily created for investigators and auditors search through 
data sets for anomalies, trends, ond other information, but it is 
generally useful for any type of data or text files.

Picalo is different from NumPy/Numarray in that it is meant for
heterogeneous data rather than homogenous data.  In NumPy, you
have an array (table) of the same type--all ints, for example.
In Picalo, you have a table made up of different column types,
very similar to a database.

One of Picalo's primary purposes is making relational
databases easier to work with.  Once you have a Picalo table, 
you can add, move, or delete columns; work with records (horizontal
slices of the data); select and group records in various ways;
and run analyses on tables.  Picalo includes adapters for popular
databases, and it provides a Query object that make queries seem
just like regular Tables (except they are live from the database).

If you work with relational databases, delimited (CSV/TSV) files, 
EBCDIC files, MS Excel files, log files, text files, or other 
heterogeneous datasets, Picalo might make your life easier.

Picalo is programmed to be as Pythonic as possible.  It's core objects--
tables, columns, records--they act like lists.  A column is a list of cells.
A record is a list of cells.  A table is a list of records.  Tables can be 
sorted via the sort function, just like the Sorting HowTo shows.  The return
values of almost all functions are new tables, so functions can be chained
together like pipes in Unix.

Picalo includes an optional Project object that stores tables in
Zope Object DB files.  When Projects are used, Picalo automatically
swaps records in and out of memory as needed to ensure efficient use of 
resources.  Projects allow Picalo to work with essentially an unlimited
amount of data.

The project was started in 2003 by Conan C. Albrecht, a professor
in Information Systems at Brigham Young University.  Conan remains
the primary developer of Picalo.

Here's an example of Picalo code loading a CSV and working with it:

    # import the picalo libraries and turn off visual progress bars
    import picalo, StringIO
    picalo.use_progress_indicators(False)

    # load the csv, could have been from a filename
    csv = '''Name,Age
    Homer,35
    Marge,34
    Lisa,8
    Bart,10
    '''
    table = picalo.load_csv(StringIO.StringIO(csv))

    table.set_type('Age', int)  # set the type of the Age column (csv defaults types to str)
    table.view()                # prints a formatted table
    print table[0].Age          # prints 35
    print table[0]['Age']       # also prints 35
    print table[0][1]           # again prints 35
    print table[-1].Name        # prints Bart
    table2 = table[0:2]         # get a slice of records
    for name in table.column('Name'):
      print name                # prints the names, one by one

    # insert a column, which defaults cells to None
    table.insert_column(1, 'DoubleAge', int)
    # change cells using an expression
    table.replace_column_values('DoubleAge', 'record.Age * 2')

    # sort by Name, then Age
    picalo.Simple.sort(table, True, 'Name', 'Age')
    # sort in more Pythonic way (only by Name this time)
    table.sort(key=lambda r: r.Name)

    # print the std. dev. of the age column
    print picalo.stdev(table.column('Age'))

    # select records by regex, those containing 'a'
    table2 = picalo.Simple.select_by_regex(table, Name='^.*a.*$')

    # filter the existing table, then clear the filter
    table.filter('record.Age > 20')
    print len(table)            # prints 2
    table.clear_filter()
    print len(table)            # prints 4

    # reorder the columns 
    table.reorder_columns(['Age', 'Name', 'DoubleAge'])

    # add a live, calculated column
    table.append_calculated('ReverseName', unicode, 'record.Name[::-1].capitalize()')
    print table[0][3]           # prints 'Trab'
    table[0].Name = 'Maggie'
    print table[0][3]           # prints 'Eiggam'

    # split into multiple tables by value
    table.append_column('FavNum', int, [ 5, 5, 2, 2 ])
    tablelist = picalo.Grouping.stratify_by_value(table, 'FavNum')
    tablelist[0].view()         # view first table in list (has two records)
    tablelist[1].view()         # view second table in list (has two records)
    # any operations to a list of tables is made to all tabels in list
    # this sets the type of the FavNum column in *both* tables
    tablelist.set_type('FavNum', float)
  

Picalo is released in two formats:
  1) As a pure-Python library that is used by issuing one of the
     following:
        from picalo import *
        # or #
        import picalo
     Python programmers will be primarily interested in the library
     version.
     
     This format is installed in the typical Python fashion, either
     as an .egg via setuptools, or via "python setup.py install" from
     the source.
        
  2) As a standalone, wx-Python-based GUI environment that allow
     end users to access the Picalo libraries.
     
     This version is packaged as a Windows setup.exe file, Mac
     application bundle, and Linux rpm and deb files.  The user
     may not realize Python is even being used when running the
     full application environment.

Please see the following:
  - HOW TO RUN at the bottom of this file for running the source
    distribution or compiling a new bundle.
  
  - CHANGELOG.TXT has good information about what's changed in recent
    versions.

  - LICENSE.TXT for the GNU Public License that Picalo is released under.
    For those who don't want to read the license, here's the higlights:
    
      1. You may use Picalo free of charge.  I hope it is helpful to you.
         Please improve the code and share back with the community.
      
      2. Picalo has NO warrantee.  I don't guarantee it will do anything
         correctly or even incorrectly.  It may do unsightly things to your
         machine.  It may munch your data or even corrupt your hard drive.
         Picalo might fry your computer or ruin your marriage.  You take 
         all risks upon yourself.
   
      3. You must release any additions to Picalo under the GPL.
         
      4. Picalo source code cannot be included or used in any products that 
         are licensed with something other than the GPL.
         
      5. More information on these issues can be found in LICENSES.TXT
    
      
  - doc/PicaloCookbook.pdf has some of the best information right now.
        
      
  - doc/Manual.pdf for installation instructions (see the Installation section)
  
  
  - doc/Manual.pdf for detailed usage instructions, tutorial, etc.
  
Enjoy!  Please report any bugs to me.  I also welcome additions to the toolkit.
  
Dr. Conan C. Albrecht
conan@warp.byu.edu


=======================================
     HOW TO RUN/COMPILE THE SOURCE
=======================================

###   TO INSTALL THE PICALO LIBRARY ONLY:

If you want to install the library version for use in your Python environment and 
you have setuptools installed, you can simply use easy_install:

  easy_install picalo
  
If you don't have setuptools or want to install manually, expand the 
picalo-x.xx.tar.gz file and run the traditional Python setup.py file:

  (first install ZODB from the Zope libraries)
  (this assumes you downloaded picalo-5.12.tar.gz)
  tar xvfz picalo-5.12.tar.gz
  cd picalo-5.12
  python setup.py install
  


###   TO BUILD THE FULL GUI APPLICATION:

Note that this section is primarily for developers.  If you simply want to
install and run Picalo, visit http://www.picalo.org/ and download a pre-built
bundle for Windows, Mac, or Linux.

Picalo has several dependencies that you'll need to ensure your Python 
installation has.  These include the following:

NOTE: Don't install eggs on Windows because py2exe chokes on them.  When doing a 
      manual setup, use "python setup.py install_lib" to disable the egg building.
      This only applies to people wanting to compile the Windows exe files.
NOTE: To build on Mac, you need to be using the Framework version of Python.  This
      is the version on python.org, not the one that comes with an Apple.  Be sure
      to explicitly install Python and ensure it is being used.

REQUIRED:
  - Python 2.5+ (http://www.python.org) - It probably runs on version 2.4 and earlier, 
    but all testing is now being done on Python 2.5+. 
    We have not made the jump to Python 3 because some libraries aren't there yet
    (especially wxPython).
  - wxPython (http://www.wxpython.org) - We're on version 2.8.x.x right now.  
    We try to keep current with wxPython, so try the most recent version of wxPython.  
    If you hit GUI snags, email Conan and ask what version we're currently on. wxPython
    often changes the API from one version to another, so you'll know right away if
    it says some wx method doesn't exist.  Note that for the command-line version of
    Picalo, wxPython is not required -- the code can run entirely without any dependencies
    here.
  - ZODB - Zope Object Database
  - pyODBC (http://pyodbc.sourceforge.net/) - This allows you to access ODBC databases. 
    Picalo should be able to run without it, although the database GUI dialogs will fail.
  - pysycopg2 - This allows you to access PostgreSQL directly.   
    The Windows build is at Stickpeople.com.
    Picalo should be able to run without it, although the database GUI dialogs will fail.
  - pygresql - An alternative driver to access PostgreSQL directly.
    Picalo should be able to run without it, although the database GUI dialogs will fail.
  - MySQLdb - This allows you to access MySQL directly.
    Picalo should be able to run without it, although the database GUI dialogs will fail.
  - cx_Oracle - Allows you to connect to Oracle 10.
    Picalo should be able to run without it, although the database GUI dialogs will fail.
  - MX Base distribution - I'm not sure if this is still required or not.  Picalo itself
    doesn't use it, but some of the dependencies above might.
  - chardet.universaldetector (http://chardet.feedparser.org/) 
  - Windows Only: py2exe - if you want to compile Picalo on Windows
  - Windows Only: InnoSetup - if you want to compile Picalo on Windows
  - Mac OS X Only: py2app - if you want to compile Picalo on Mac OS X (installs easily 
    with easy_install).
  
Once you are sure the above are running, change to the trunk/ directory.  Run the following:

python Picalo.pyw

Alternatively, to run the command line version, execute the following from within the
Python interpreter:

>>> from picalo import *
  