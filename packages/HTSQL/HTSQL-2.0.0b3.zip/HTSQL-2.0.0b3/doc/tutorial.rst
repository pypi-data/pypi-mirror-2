=====================
Introduction to HTSQL
=====================

*A query language for the accidental programmer*

HTSQL makes accessing data as easy as browsing the web.  An HTSQL
processor translates web requests into relational database queries and
returns the results in a form ready for display or processing.
Information in a database can then be directly accessed from a browser,
a mobile application, statistics tool, or a rich Internet application.
Like any web resource, an HTSQL service can be secured via encryption
and standard authentication mechanisms -- either on your own private
intranet or publicly on the Internet.

HTSQL users are data experts.  They may be business users, but they can
also be technical users who value data transparency and direct access.
Business users can use HTSQL to quickly search the database and create
reports without the help of IT.  Programmers can use it as data access
layer for web applications.  HTSQL can be installed by DBAs to provide
easy, safe database access for power users.

HTSQL is a schema-driven URI-to-SQL translator that takes a request over
HTTP, converts it to a set of SQL queries, executes these queries in a
single transaction, and returns the results in a format (CSV, HTML,
JSON, etc.) requested by the user agent:: 

  /----------------\                   /------------------------\
  | USER AGENT     |                   |   HTSQL WEB SERVICE    |
  *----------------*  HTTP Request     *------------------------* 
  |                | >---------------> -.                       |
  | * Web Browsers |  URI, headers,    | \      .---> Generated |
  |   HTML, TEXT   |  post/put body    |  v    /      SQL Query |
  |                |                   |  HTSQL          |      |
  | * Applications |                   |  PROCESSOR      v      |
  |   JSON, XML    |  HTTP Response    | /   ^.       SECURED   |
  |                | <---------------< -.      \      DATABASE  |
  | * Spreadsheets |  status, header,  |     Query       .      |
  |   CSV, XML     |  csv/html/json    |     Results <---/      |
  |                |  result body      |                        |
  \----------------/                   \------------------------/  

The HTSQL query processor does heavy lifting for you.  Using
relationships between tables as permitted links, the HTSQL processor
translates graph-oriented web requests into corresponding relational
queries.  This translation can be especially involved for sophisticated
requests having projections and aggregates.  For complex cases, an
equivalent hand-written SQL query is tedious to write and non-obvious
without extensive training.  By doing graph to relational mapping on
your behalf, HTSQL permits your time to be spent exploring information
instead of debugging.

The HTSQL language is easy to use.  We've designed HTSQL to be broadly
usable by semi-technical domain experts, or what we call *accidental
programmers*.  We've field tested the toolset with business analysts,
medical researchers, statisticians, and web application developers. By
using a formalized directed graph as the underpinning of the query
algebra and by using a URI-inspired syntax over HTTP, we've obtained a
careful balance between clarity and functionality.

We hope you like it.


Getting Started
===============

The following examples show output from the HTSQL command-line system,
which is plain text.  HTSQL can output HTML, CSV, XML and many other
formats.  This makes it suitable not only for direct queries, but as a
data access layer for application development.

We'll use a fictional university that maintains a database for its
student enrollment system.  There are four tables that describe the
business units of the university and their relationship to the 
courses offered::

  +--------------------+              +---------------------+     
  | DEPARTMENT         |              | SCHOOL              |     
  +--------------------+              +---------------------+     
  | code            PK |--\       /--o| code             PK |----\
  | school          FK |>-|------/    | name          NN,UK |    |
  | name         NN,UK |  |    .      +---------------------+    |
  +--------------------+  |     .                              . |
                        . |  departments                      .  |
       a department    .  |  may belong                      .   |
       offers zero or .   |  to at most        a school          |
       more courses       |  one school        administers zero  |
                          |                    or more programs  |
  +--------------------+  |                                      |
  | COURSE             |  |           +---------------------+    |
  +--------------------+  |           | PROGRAM             |    |
  | department  FK,PK1 |>-/           +---------------------+    |
  | number         PK2 |              | school       PK1,FK |>---/
  | title           NN |              | code            PK2 |        
  | credits         NN |              | title            NN |        
  | description        |              | degree           CK |        
  +--------------------+              +---------------------+        

  PK - Primary Key   UK - Unique Key         FK - Foreign Key
  NN - Not Null      CK - Check Constraint   

The university consists of schools, which administer one or more
degree-granting programs.  Departments are associated with a school
and offer courses.  Further on in the tutorial we will introduce
other tables such as student, instructor and enrollment.

Selecting Data
--------------

HTSQL requests typically begin with a table name.  You can browse the
contents of a table, search for specific data, and select the columns
you want to see in the results.  

The most basic HTSQL request (A1_) returns everything from a table::

   /school 

.. _A1:  http://demo.htsql.org/school

The result set is a list of schools in the university, including all
columns, sorted by the primary key for the table::

    school                                            
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    code | name                     
    -----+--------------------------
    art  | School of Art and Design                   
    bus  | School of Business                
    edu  | College of Education                       
    egn  | School of Engineering
    ...                      

Not all columns are useful for every context.  Use a *selector* to
choose columns for display (A2_)::

    /program{school, code, title}

    program
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
    school | code     | title
    -------+----------+-----------------------------------
    art    | gart     | Post Baccalaureate in Art History
    art    | uhist    | Bachelor of Arts in Art History  
    art    | ustudio  | Bachelor of Arts in Studio Art   
    bus    | pacc     | Graduate Certificate in Accounting
    ...

.. _A2: http://demo.htsql.org/program{school,code,title}

Add a plus (``+``) sign to the column name to sort the column in
ascending order.  Use a minus sign (``-``) for descending order.  For
example, this request (A3_) returns departments in descending order::

    /department{name-, school}

    department                                        
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    name                   | school
    -----------------------+-------
    Wind                   | mus   
    Vocals                 | mus   
    Teacher Education      | edu   
    Studio Art             | art
    ...   

.. _A3: 
    http://demo.htsql.org/department{name-,school}

Using two ordering indicators will sort on labeled columns as they
appear in the selector.  In the example below, we sort in ascending
order on ``department`` and then descending on ``credits`` (A4_)::

    /course{department+, number, credits-, title}

    course                                            
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    department | number | credits | title                     
    -----------+--------+---------+---------------------------
    acc        | 315    | 5       | Financial Accounting      
    acc        | 200    | 3       | Principles of Accounting I
    acc        | 426    | 3       | Corporate Taxation        
    ...

.. _A4: 
    http://demo.htsql.org
    /course{department+, number, credits-, title}
 
To display friendlier names for the columns, use ``as`` to rename a
column's title (A5_)::

    /course{department as 'Dept Code'+, number as 'No.',
            credits-, title}

    course                                            
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Dept Code | No. | credits | title                      
    ----------+-----+---------+----------------------------
    acc       | 315 | 5       | Financial Accounting       
    acc       | 200 | 3       | Principles of Accounting I 
    acc       | 426 | 3       | Corporate Taxation         
    ...

.. _A5: 
    http://demo.htsql.org
    /course{department%20as%20'Dept%20Code'+,number%20as%20'No.',
            credits-, title}

Selectors let you choose, rearrange, and sort columns of interest.  They
are an easy way to exclude data that isn't meaningful to your report.   

Linking Data
------------

In our example schema, each ``program`` is administered by a ``school``.
Since the HTSQL processor knows about this relationship, it is possible
to link data accordingly (B1_)::

    /program{school.name, title}

    program                                           
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    school.name               | title                             
    --------------------------+-----------------------------------
    School of Art and Design  | Post Baccalaureate in Art History 
    School of Art and Design  | Bachelor of Arts in Art History   
    School of Art and Design  | Bachelor of Arts in Studio Art    
    School of Business        | Graduate Certificate in Accounting
    ...

.. _B1: 
    http://demo.htsql.org
    /program{school.name, title}

This request joins the ``program`` and ``school`` tables by the foreign
key from ``program{school}`` to ``school{code}``.  This is called a
*singular* relationship, since for every ``program``, there is exactly
one ``school``.  

It is possible to join through multiple foreign keys; since ``course``
is offered by a ``department`` which belongs to a ``school``, we can
list courses including school and department name (B2_)::

    /course{department.school.name, department.name, title}

    course                                           
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    department.school.name | department.name | title                    
    -----------------------+-----------------+---------------------------
    School of Business     | Accounting      | Practical Bookkeeping      
    School of Business     | Accounting      | Principles of Accounting I 
    School of Business     | Accounting      | Financial Accounting       
    School of Business     | Accounting      | Corporate Taxation         
    ...

.. _B2: 
    http://demo.htsql.org
    /course{department.school.name, department.name, title}

This request can be shortened a bit by collapsing the duplicate mention
of ``department``; the resulting request is equivalent (B3_)::

    /course{department{school.name, name}, title}

.. _B3: 
    http://demo.htsql.org
    /course{department{school.name, name}, title}

For cases where you don't wish to specify each column explicitly, use
the wildcard ``*`` selector.  The request below returns all columns from
``department`` and all columns from its correlated ``school`` (B4_)::

    /department{*,school.*}

    department                                       
    ~~~~~~~~~~~~~~~~~~~~ ... ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ...
    code   | name        ... | school.name                ...  
    -------+------------ ... +--------------------------- ...  
    acc    | Accounting  ... | School of Business         ...  
    arthis | Art History ... | School of Art and Design   ...  
    artstd | Studio Art  ... | School of Art and Design   ...  
    astro  | Astronomy   ... | School of Natural Sciences ...  
    ...

.. _B4: 
    http://demo.htsql.org
    /department{*,school.*}
    
Since the HTSQL processor knows about relationships between tables in
your relational database, joining tables in your reports is trivial.

Filtering Data
--------------

Predicate expressions in HTSQL follow the question mark ``?``.  
For example, to return departments in the 'School of Engineering'
we write (C1_)::
  
    /department?school='egn'

    department                            
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    code | name                   | school
    -----+------------------------+-------
    be   | Bioengineering         | egn   
    comp | Computer Science       | egn   
    ee   | Electrical Engineering | egn   
    me   | Mechanical Engineering | egn
    ...

.. _C1: 
    http://demo.htsql.org
    /department?school='egn'

The request above returns all rows in the ``department`` table where the
column ``school`` is equal to ``'eng'``.   In HTSQL, *literal* values are
single quoted, in this way we know ``'eng'`` isn't the name of a column.

Often times we want to compare a column against values from a list.  The
next example returns rows from the ``program`` table for the "Bachelors
of Arts" (``'ba'``) or "Bachelors of Science" (``'bs'``) degrees (C2_)::

    /program?degree={'ba','bs'}

    program                                                    
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    school | code     | title                             | degree
    -------+----------+-----------------------------------+-------
    art    | uhist    | Bachelor of Arts in Art History   | ba
    art    | ustudio  | Bachelor of Arts in Studio Art    | ba
    bus    | uacct    | Bachelor of Science in Accounting | bs
    ...

.. _C2: 
    http://demo.htsql.org
    /program?degree={'ba','bs'}

Complex filters can be created using boolean connectors, such as the
conjunction (``&``) and alternation (``|``) operators .  The following
request returns programs in the "School of Business" that do not
grant a "Bachelor of Science" degree (C3_)::

    /program?school='bus'&degree!='bs'

    program                                                    
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    school | code | title                              | degree
    -------+------+------------------------------------+-------
    bus    | mba  | Masters of Business Administration | mb    
    bus    | pacc | Graduate Certificate in Accounting | ct    
    bus    | pcap | Certificate in Capital Markets     | ct
    ...

.. _C3: 
    http://demo.htsql.org
    /program?school='bus'&degree!='bs'

Filters can be combined with selectors and links.  The following request
returns courses, listing only department number and title, having less
than 3 credits in the "School of Natural Science" (C4_)::

    /course{department, number, title}
      ?credits<3&department.school='ns'

    course                                              
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    department | number | title                         
    -----------+--------+-------------------------------
    phys       | 388    | Experimental Physics I        
    chem       | 115    | Organic Chemistry Laboratory I
    astro      | 142    | Solar System Lab              
    astro      | 155    | Telescope Workshop            
    ...

.. _C4: 
    http://demo.htsql.org
    /course{department, number, title}
       ?credits<3&department.school='ns'

It is sometimes desirable to specify the filter before the selector.
Using a *table expression*, denoted by parenthesis, the previous request
is equivalent to (C5_)::

    /(course?credits<3&department.school='ns')
      {department, number, title}

.. _C5: 
    http://demo.htsql.org
    /(course?credits<3&department.school='ns')
      {department, number, title}

HTSQL supports a whole suite of functions and predicator operators.
Further, through the plug-in mechanism, custom data types, operators,
and functions may be integrated to support domain specific needs.

Formatters
----------

Once data is selected, linked and filtered, it is formatted for the
response.  By default, HTSQL uses the ``Accept`` header to negotiate the
output format with the user agent.  This can be overridden with a format
command, such as ``/:json``.  For example, results in JSON format (RFC
4627) can be requested as follows (D1_)::

    /school/:json

    [
      ["code", "name"],
      ["art", "School of Art and Design"],
      ["bus", "School of Business"],
      ["edu", "College of Education"],
      ["egn", "School of Engineering"],
      ["la", "School of Arts, Letters, and the Humanities"],
      ["mart", "School of Modern Art"],
      ["mus", "Musical School"],
      ["ns", "School of Natural Sciences"],
      ["sc", "School of Continuing Studies"]
    ]

.. _D1: 
    http://demo.htsql.org
    /school/:json

Other formats include ``/:txt`` for plain-text formatting, ``/:html`` for
display in web browsers, and ``/:csv`` for data exchange. 

Putting it All Together
-----------------------

The following request selects records from the ``course`` table,
filtered by all departments in the 'School of Business', sorted by
``course`` ``title``, including ``department``'s ``code`` and ``name``,
and returned as a "Comma-Separated Values" (RFC 4180) (E1_)::

    /course{department{code,name},number,title+}?
      department.school='bus'/:csv

    department.code,department.name,number,title
    corpfi,Corporate Finance,234,Accounting Information Systems
    acc,Accounting,527,Advanced Accounting
    capmrk,Capital Markets,756,Capital Risk Management
    corpfi,Corporate Finance,601,Case Studies in Corporate Finance
    ... 

.. _E1: 
    http://demo.htsql.org
    /course{department{code,name},number,title+}?
          department.school='bus'/:csv
    
HTSQL requests are powerful without being complex.  They are easy to
read and modify.  They adapt to changes in the database.  These
qualities increase the usability of databases by all types of users and
reduce the likelihood of costly errors.


Relating and Aggregating Data
=============================

HTSQL distinguishes between *singular* and *plural* relationships to
simplify query construction.  By a *singular* relationship we mean for
every record in one table, there is at most one record in a linked
table; by *plural* we mean there is perhaps more than one correlated
record.  To select a *plural* expression in a result set, an *aggregate*
function, such as ``sum``, ``count``, or ``exists`` must be used.  In
this way, what would be many values is converted into a single data cell
and integrated into a coherent result set. 

By requiring aggregates for plural expressions, HTSQL reduces query
construction time and reduces errors.  When a query starts with a table,
rows returned are directly correlated to records in this table. Since
cross products or projections cannot be created accidentally, the
combined result set is always consistent and understandable. 

Basic Linking
-------------

One-to-many relationships are the primary building block of relational
structures.  In our schema, each ``course`` is offered by a
``department`` with a mandatory foreign key.  For each course, there is
exactly one corresponding department.  In this case, the relationship is
singular in one direction and plural in the other.

If each row in your result set represents a ``course``, it is easy to
get correlated information for each course's department (RA1_)::

    /course{department.name, title}

    course                                              
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    department.name        | title                      
    -----------------------+----------------------------
    Accounting             | Practical Bookkeeping      
    Accounting             | Principles of Accounting I 
    Accounting             | Financial Accounting       
    ...

.. _RA1:
    http://demo.htsql.org
    /course{department.name,title}

It's possible to join *up* a hierarchy in this way, but not down. If
each row in your result set is a ``department``, then it is an error to
request ``course``'s ``credits`` since there could be many courses in a
given department (RA2_)::

    /department{name, course.credits}
    
    400 Bad Request

    a singular expression is required at position 26:
    /department{name, course.credits}
                             ^------

.. _RA2:
    http://demo.htsql.org
    /department{name,course.credits}

In cases like this, an aggregate function, such as ``max`` is needed to
convert a plural expression into a singular value.  The following
example shows the maximum course credits by department (RA3_)::

    /department{name, max(course.credits)}

    department                          
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    name             | max(course.credits)
    -----------------+--------------------
    Accounting       |                   5
    Alumni & Parents |                   4
    Art History      |                   4
    ...

.. _RA3:
    http://demo.htsql.org
    /department{name,max(course.credits)}

Conversely, you cannot use aggregates with singular expressions.  For
example, since ``school`` is singular relative to ``department``, it is
an error to count them (RA4_)::

    /department{name, count(school)}
    
    400 Bad Request

    a plural expression is required at position 25:
    /department{name, count(school)}
                            ^-----

.. _RA4:
    http://demo.htsql.org
    /department{name, count(school)}

For single row or *scalar* expressions, an aggregate is always needed
when referencing a table.  For example, the query below returns maximum
number of course credits across all departments (RA5_)::

    /max(course.credits)

    max(course.credits)                                                    
    -------------------                                                    
                      8                                                    
                (1 row)    

.. _RA5:
    http://demo.htsql.org
    /max(course.credits)


Aggregate Expressions
---------------------

Since ``school`` table has a *plural* (one to many) relationship 
with ``program`` and ``department``, we can count them (RB1_)::

    /school{name, count(program), count(department)}

    school
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    name                     | count(program) | count(department)
    -------------------------+----------------+------------------
    School of Art and Design | 3              | 2                
    School of Business       | 5              | 3                
    College of Education     | 7              | 2                
    School of Engineering    | 8              | 4                
    ...

.. _RB1: 
    http://demo.htsql.org
    /school{name,count(program),count(department)}

Filters may be used within an aggregate expression.  For example, the 
following returns the number of courses, by department, that are at
the 400 level or above (RB2_)::

    /department{name, count(course?number>=400)}

    department
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    name           | count(course?number>=400)
    ---------------+--------------------------
    Accounting     |                         3
    Art History    |                         4
    Astronomy      |                         0
    Bioengineering |                         2
    ...

.. _RB2:
    http://demo.htsql.org
    /department{name, count(course?number>=400)}

It's possible to nest aggregate expressions.  This request returns the
average number of courses each department offers (RB3_)::

    /school{name, avg(department.count(course))}

    school                                                  
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    name                     | avg(department.count(course))
    -------------------------+------------------------------
    School of Art and Design |            6.5000000000000000
    School of Business       |            4.3333333333333333
    College of Education     |            5.0000000000000000
    School of Engineering    |            5.2500000000000000
    ...

.. _RB3:
    http://demo.htsql.org
    /school{name, avg(department.count(course))}

Filters and nested aggregates can be combined.  Here we count, for each
school, departments offering 4 or more credits (RB4_)::

    /school{name, count(department?exists(course?credits>3))}

    school                                                               
    ---------------------------------------------------------------------
    name                     | count(department?exists(course?credits>3))
    -------------------------+-------------------------------------------
    School of Art and Design |                                          2
    School of Business       |                                          1
    College of Education     |                                          1
    School of Engineering    |                                          4
    ...

.. _RB4:
    http://demo.htsql.org
    /school{name, count(department?exists(course?credits>3))}

Filtering can be done on one column, with aggregation on another.  This
example shows average credits from only high-level courses (RB5_)::

    /department{name, avg((course?number>400).credits)}

    department                                       
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    name           | avg((course?number>400).credits)
    ---------------+---------------------------------
    Accounting     |               3.0000000000000000
    Art History    |               3.2500000000000000
    Astronomy      |                                 
    Bioengineering |               5.5000000000000000

.. _RB5:
    http://demo.htsql.org
    /department{name, avg((course?number>400).credits)}

Numerical aggregates are supported.  This request computes some useful
``course.credit`` statistics (RB6_)::

    /department{code, min(course.credits), max(course.credits), 
                      avg(course.credits)}

    department                                                              
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    code   | min(course.credits) | max(course.credits) | avg(course.credits)
    -------+---------------------+---------------------+--------------------
    acc    |                   2 |                   5 |  3.1666666666666667
    arthis |                   3 |                   4 |  3.1666666666666667
    astro  |                   1 |                   3 |  2.2500000000000000
    be     |                   3 |                   8 |  4.2500000000000000
    ...

.. _RB6:
    http://demo.htsql.org
    /department{code, min(course.credits), max(course.credits), 
                      avg(course.credits)}

The ``every`` aggregate tests that a predicate is true for every row in
the correlated set.  This example returns ``department`` records that
either lack correlated ``course`` records or where every one of those
``course`` records have exactly ``3`` credits (RB7_)::

    /department{name, avg(course.credits), count(course)} 
      ?every(course.credits=3)

    department
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    name               | avg(course.credits) | count(course)
    -------------------+---------------------+--------------
    Bursar's Office    |                     |             0
    Capital Markets    |  3.0000000000000000 |             4
    Career Development |                     |             0
    Corporate Finance  |  3.0000000000000000 |             3
    ...

.. _RB7:
    http://demo.htsql.org
    /department{name, avg(course.credits), count(course)} 
      ?every(course.credits=3)


Logical Expressions
===================

A *filter* refines results by including or excluding data by specific
criteria.  This section reviews comparison operators, boolean
expressions, and ``NULL`` handling.

Comparison Operators
--------------------

The quality operator (``=``) is overloaded to support various types. 
For character strings, this depends upon the underlying database's
collation rules but typically is case-sensitive.  For example, to return
a ``course`` by ``title`` (PC1_)::

    /course?title='Drawing'

    course
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    department | number    | title   | credits 
    -----------+-----------+---------+---------
    stdart     | 333       | Drawing | 3         

.. _PC1:
    http://demo.htsql.org
    /course?title='Drawing'

If you're not sure of the exact course title, use the case-insensitive
*contains* operator (``~``).  The example below returns all ``course``
records that contain the substring ``'lab'`` (PC2_)::

    /course?title~'lab'

    course
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    department | number | title                          | credits
    -----------+--------+--------------------------------+--------
    astro      |    142 | Solar System Lab               |       2
    chem       |    115 | Organic Chemistry Laboratory I |       2
    chem       |    314 | Laboratory Chemistry           |       3
    comp       |    710 | Laboratory in Computer Science |       4
    ...

.. _PC2:
    http://demo.htsql.org
    /course?title~'lab'

Use the *not-contains* operator (``!~``) to exclude all courses with
physics in the title (PC3_)::

    /course?title!~'lab'

.. _PC3:
    http://demo.htsql.org
    /course?title!~'lab'

To exclude a specific class, use the *not-equals* operator (PC4_)::

    /course?title!='Organic Chemistry Laboratory I'

.. _PC4:
    http://demo.htsql.org
    /course?title!='Organic Chemistry Laboratory I'


The *equality* (``=``) and *inequality* (``!=``) operators are
straightforward when used with numbers (PC5_)::

    /course{department,number,title}?number=101 
 
    course                                                 
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    department | number | title                      
    -----------+--------+----------------------------
    eng        |    101 | Introduction to Composition
    mth        |    101 | College Algebra            
    ...

.. _PC5:
    http://demo.htsql.org
    /course{department,number,title}?number=101

The *in* operator (``={}``) can be thought of as equality over a set.
This example, we return courses that are in neither the "Art History"
nor the "Studio Art" department (PC6_)::

    /course?department!={'arthis','stdart'}

.. _PC6:
    http://demo.htsql.org
    /course?department!={'arthis','stdart'}

Use the *greater-than* (``>``) operator to request courses with more
than 3 credits (PC7_):: 

     /course?credits>3

     course
     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     department | number    | title                     | credits
     -----------+-----------+---------------------------+--------
     arthis     | 712       | Museum and Gallery Mgmt   | 4        
     stdart     | 411       | Underwater Basket Weaving | 4         
     .

.. _PC7:
    http://demo.htsql.org
    /course?credits>3

Use the *greater-than-or-equal-to* (``>=``) operator request courses
that have three credits or more (PC8_)::

    /course?credits>=3

.. _PC8:
    http://demo.htsql.org
    /course?credits>=3

Using comparison operators with strings tells HTSQL to compare them
alphabetically (once again, dependent upon database's collation).  For
example, the *greater-than* (``>``) operator can be used to request
departments whose ``code`` follows ``'me'`` in the alphabet (PC9_)::

    /department?code>'me'

    department                         
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    code  | name              | school
    ------+-------------------+-------
    mth   | Mathematics       | ns    
    phys  | Physics           | ns    
    pia   | Piano             | mus   
    poli  | Political Science | la    
    ...

.. _PC9:
    http://demo.htsql.org
    /department?code>'me'


Boolean Expressions
-------------------

HTSQL uses function notation for constants such as ``true()``, ``false()``
and ``null()``.  For the text formatter, a ``NULL`` is shown as a blank,
while the empty string is presented as a double-quoted pair (PA1_)::

    /{true(), false(), null(), ''}

                            
    true() | false() | null() | '' 
    -------+---------+--------+---
    true   | false   |        | ""

.. _PA1:
    http://demo.htsql.org
    /{true(), false(), null()}

The ``is_null()`` function returns ``true()`` if it's operand is
``null()``. In our schema, non-academic ``department`` records that have
a ``NULL`` ``school`` can be listed (PA2_)::

    /department{code, name}?is_null(school)

    department
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    code    | name              
    --------+-------------------
    bursar  | Bursar's Office   
    career  | Career Development
    parent  | Parents & Alumni  
                        (3 rows)

.. _PA2:
    http://demo.htsql.org
    /department{code, name}?is_null(school)

The *negation* operator (``!``) is ``true()`` when it's operand is
``false()``.   To skip non-academic ``department`` records (PA3_)::

    /department{code, name}?!is_null(school)

    department
    ~~~~~~~~~~~~~~~~~~~~~~~
    code   | name          
    -------+---------------
    acc    | Accounting          
    arthis | Art History         
    astro  | Astronomy           
    be     | Bioengineering      
    ...

.. _PA3:
    http://demo.htsql.org
    /department{code, name}?!is_null(school)

The *conjunction* (``&``) operator is ``true()`` only if both of its
operands are ``true()``.   This example asks for courses in the
``'Accounting'`` department having less than 3 credits (PA4_)::

    /course?department='acc'&credits<3

    course
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    department | number    | title                | credits
    -----------+-----------+----------------------+--------
    acc        | 100       | Practical Bookkeeping | 2

.. _PA4:
    http://demo.htsql.org
    /course?department='acc'&credits<3

The *alternation* (``|``) operator is ``true()`` if either of its
operands is ``true()``.  For example, we could list courses having
anomalous number of credits (PA5_)::

    /course?credits>4|credits<3
  
   course
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   department | number | title                          | credits
   -----------+--------+--------------------------------+--------
   acc        |    100 | Practical Bookkeeping          |       2
   acc        |    315 | Financial Accounting           |       5
   astro      |    142 | Solar System Lab               |       2
   astro      |    155 | Telescope Workshop             |       1
   ...

.. _PA5:
    http://demo.htsql.org
    /course?credits>4|credits<3

The precedence rules for boolean operators follow typical programming
convention, negation binds more tightly than conjunction, which binds
more tightly than alternation.  Parenthesis can be used to override this
default grouping rule or to better clarify intent.  The next example
returns that are in "Art History" or "Studio Art" having more than three
credits (PA6_)::

    /course?(department='arthis'|department='stdart')&credits>3

    course                                                       
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
    department | number | title                         | credits
    -----------+--------+-------------------------------+-------- 
    arthis     | 712    | Museum and Gallery Management | 4       
    stdart     | 411    | Underwater Basket Weaving     | 4       
    stdart     | 509    | Twentieth Century Printmaking | 4       
    stdart     | 614    | Drawing Master Class          | 5       
    ...

.. _PA6:
    http://demo.htsql.org
    /course?(department='arthis'|department='stdart')&credits>3

Without the parenthesis, the expression above would show all courses
from ``'arthis'`` regardless of credits (PA7_)::

    /course?department='arthis'|department='stdart'&credits>3

    course
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    department | number | title                           | credits
    -----------+--------+---------------------------------+--------
    arthis     | 202    | History of Art Criticism        | 3        
    arthis     | 340    | Arts of Asia                    | 3        
    arthis     | 623    | Contemporary Latin American Art | 3        
    ...       

.. _PA7:
    http://demo.htsql.org
    /course?department='arthis'|department='stdart'&credits>3

When a non-boolean is used in a logical expression, it is implicitly
cast as a *boolean*.  As part of this cast, tri-value logic is
flattened, ``null()`` is converted into ``false()``.  For strings, the
empty string (``''``) is also treated as ``false()``.  This conversion
rule shortens URLs and makes them more readable.

For example, this query returns only ``course`` records having a
``description`` (PA8_)::
    
    /course?description
    
.. _PA8:
    http://demo.htsql.org
    /course?description

The predicate ``?description`` is treated as a short-hand for
``?(!is_null(description)&description!='')``.  The negated variant of
this shortcut is more illustrative (PA9_)::

    /course{department,number,description}? !description

    course
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    department | number | description
    -----------+--------+------------
    acc        |    100 |            
    me         |    627 | ""         
                             (2 rows)

.. _PA9:
    http://demo.htsql.org
    /course{department,number,description}? !description


Types and Functions
===================

HTSQL supports *boolean*, *date*, *numeric*, and *text* data types, as
well as variants.  The pluggable type system can be used to augment the
core types provided. 

Working with NULLs
------------------

HTSQL provides a rich function set for handling ``NULL`` expressions;
however, careful attention must be paid.  For starters, the standard
equality operator (``=``) is null-regular, that is, if either operand is
``null()`` the result is ``null()``.  The following request always
returns 0 rows (WN1_)::
  
   /department?school=null()

    department
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    code    | name              
    --------+-------------------
                          0 rows

.. _WN1:
    http://demo.htsql.org
    /department?school=null()

While you wouldn't directly write that query, it could be the final
result after parameter substitution for a templatized query such as
``/department?school=$var``.  For cases like this, use *total equality*
operator (``==``) which treats ``NULL`` values as equivalent (WN2_)::

    /department?school==null()

    department
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    code    | name              
    --------+-------------------
    bursar  | Bursar's Office   
    career  | Career Development
    parent  | Parents & Alumni  
                        (3 rows)

.. _WN2:
    http://demo.htsql.org
    /department?school==null()

The ``!==`` operator lists the complement, including records with a
``NULL`` for the field tested (WN3_)::

    /department?school!=='art'

    department
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    code   | name                   | school
    -------+------------------------+-------
    acc    | Accounting             | bus   
    astro  | Astronomy              | ns    
    be     | Bioengineering         | egn   
    bursar | Bursar's Office        |       
    capmrk | Capital Markets        | bus   
    ...

.. _WN3:
    http://demo.htsql.org
    /department?school!=='art'



Odds & Ends
===========

There are a few more items that are important to know about, but for
which we don't document yet (but will before release candidate).

* untyped literals, ``/{1='1'}``
* single-quote escaping, ``/{'Bursar''s Office'}``
* percent-encoding, ``/{'%25'}``
* functions vs methods
* sort expression, ``/course.sort(credits)``
* limit/offset, ``/course.limit(5,20)``


