********************
  HTSQL Reference
********************

This document describes the use of the HTSQL language.  We start with
describing the syntax of HTSQL, then we discuss the HTSQL data model
and the query semantics and conclude with the list of built-in
data types, functions and operators.


Syntax
======

A valid input of an HTSQL processor is called an HTSQL query.

In a regular mode of operation, an HTSQL processor is started as a web
service and accepts queries as HTTP ``GET`` requests.  However, an HTSQL
query can also be executed using a command-line utility ``htsql-ctl`` or
via internal Python API.

Encoding
--------

An HTSQL query is a string of characters in UTF-8 encoding.  Octets
composing the string could be written literally or percent-encoded.  A
percent-encoded octet is serialized as three characters: ``%`` followed
by two hexdecimal digits encoding the octet value.

.. htsql:: /{'HTSQL', %27HTSQL%27, %27%48%54%53%51%4C%27}
   :query: /%7B'HTSQL',%20%27HTSQL%27,%20%27%48%54%53%51%4C%27%7D
   :hide:

Percent-encoding is useful for transmitting an HTSQL query via channels
that forbid certain characters in literal form.  The list of characters
that should be encoded depends on the channel type, but the percent
(``%``) character itself must always be percent-encoded.

.. htsql:: /{'%25'}
   :query: /%7B'%25'%7D
   :hide:

A ``NUL`` character cannot appear in an HTSQL query, neither in literal
nor in percent-encoded form.

The HTSQL processor decodes percent-encoded octets before parsing the
query.  As a consequence, a percent-encoded punctuation or operator
character still plays its syntax role.

Lexical Structure
-----------------

An HTSQL query is parsed into a sequence of tokens.  The following
tokens are recognized.

*NAME*
    A sequence of alphanumeric characters that does not start with a
    digit.

    .. htsql:: /school
       :cut: 3
       :hide:

*NUMBER*
    A numeric literal: integer, decimal and exponential notations are
    recognized.

    .. htsql:: /{60, 2.125, 271828e-5}
       :hide:

*STRING*
    A string literal enclosed in single quotes; any single quote
    character should be doubled.

    .. htsql:: /{'HTSQL', 'O''Reilly'}
       :hide:

*SYMBOL*
    A valid symbol in the HTSQL grammar; that includes operators and
    punctuation characters.  Some symbols are represented by more than
    one character (e.g. ``<=``, ``!~``).

Individual tokens may be separated by whitespace characters.

See :class:`htsql.tr.scan.Scanner` for detailed description of HTSQL
tokens.

Syntax Structure
----------------

A sequence of HTSQL tokens must obey the HTSQL grammar.

An HTSQL query starts with ``/`` followed by a valid HTSQL expression
and is concluded with an optional query decorator.

The following table lists HTSQL operations in the order of precedence.

+----------------------+---------------------------+---------------------------+----------------------+
| Operation            | Description               | Example Input             | Output               |
+======================+===========================+===========================+======================+
| `x :name`            | infix function call       | ``'HTSQL':length``        | ``5``                |
+----------------------+                           +---------------------------+----------------------+
| `x :name y`          |                           | ``1/3 :round 2``          | ``0.33``             |
+----------------------+                           +---------------------------+----------------------+
| `x :name (y,z,...)`  |                           | ``'HTSQL':slice(1,-1)``   | ``'TSQ'``            |
+----------------------+---------------------------+---------------------------+----------------------+
| `x +`, `x -`         | sorting decorator         | ``program{degree+}``      |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `p | q`              | logical *OR* operator     | ``true()|false()``        | ``true()``           |
+----------------------+---------------------------+---------------------------+----------------------+
| `p & q`              | logical *AND* operator    | ``true()&false()``        | ``false()``          |
+----------------------+---------------------------+---------------------------+----------------------+
| `\! p`               | logical *NOT* operator    | ``!true()``               | ``false()``          |
+----------------------+---------------------------+---------------------------+----------------------+
| `x = y`, `x != y`,   | comparison operators      | ``2+2=4``                 | ``true()``           |
| `x == y`, `x !== y`  |                           |                           |                      |
+----------------------+                           +---------------------------+----------------------+
| `x ~ y`, `x !~ y`    |                           | ``'HTSQL'~'SQL'``         | ``true()``           |
+----------------------+                           +---------------------------+----------------------+
| `x < y`, `x <= y`,   |                           | ``12>7``                  | ``true()``           |
| `x > y`, `x >= y`    |                           |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `x + y`, `x - y`     | addition, subtraction     | ``'HT'+'SQL'``            | ``'HTSQL'``          |
+----------------------+---------------------------+---------------------------+----------------------+
| `x * y`, `x / y`     | multiplication, division  | ``12*7``                  | ``84``               |
+----------------------+---------------------------+---------------------------+----------------------+
| `- x`                | negation                  | ``-42``                   |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `T ^ x`              | projection operator       | ``program^degree``        |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `T ? p`              | sieve operator            | ``program?degree='ms'``   |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `T := x`             | assignment                | |assign-in|               |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `S . T`              | traversal operator        | ``school.program``        |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `{x,y,...}`          | selection operator        | ``{count(school)}``       |                      |
+----------------------+                           +---------------------------+----------------------+
| `T {x,y,...}`        |                           | ``school{code,name}``     |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `name (...)`         | function call             | ``round(1/3,2)``          | ``0.33``             |
+----------------------+---------------------------+---------------------------+----------------------+
| `(...)`              | grouping                  | ``(7+4)*2``               | ``22``               |
+----------------------+---------------------------+---------------------------+----------------------+
| `*`                  | wildcard selection        | ``school.*``              |                      |
+----------------------+                           +---------------------------+----------------------+
| `* number`           |                           | ``school.*1``             |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `^`                  | projection complement     | ``count(^)``              |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `name`               |                           | ``school``                |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `number`             |                           | ``60``, ``2.125``,        |                      |
|                      |                           | ``271828e-5``             |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `string`             |                           | ``'HTSQL'``               |                      |
+----------------------+---------------------------+---------------------------+----------------------+

.. |assign-in| replace:: ``student := student?is_active``

An optional query decorator starts with ``/`` followed ``:`` and the
decorator name.

.. htsql:: /school/:csv
   :hide:

See :class:`htsql.tr.parse.QueryParser` for a formal description of the
HTSQL grammar.

Below we describe individual syntax elements.

Atomic Expressions
------------------

An atomic expression is a basic syntax unit.  HTSQL recognizes the
following atoms:

*Identifier*
    An identifier is a sequence of characters which contains Latin
    letters, underscores (``_``), decimal digits and those Unicode
    characters that are classified as alphanumeric.  An identifier must
    not start with a digit.

    In HTSQL, identifiers are *case-insensitive*.

    Identifiers are used to refer to database entities such as tables
    and attributes, to define calculated attributes, and to call
    functions.

    .. htsql:: /school{name, count(department)}
       :cut: 3
       :hide:

    In this example, four identifiers ``school``, ``name``, ``count``
    and ``department`` represent respectively a table, a table
    attribute, a built-in function and a table link.

*Literal*
    HTSQL supports two types of literal values: *quoted* and *unquoted*.

    An unquoted (or numeric) literal is a number written in integer,
    decimal or exponential notation.

    .. htsql:: /{60, 2.125, 271828e-5}
       :hide:

    The range of allowed numeric values depends on the database backend.
    The type of a numeric literal is determined from notation: literals
    written in integer, decimal and exponential notation are assigned to
    `integer`, `decimal` and `float` data type respectively.

    A quoted literal is a (possibly empty) sequence of arbitrary
    characters enclosed in single quotes.  Any single quote in the value
    must be doubled.

    .. htsql:: /{'HTSQL', 'O''Reilly'}
       :hide:

    The data type of a quoted literal is inferred from the context in
    which the literal is used; the default data type is `string`.

*Wildcard*
    A wildcard selection (``*``) selects all output columns of the
    table.

    .. htsql:: /department{school.*, *}
       :cut: 3
       :hide:

    .. **

    When followed by an integer literal ``N``, a wildcard selects
    ``N``-th output column of the table.  ``N`` starts from ``1`` and
    should not exceed the number of output columns.

    .. htsql:: /school{name, count(department)}?*2>=4
       :cut: 3
       :hide:

*Complement*
    A projection complement (``^``) represents a complement link from a
    projection to the projected table.

    Do not confuse a projection complement with a binary projection
    operator, which is also represented with the ``^`` character.

    .. htsql:: /(program^degree){*, count(^)}
       :cut: 3
       :hide:

    .. **

    In this example, the first and the second occurrences of ``^``
    indicate a projection operator and a projection complement
    respectively.

*Grouping*
    Any expression enclosed in parentheses (``(...)``) is treated
    syntactically as a single atom.  Use grouping to override the
    default operator precedence.

    .. htsql:: /(7+4)*2
       :hide:

    Do not confuse a grouping operation with a function call, which also
    uses parentheses.

Function Calls
--------------

HTSQL has a large library of built-in functions and can be extended with
user-defined functions.

A function call is represented as a function name followed by ``(``, a
comma-separated list of arguments, and ``)``.

.. htsql:: /round(1/3, 2)
   :hide:

A function may accept no arguments, but the parentheses are still
required.

.. htsql:: /today()
   :hide:

For functions with at least one argument, HTSQL supports an alternative
infix call notation.  In this notation, the expression starts with the
first argument followed by ``:`` and a function name, and then the rest
of the arguments.  The trailing arguments must be enclosed in
parentheses if their number is more than one.

.. htsql:: /{today() :year, 1/3 :round 2, 'HTSQL' :slice(1, -1)}
   :hide:

This example could be equivalently expressed as

.. htsql:: /{year(today()), round(1/3, 2), slice('HTSQL', 1, -1)}
   :hide:

Infix function calls are composable and have the lowest precedence among
the operators.

.. htsql:: /{'h'+'t'+'t'+'p' :replace('tp', 'sql') :upper}
   :hide:

For a list and description of built-in functions, see the respective
section of the reference.

Operators
---------

An HTSQL operator is denoted by a special character or a sequence of
characters (e.g. ``+``, ``<=``).  HTSQL has infix, prefix and postfix
operators, and some operators admit all three forms.

The current version of HTSQL does not support user-defined operators;
future versions may add this ability.

In HTSQL, the order in which the operators are applied is determined by
*operator precedence*.  For example, multiplication and division
operators have a higher precedence than addition and subtraction.

Some HTSQL operators are composable (e.g. arithmetic operators) and some
are not (e.g. equality operators).  We call the former *associative* and
the latter *non-associative*.

*Logical Operators*
    HTSQL supports the following logical operators:

    * `p | q` --- logical *OR*;
    * `p & q` --- logical *AND*;
    * `\! p` --- logical *NOT*.

    In this list, the operators are sorted by the order of precedence,
    from lowest to highest.  All logical operators are left-associative.

    .. htsql:: /{true()|false(), true()&false(), !false()}
       :hide:

*Comparison Operators*
    HTSQL supports the following comparison operators:

    * `x = y`, `x != y`, `x == y`, `x !== y` --- *equality* operators;
    * `x ~ y`, `x !~ y` --- *containing* operators;
    * `x < y`, `x <= y`, `x > y`, `x >= y` --- *ordering* operators.

    .. htsql:: /{2+2=4, 'HTSQL'~'SQL', 12>7&7>=2}
       :hide:

    All comparison operators have the same precedence and are not
    associative.

    Future versions of HTSQL may make ordering operators
    left-associative to express *between* operation (e.g.
    `a <= x <= b`).

*Arithmetic Operators*
    HTSQL supports the usual set of arithmetic operators:

    * `x + y` --- *addition*;
    * `x - y` --- *subtraction*;
    * `x * y` --- *multiplication*;
    * `x / y` --- *division*;
    * `- x` --- *negation*.

    .. htsql:: /{'HT'+'SQL', today()-1, -6*4/5}
       :hide:

    Arithmetic operators have standard precedence and associativity.

*Table Operators*
    HTSQL supports specialized operators to work with table expressions:

    * `T ^ x` --- *projection* operator;
    * `T ? p` --- *sieve* operator;
    * `S . T` --- *traversal* operator;
    * `T {x,y,...}` --- *selection* operator.

    The projection operator (`T ^ x`) produces a row set containing all
    unique values of `x` as it ranges over `T`.  Do not confuse the
    projection operator with a projection complement.

    .. htsql:: /program^degree
       :cut: 3
       :hide:

    .. **

    The sieve operator (`T ? p`) produces rows of `T` satisfying
    condition `p`.

    .. htsql:: /school?code='art'
       :hide:

    The traversal operator (`S . T`) evaluates `T` in the context of
    `S`.

    .. htsql:: /(school?code='art').program
       :hide:

    The selection operator specifies output columns.  The operator
    admits two forms: with and without the selection base.

    .. htsql:: /school{name}
       :cut: 3
       :hide:

    .. htsql:: /{count(school)}
       :hide:

    Table operators have irregular precedence; for more details, see the
    HTSQL grammar.  For a comprehensive description of the semantics of
    table operators, see the respective section of the reference.

*Sorting Decorators*
    `x +` and `x -` are two sorting decorators indicating ascending and
    descending order respectively.

    .. htsql:: /course.sort(department_code+,credits-)
       :cut: 3
       :hide:

    Sorting decorators have the same precedence as infix function call.

    Sorting decorators are only meaningful when used as arguments of the
    `sort()` function and in a selector expression.

*Assignment*
    `T := x` is an assignment expression.

    The left side of an assignment must be an identifier, a function
    call or a traversal operator, and it indicates the name and formal
    parameters (if any) of a calculated attribute.  The right side of an
    assignment is an arbitrary expression.

    .. htsql:: /school{name, num_dept}?num_dept>=4 :where school.num_dept := count(department)
       :cut: 3
       :hide:

    An assignment expression could be used only as an argument of
    functions `define()` and `where()`.

For a comprehensive description built-in operators see the respective
section.


Data Model and Query Semantics
==============================

In this section, we describe how HTSQL represents information in the
database and how the HTSQL translator interprets the queries.

Data Model
----------

HTSQL is not a full-fledged database system.  As opposed to regular data
stores, it does not include a storage layer, but relies on a relational
database server to physically store and retrieve data.

HTSQL is designed to work on top of existing relational databases and
does not impose any restrictions on how information is modeled and
stored there.  At the same time, HTSQL works best when the data in the
database is highly normalized.

Even though HTSQL wraps a relational database, it does not expose the
relational model directly to the users.  Instead it derives *HTSQL data
model* from the underlying database and uses this model when presenting
data to the users and interpreting user queries.  HTSQL data model is
very close to traditional `network data model`_ utilized by CODASYL, and
various OODBMS and ORM systems.

.. _network data model: http://en.wikipedia.org/wiki/Network_model

In the next sections, we describe HTSQL data model and how it is
inferred from the relational model of the underlying database.

Model and Instances
-------------------

When describing how information is represented by HTSQL, we
differentiate between *a database model* and *a database instance*.

A database model specifies the structure of the database: what types of
business entities are represented and how the entities may relate to
each other.  A database instance is the actual data in the database
and must satisfy the constraints imposed by the model.  The difference
between a model and an instance is the difference between the shape
of data and data itself.

Let's consider the model of a student enrollment system in a fictional
university.  This model may contain schools, programs administered
by a school, departments associated with a school, and courses offered
by a department.  A concrete instance of this model may contain
a school of *Engineering* with associated departments of *Computer
Science*, *Electrical Engineering*, etc.:

.. diagram:: dia/model-and-instance.tex
   :align: center

Classes and Links
-----------------

HTSQL structures the data with *classes* and *links*, which together
form *a model graph*.  Classes, which are the nodes in the model graph,
represents types of entities.  Links, which are the arcs in the model
graph, describe relations between entities.  Both classes and links
have a name.

Among classes we distinguish *domain classes* and *record classes*.
Domain classes represent scalar data types such as `boolean`, `integer`,
`string`, `date`.  Record classes represent types of business entities
modeled by the database.  A student enrollment system in our example
would have record classes such as `school`, `program`, `department`,
`course`.

Links are classified by the type of classes they connect.  A link from a
record class to a domain class indicates that records of this class have
an attribute, which type is specified by the domain class.  For example,
`school` class may have a link called `name` to `string` class, which
indicates that each *school* record has a string attribute *name*.

A link between two record classes indicates that records of these
classes are related to each other.  For example, `department` class
has a link to `school` class, which indicates that each *department*
record may be associated with some *school* record.

.. diagram:: dia/sample-model.tex
   :align: center

Since different links may have the same name, we will use dotted
notation `class.link` to indicate links.  Here, `class` is the name of a
class, `link` is the name of a link originating from the class.  Thus,
`school.name` and `department.school` are links on the diagram.

Records and Relations
---------------------

As we focus from the database model to a specific instance, classes
are populated with values and records, and links are expanded to
relations between individual items.

On the instance level, a domain class is transformed into a set of all
values of the respective type.  Thus, `boolean` class contains two
values: ``true`` and ``false``, `integer` class contains all integer
numbers, and so on.

A record class becomes a set of records representing business entities
of this class.

It is convenient to depict an entity as a collection of attribute
values, hence the word "record".  Even though it is permitted for two
different records to have the same set of attribute values, in practice,
there often exists an attribute or a group of attributes which could
uniquely identify a record.  We use the value of such an attribute
enclosed in brackets to denote records in writing.  Thus, an instance of
class `school` may contain records ``[eng]``, ``[la]``, ``[ns]``
representing respectively schools of *Engineering*, of *Arts and
Humanities*, and of *Natural Sciences*, assuming that we use attribute
`school.code` to uniquely identify records.

.. diagram:: dia/sample-instance-1.tex
   :align: center

A link between two classes is unwound into connections between elements
of these classes.  If in the database model a link represents an entity
attribute, in a specific instance a link connects records to attribute
values.  A link between two record classes would connect records of
these classes.

For example, link `school.name` connects a school record ``[eng]`` to a
string value ``'School of Engineering'``.  The record ``[eng]`` is also
connected to department records ``[comp]`` and ``[ee]`` indicating that
*Department of Computer Science* and *Department of Electrical
Engineering* belong to *School of Engineering*.

.. diagram:: dia/sample-instance-2.tex
   :align: center

Some links may enforce constraints on connections between elements.
We classify these constraints as follows:

A link is called *singular* if any element of the origin class is
connected to no more than one element of the target class.  Otherwise,
the link is called *plural*.

For example, all links representing attributes are singular; link
`department.school` is also singular because each department may be
associated with just one school, but the *reverse* link
`school.department` is plural since a school may contain more than one
department.

.. diagram:: dia/singular-links.tex
   :align: center

A link is called *total* if any element of the origin class is connected
to at least one element of the target class.  Otherwise, the link is
called *partial*.

For example, we require that every school entity has a code, therefore
attribute `school.code` is total.  We also permit a department
to lack an associated school, which means link `department.school`
is partial.

.. diagram:: dia/total-links.tex
   :align: center

A link is called *unique* if any element of the target class is
connected to no more than one element of the origin class.  Otherwise,
the link is *non-unique*.

Attribute `school.name` is unique since different school entities must
have different names, but link `department.school` is non-unique as
different departments are allowed to be associated with the same school.

.. diagram:: dia/unique-links.tex
   :align: center

Note that links constraints are defined on the database model
and applied to all instances of the model.

Correspondence to the relational model
--------------------------------------

In this section, we explain how underlying relation database model
is translated to HTSQL data model.

For the most part, translation of relational structure to HTSQL model
is straightforward.  SQL data types become domain classes, SQL tables
become record classes, table columns are class attributes.

Column constraints are trivially translated to properties of the
respective attributes.  ``NOT NULL`` constraint on a table column means,
in HTSQL terms, that the respective class attribute is total.
``UNIQUE`` constraint on a column indicates that the respective
attribute link is unique.  ``PRIMARY KEY`` constraint indicates that the
attribute link is both total and unique.

The link structure of the model graph is provided by foreign key
constraints.  Specifically, a foreign key creates a singular link
from the referring class to the referred class.

Consider, for example, the following fragment of an SQL schema:

.. sourcecode:: sql

   CREATE TABLE ad.school (
       code                VARCHAR(16) NOT NULL,
       name                VARCHAR(64) NOT NULL,
       campus              VARCHAR(5),
       CONSTRAINT school_pk
         PRIMARY KEY (code),
       CONSTRAINT name_uk
         UNIQUE (name),
       CONSTRAINT school_campus_ck
         CHECK (campus IN ('old', 'north', 'south'))
   );

   CREATE TABLE ad.department (
       code                VARCHAR(16) NOT NULL,
       name                VARCHAR(64) NOT NULL,
       school_code         VARCHAR(16),
       CONSTRAINT department_pk
         PRIMARY KEY (code),
       CONSTRAINT department_name_uk
         UNIQUE (name),
       CONSTRAINT department_school_fk
         FOREIGN KEY (school_code)
         REFERENCES ad.school(code)
   );

HTSQL model of this schema consists of two classes, `school` and
`department`, each with three attributes: `code`, `name`, `campus`
and `code`, `name`, `school_code` respectively.  Additionally,
the foreign key constraint ``department_school_fk`` generates
a singular link from class `department` to class `school` and a
reverse plural link from class `school` to class `department`.

Data Flow
---------

A central concept in HTSQL is *data flow*, a sequence of homogeneous
values.

HTSQL is a data flow transformation language.  Every HTSQL expression
operates on flows; that is, it accepts an *input flow* and transforms it
into an *output flow*.

(diagram: input flow -> expression -> output flow)

The initial input flow consists of a single empty record.  HTSQL
processor interprets the given HTSQL query as a sequence (or rather a
directed graph) of flow operations, which it applies one by one.  The
resulting flow is then displayed to the user in a tabular form.

Different operations affect the flow in various ways: multiply it, or
remove elements from it, apply a scalar function to each element, etc.
In the next sections, we discuss different types flow operations.

Scalar Expressions
------------------

A simplest example of a flow operation is an application of some
expression to each value in a flow.  The output flow consists of a
results of the expression.

That kind of expression does not change the number of elements in the
flow; we call such expressions *scalar*.

.. htsql:: /(3+4)*6

In this example, a scalar expression ``(3+4)*6`` is applied to the
initial flow; the value of this expression forms the resulting flow.

(diagram: [] -> (3+4)*6 -> 42)

.. htsql:: /school{code, count(department)}
   :cut: 4

In this example, two scalar expressions ``code`` and
``count(department)`` are applied to the flow consisting of *school*
records.  For each school entity, they extract the value of the
attribute ``code`` and the number of associated departments.

(diagram: [art], [bus], [edu], [eng], ...
    -> {'art',2}, {'bus',3}, {'edu',2}, {'eng',4}, ...)

A scalar expression is an example of a *singular* expression; one which
does not increase the number of elements in the flow, as opposed to a
*plural* expression, which may produce more output elements than in the
input flow.

Navigation
----------

Navigation is an operation of selecting the initial record class or
traversing a link.

When used in the root scope, a class name produces a flow of all records
from the class.

.. htsql:: /school
   :cut: 4

(diagram: [] -> (school) -> [art], ...)

In a class scope, the name of a link produces the flow consisting of
associated records from the target class.

.. htsql:: /school.department
   :cut: 4

(diagram: [] -> (school) -> [art], ... -> (department) -> [arthis], ...)

As in the previous example, ``school`` generates a flow of *school*
records.  Then we traverse a link ``school.department``.  That each, for
each school record in the input flow, we find the associated
*department* records, the output flow consists of all *department*
records combined.

A traversal operation is singular or plural depending on whether the
respective link is singular or plural.

Filtering
---------

A *sieve* expression filters the input flow leaving only those elements
which satisfy the given condition.

A sieve expression takes one argument: a scalar logical expression
called the *filter*.  It applies the filter to each element of the input
flow.  The output flow consists of those elements of the input flow for
which the filter is evaluated to *TRUE* value.

.. htsql:: /school?count(department)>3

(diagram)

In this example, the sieve expression evaluates a filter condition
``count(department)>3`` for each record from the *school* class; those
records for which this condition is valid generate the output of the
query.

A *sort* expression reorders elements in the flow according to a given
argument.

.. htsql:: /school.sort(name+)
   :cut: 4

(diagram)

In this example, the *school* records are ordered in the ascending order
with respect to the value of ``name`` attribute.

A *truncation* operation makes a slice of the input flow.

.. htsql:: /school.limit(3)

(diagram)

In this case, we take the top 3 records from the *school* class.

Aggregates
----------

An aggregate function converts a plural expression into a scalar.

The argument of an aggregate function must be a plural expression.  Then
for each element of the input flow, the aggregate evaluates the
respective sub-flow and applies a set function to the result to generate
a scalar value.

.. htsql:: /count(school)

(diagram)

In this example, ``count()`` aggregates produces the number of elements
in the flow generated by expression ``school``.

.. htsql:: /department{code, max(course.credits)}
   :cut: 4

(diagram)

In this example, ``max(course.credits)`` starts with evaluating the flow
``department.course.credits``.  Then for each *department* record of the
input flow, ``max()`` finds the maximum value in the respective
sub-flow.

Projection
----------

A projection expression takes a scalar argument called the *kernel*.
The output flow of projection consists of all unique values of the
kernel as it runs over the input flow.

.. htsql:: /school^campus

(diagram)

The output of this query consists of all distinct values of
`school.campus` attribute.

Naming Scope
------------

In HTSQL, identifiers are used to refer to class names, attributes,
links as so on.  A collection of available names and associated objects
is called a naming *scope*.

Root Scope
----------

The root scope is the top level scope in the scope stack -- it is the
scope where the query is evaluated.  This scope contains the names of
all classes (tables) in the database.

.. htsql:: /{count(school), count(department)}

In this example, identifiers ``school`` and ``department`` belong to the
root scope and are associated with the respective classes.

Class Scope
-----------

The class scope is associated with some class (table) of the database.
The scope contains names of all class attributes and links to other
classes.

.. htsql:: /school{code, count(department)}?exists(program)
   :cut: 4

In this example, ``school`` belongs to the root scope while identifiers
``code``, ``department`` and ``program`` belong to the scope of `school`
class.  ``school.code`` is the attribute of `school`,
``school.department`` and ``school.program`` are links to the respective
classes.

Projection Scope
----------------

The projection scope is associated with a projection expression.

Projection is an example of a derived class: its records are composed
from unique values of the kernel as it runs over the base class.  A
projection class has a natural link back to the base class: it relates
the value of the kernel to every record of the base class that produced
this value.

(diagram)

This link is called a *complement* link.  HTSQL assigns the name for the
link that coincides with the name of the base class.  In cases when
HTSQL is unable to deduce a link name, one may use a special
*complement* expression: `^`.

Attributes of the projection class are values of the kernel expression.
When possible, HTSQL automatically assigns names for attributes,
otherwise, the user may define custom attribute names.

.. htsql:: /(school^campus){campus, count(school)}

In this example, the projection scope ``(school^campus)`` has two names:
the attribute name ``campus`` and the kernel link ``school``.

.. htsql::

    /(school^{num_dept := count(department)})
        {num_dept, count(school)}

In this example, we assign the name ``num_dept`` to the projection
attribute.

Modifying Scope
---------------

HTSQL allows adding new attributes to an existing scope, see
functions ``define()`` and ``where()``.

References
----------

Traversing a link changes the scope; any names defined in the previous
scope are no longer available.  To pass values between different scopes,
use references.

Data Types
==========

Every HTSQL expression has an associated type.  The type defines the set
of valid values produced by the expression and permitted operations over
the expression.  The type also indicates how returned values are
formatted in the output.

Since HTSQL wraps an SQL database, HTSQL data types are related to SQL
data type.  Although HTSQL does not expose SQL data types directly to
the user, each SQL data type corresponds to some HTSQL data type and
vice versa.

In this section we describe what data types HTSQL supports, how HTSQL
types are mapped to SQL types, the format of input literals for each
data type, etc.

Regular and Special Types
-------------------------

HTSQL demands that every expression has an associated type.  For
example, in the query:

.. htsql:: /{2+2=4, count(school), date('2010-04-15')-6813}

the expressions ``2+2=4``, ``count(school)``,
``date('2010-04-15')-6813`` have the types `boolean`, `integer` and
`date` respectively.  These are *regular* types.

The following table lists the default set of supported regular data
types in HTSQL; more data types could be added by *HTSQL extensions*.

+----------------------+---------------------------+---------------------------+
| Type                 | Description               | Example Input             |
+======================+===========================+===========================+
| `boolean`            | logical data type, with   | ``true()``                |
|                      | two values: *TRUE* and    +---------------------------+
|                      | *FALSE*                   | ``false()``               |
+----------------------+---------------------------+---------------------------+
| `integer`            | binary integer type       | ``4096``                  |
+----------------------+---------------------------+---------------------------+
| `decimal`            | arbitrary-precision       | ``124.49``                |
|                      | exact numeric type        |                           |
+----------------------+---------------------------+---------------------------+
| `float`              | IEEE 754 floating-point   | ``271828e-5``             |
|                      | inexact numeric type      |                           |
+----------------------+---------------------------+---------------------------+
| `string`             | text data type            | ``string('HTSQL')``       |
+----------------------+---------------------------+---------------------------+
| `enum`               | enumeration data type,    |                           |
|                      | with predefined set of    |                           |
|                      | valid string values       |                           |
+----------------------+---------------------------+---------------------------+
| `date`               | calendar date             | ``date('2010-04-15')``    |
+----------------------+---------------------------+---------------------------+
| `time`               | time of day               | ``time('20:13:04.5')``    |
+----------------------+---------------------------+---------------------------+
| `datetime`           | date and time combined    | |datetime-in|             |
+----------------------+---------------------------+---------------------------+
| `opaque`             | unrecognized data type    |                           |
+----------------------+---------------------------+---------------------------+

.. |datetime-in| replace:: ``datetime('2010-04-15 20:13:04.5')``

Some HTSQL expressions do not produce a proper value and therefore
cannot be assigned a regular data type.  In this case, the expression is
assigned one of the *special* data types: `record`, `untyped` or `void`.

Record entities are assigned the `record` type.  This type is special
since values of this type are never displayed directly and it has no
corresponding SQL data type.

Quoted HTSQL literals have no intrinsic data type; their actual type is
determined from the context.  Until it is determined, HTSQL translator
assign them a temporary `untyped` type.

Some expressions, such as assignments, produce no values and therefore
have no meaningful data type.   In this case, the assigned type is
`void`.

The following table lists supported special data types.

+----------------------+---------------------------+---------------------------+
| Type                 | Description               | Example Input             |
+======================+===========================+===========================+
| `record`             | type of record entities   | ``school``                |
+----------------------+---------------------------+---------------------------+
| `untyped`            | initial type of quoted    | ``'HTSQL'``               |
|                      | literals                  |                           |
+----------------------+---------------------------+---------------------------+
| `void`               | type without any valid    |                           |
|                      | values                    |                           |
+----------------------+---------------------------+---------------------------+

Literal Expressions
-------------------

A literal expression is an atomic expression that represents a fixed
value.  HTSQL supports two types of literals: *numeric* (or unquoted) and
*quoted*.

An unquoted literal is a number written in one of the following forms:

* an integer number
* a number with a decimal point
* a number in exponential notation

.. htsql:: /{60, 2.125, 271828e-5}

Literals in these forms are assigned `integer`, `decimal` and `float`
types respectively.

A quoted literal is an arbitrary string value enclosed in single quotes.

.. htsql:: /{'', 'HTSQL', 'O''Reilly'}

In this example, three literal expressions represent an empty string,
*HTSQL* and *O'Reilly* respectively.  Note that to represent a single
quote in the value, we must duplicate it.

As opposed to numeric literals, quoted literals have no intrinsic type,
their type is determined from the context.  Specifically, the type of
a quoted literal is inferred from the innermost expression that contains
the literal.  Until the actual data type of a quoted literal is
determined, the literal is assigned an `untyped` type.

Consider a query:

.. htsql:: /2+2='4'

Here, a quoted literal ``'4'`` is a right operand of an equality
expression, and its left counterpart ``2+2`` has the type `integer`.
Therefore, HTSQL processor is able to infer `integer` for the literal
``'4'``.

There is no generic rule how to determine the type of a quoted literal;
every operator and function have different rules how to treat untyped
values.  However the content of the literal is never examined when
determining its data type.  It is possible to explicitly specify the
type of an unquoted literal by applying a *cast* operator.

.. htsql:: /{string('2010-04-15'), date('2010-04-15')}

Here, the same quoted literal is converted to `string` and `date` data
types respectively.  Each data type has a set of quoted literals it
accepts; it is an error when the quoted literal does not obey the format
expected by a particular type.

.. htsql:: /{integer('HTSQL')}
   :error:

Note the error generated because ``'HTSQL'`` is not a valid format for
an integer literal.

Type Conversion
---------------

Expressions of one type could be explicitly converted to another type
using a *cast* function.  A cast function is a regular function with one
argument; the name of the function coincides with the name of the target
type.

Not every conversion is permitted; for instance, an integer value could
be converted to a string, but not to a date:

.. htsql:: /string(60)

.. htsql:: /date(60)
   :error:

Implicit type conversion is called *coercion*.  In an arithmetic
formulas and other expressions that require homogeneous arguments, when
the operands are of different types, values of less generic types are
converted to the most generic type.  The order of conversion is as
follows:

* `integer`
* `decimal`
* `float`



Boolean
-------

Type `boolean` is a logical data type with two values: *TRUE*
and *FALSE*.

.. htsql:: /{boolean('true'), boolean('false')}

.. htsql:: /{true(), false()}

The following table maps the `boolean` type to respective
native data types.

+----------------------+---------------------------+
| Backend              | Native types              |
+======================+===========================+
| *sqlite*             | ``BOOL``, ``BOOLEAN`` or  |
|                      | any type containing       |
|                      | ``BOOL`` in its name      |
+----------------------+---------------------------+
| *pgsql*              | ``BOOLEAN``               |
+----------------------+---------------------------+
| *mysql*              | ``BOOL`` aka ``BOOLEAN``  |
|                      | aka ``TINYINT(1)``        |
+----------------------+---------------------------+
| *oracle*             | |oracle-native|           |
+----------------------+---------------------------+
| *mssql*              | ``BIT``                   |
+----------------------+---------------------------+

.. |oracle-native| replace:: ``NUMBER(1) CHECK (X IN (0, 1))``






Special Data Types
==================


Function Syntax
===============

A few observations about HTSQL's function and operator usage:

* For any function, "``f(x,y)``" can be written "``x :f(y)``" and
  depending upon grammatical context, abbreviated to "``x :f y``". 

* Unless annotated, functions are null-regular, that is, if any of 
  their arguments is ``null()`` then the result is ``null()``.

* HTSQL uses zero-based indexes, e.g. the 1st item in a collection is 
  indexed by ``0``, the 2nd character indexed by ``1``, and so on. 

* A single quoted string in an HTSQL request is an *untyped* literal,
  and is automatically cast depending upon the context -- it is not
  necessarily a string value.


Logical Operators
=================

+----------------------+---------------------------+---------------------------+----------------------+
| Function             | Description               | Example Input             | Output               |
+======================+===========================+===========================+======================+
| `boolean(x)`         | cast *x* to Boolean       | ``boolean(true())``       | ``true()``           |
|                      |                           +---------------------------+----------------------+
|                      |                           | ``boolean(false())``      | ``false()``          |
|                      |                           +---------------------------+----------------------+
|                      |                           | ``boolean(1)``            | ``true()``           |
|                      |                           +---------------------------+----------------------+
|                      |                           | |boolean-from-string-in|  | ``true()``           |
|                      |                           +---------------------------+----------------------+
|                      |                           | ``boolean(string(''))``   | ``false()``          |
|                      |                           +---------------------------+----------------------+
|                      |                           | |boolean-from-date-in|    | ``true()``           |
|                      |                           +---------------------------+----------------------+
|                      |                           | ``boolean(null())``       | ``null()``           |
|                      |                           +---------------------------+----------------------+
|                      |                           | |boolean-from-null-s-in|  | ``false()``          |
+----------------------+---------------------------+---------------------------+----------------------+
| `true()`             | logical *TRUE* value      | ``true()``                |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `false()`            | logical *FALSE* value     | ``false()``               |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `p & q`              | logical *AND* operator;   | ``true()&true()``         | ``true()``           |
|                      | treats nulls as *UNKNOWN* +---------------------------+----------------------+
|                      |                           | ``true()&false()``        | ``false()``          |
|                      |                           +---------------------------+----------------------+
|                      |                           | ``false()&false()``       | ``false()``          |
|                      |                           +---------------------------+----------------------+
|                      |                           | ``true()&null()``         | ``null()``           |
|                      |                           +---------------------------+----------------------+
|                      |                           | ``false()&null()``        | ``false()``          |
+----------------------+---------------------------+---------------------------+----------------------+
| `p | q`              | logical *OR* operator;    | ``true()|true()``         | ``true()``           |
|                      | treats nulls as *UNKNOWN* +---------------------------+----------------------+
|                      |                           | ``true()|false()``        | ``true()``           |
|                      |                           +---------------------------+----------------------+
|                      |                           | ``false()|false()``       | ``false()``          |
|                      |                           +---------------------------+----------------------+
|                      |                           | ``true()|null()``         | ``true()``           |
|                      |                           +---------------------------+----------------------+
|                      |                           | ``false()|null()``        | ``null()``           |
+----------------------+---------------------------+---------------------------+----------------------+
| `\!p`                | logical *NOT* operator;   | ``!true()``               | ``false()``          |
|                      | treats nulls as *UNKNOWN* +---------------------------+----------------------+
|                      |                           | ``!false()``              | ``true()``           |
|                      |                           +---------------------------+----------------------+
|                      |                           | ``!null()``               | ``null()``           |
+----------------------+---------------------------+---------------------------+----------------------+
| `is_null(x)`         | *x* is null               | ``is_null(null())``       | ``true()``           |
+----------------------+---------------------------+---------------------------+----------------------+
| `x = y`              | *x* is equal to *y*       | ``'HTSQL'='QUEL'``        | ``false()``          |
|                      |                           +---------------------------+----------------------+
|                      |                           | ``2=null()``              | ``null()``           |
+----------------------+---------------------------+---------------------------+----------------------+
| `x != y`             | *x* is not equal to *y*   | ``'HTSQL'!='QUEL'``       | ``true()``           |
|                      |                           +---------------------------+----------------------+
|                      |                           | ``2!=null()``             | ``null()``           |
+----------------------+---------------------------+---------------------------+----------------------+
| `x == y`             | *x* is equal to *y*;      | ``'HTSQL'=='QUEL'``       | ``false()``          |
|                      | treats nulls as regular   +---------------------------+----------------------+
|                      | values                    | ``2==null()``             | ``false()``          |
+----------------------+---------------------------+---------------------------+----------------------+
| `x !== y`            | *x* is not equal to *y*;  | ``'HTSQL'!=='QUEL'``      | ``true()``           |
|                      | treats nulls as regular   +---------------------------+----------------------+
|                      | values                    | ``2!==null()``            | ``true()``           |
+----------------------+---------------------------+---------------------------+----------------------+
| `x = {a,b,c,...}`    | *x* is among *a*, *b*,    | ``5={2,3,5,7}'``          | ``true()``           |
|                      | *c*, ...                  |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `x != {a,b,c,...}`   | *x* is not among *a*,     | ``5!={2,3,5,7}'``         | ``false()``          |
|                      | *b*, *c*, ...             |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `x < y`              | *x* is less than *y*      | ``1<10``                  | ``true()``           |
|                      |                           +---------------------------+----------------------+
|                      |                           | ``'omega'<'alpha'``       | ``false()``          |
+----------------------+---------------------------+---------------------------+----------------------+
| `x <= y`             | *x* is less than or equal | ``1<=10``                 | ``true()``           |
|                      | to *y*                    +---------------------------+----------------------+
|                      |                           | ``'omega'<='alpha'``      | ``false()``          |
+----------------------+---------------------------+---------------------------+----------------------+
| `x > y`              | *x* is greater than *y*   | ``1>10``                  | ``false()``          |
|                      |                           +---------------------------+----------------------+
|                      |                           | ``'omega'>'alpha'``       | ``true()``           |
+----------------------+---------------------------+---------------------------+----------------------+
| `x >= y`             | *x* is greater than or    | ``1>=10``                 | ``false()``          |
|                      | equal to *y*              +---------------------------+----------------------+
|                      |                           | ``'omega'>='alpha'``      | ``true()``           |
+----------------------+---------------------------+---------------------------+----------------------+
| `if_null(x,y)`       | *x* if *x* is not null;   | ``if_null(1,0)``          | ``1``                |
|                      | *y* otherwise             +---------------------------+----------------------+
|                      |                           | ``if_null(null(),0)``     | ``0``                |
+----------------------+---------------------------+---------------------------+----------------------+
| `null_if(x,y)`       | *x* if *x* is not equal   | ``null_if(1,0)``          | ``1``                |
|                      | to *y*; null otherwise    +---------------------------+----------------------+
|                      |                           | ``null_if(0,0)``          | ``null()``           |
+----------------------+---------------------------+---------------------------+----------------------+
| |if-fn|              | first *ck* such that *pk* | |if-true-in|              | ``'up'``             |
+----------------------+ is *TRUE*; *o* or null    +---------------------------+----------------------+
| |if-else-fn|         | otherwise                 | |if-false-in|             | ``'down'``           |
+----------------------+---------------------------+---------------------------+----------------------+
| |switch-fn|          | first *ck* such that *x*  | |switch-1-in|             | ``'up'``             |
+----------------------+ is equal to *yk*; *o* or  +---------------------------+----------------------+
| |switch-else-fn|     | null otherwise            | |switch-0-in|             | ``'down'``           |
+----------------------+---------------------------+---------------------------+----------------------+

.. |boolean-from-string-in| replace:: ``boolean(string('HTSQL'))``
.. |boolean-from-date-in| replace:: ``boolean(date('2010-04-15'))``
.. |boolean-from-null-s-in| replace:: ``boolean(string(null()))``
.. |if-fn| replace:: `if(p1,c1,...,pn,cn)`
.. |if-else-fn| replace:: `if(p1,c1,...,pn,cn,o)`
.. |if-true-in| replace:: ``if(true(),'up','down')``
.. |if-false-in| replace:: ``if(false(),'up','down')``
.. |switch-fn| replace:: `switch(x,y1,c1,...,yn,cn)`
.. |switch-else-fn| replace:: `switch(x,y1,c1,...,yn,cn,o)`
.. |switch-1-in| replace:: ``switch(1,1,'up',0,'down')``
.. |switch-0-in| replace:: ``switch(0,1,'up',0,'down')``


Numeric Functions
=================

+----------------------+---------------------------+---------------------------+----------------------+
| Function             | Description               | Example Input             | Output               |
+======================+===========================+===========================+======================+
| `integer(x)`         | cast *x* to integer       | ``integer(60)``           | ``60``               |
|                      |                           +---------------------------+----------------------+
|                      |                           | ``integer(17.25)``        | ``17``               |
|                      |                           +---------------------------+----------------------+
|                      |                           | ``integer(223607e-5)``    | ``2``                |
|                      |                           +---------------------------+----------------------+
|                      |                           | ``integer(string('60'))`` | ``60``               |
+----------------------+---------------------------+---------------------------+----------------------+
| `decimal(x)`         | cast *x* to decimal       | ``decimal(60)``           | ``60.0``             |
|                      |                           +---------------------------+----------------------+
|                      |                           | ``decimal(17.25)``        | ``17.25``            |
|                      |                           +---------------------------+----------------------+
|                      |                           | ``decimal(223607e-5)``    | ``2.23607``          |
|                      |                           +---------------------------+----------------------+
|                      |                           | |decimal-from-string-in|  | ``17.25``            |
+----------------------+---------------------------+---------------------------+----------------------+
| `float(x)`           | cast *x* to float         | ``float(60)``             | ``6e1``              |
|                      |                           +---------------------------+----------------------+
|                      |                           | ``float(17.25)``          | ``1725e-2``          |
|                      |                           +---------------------------+----------------------+
|                      |                           | ``float(223607e-5)``      | ``223607e-5``        |
|                      |                           +---------------------------+----------------------+
|                      |                           | |float-from-string-in|    | ``223607e-5``        |
+----------------------+---------------------------+---------------------------+----------------------+
| `-x`                 | negate *x*                | ``-7``                    |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `x + y`              | add *x* to *y*            | ``13+7``                  | ``20``               |
+----------------------+---------------------------+---------------------------+----------------------+
| `x - y`              | subtract *y* from *x*     | ``13-7``                  | ``6``                |
+----------------------+---------------------------+---------------------------+----------------------+
| `x * y`              | multiply *x* by *y*       | ``13*7``                  | ``91``               |
+----------------------+---------------------------+---------------------------+----------------------+
| `x / y`              | divide *x* by *y*         | ``13/7``                  | ``1.85714285714286`` |
+----------------------+---------------------------+---------------------------+----------------------+
| `round(x)`           | round *x* to the nearest  | ``round(17.25)``          | ``17``               |
|                      | integer                   |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `round(x,n)`         | round *x* to *n* decimal  | ``round(17.25,1)``        | ``17.3``             |
|                      | places                    |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+

.. |decimal-from-string-in| replace:: ``decimal(string('17.25'))``
.. |float-from-string-in| replace:: ``float(string('223607e-5'))``


String Functions
================

By convention, string functions take a string as its first parameter.
When an untyped literal, such as ``'value'`` is used and a string is
expected, it is automatically cast.  Hence, for convenience, we write
string typed values using single quotes in the output column.

+----------------------+---------------------------+---------------------------+----------------------+
| Function             | Description               | Example Input             | Output               |
+======================+===========================+===========================+======================+
| `string(x)`          | cast *x* to string        | ``string('Hello')``       | ``'Hello'``          |
|                      |                           +---------------------------+----------------------+
|                      |                           | ``string(1.0)``           | ``'1.0'``            |
|                      |                           +---------------------------+----------------------+
|                      |                           | ``string(null())``        | ``null()``           |
|                      |                           +---------------------------+----------------------+
|                      |                           | ``string(true())``        | ``'true'``           |
|                      |                           +---------------------------+----------------------+
|                      |                           | ``string(false())``       | ``'false'``          |
|                      |                           +---------------------------+----------------------+
|                      |                           | |string-from-date-in|     | ``'2010-04-15'``     |
+----------------------+---------------------------+---------------------------+----------------------+
| `length(s)`          | number of characters      | ``length('HTSQL')``       | ``5``                |
|                      | in *s*                    |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `x + y`              | concatenate *x* and *y*;  | ``'Hello' + ' World'``    | ``'Hello World'``    |
|                      | treats nulls as empty     +---------------------------+----------------------+
|                      | strings                   | ``'Hello' + null()``      | ``'Hello'``          |
|                      |                           |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `x ~ y`              | *x* contains *y*;         | ``'HTSQL' ~ 'sql'``       | ``true()``           |
|                      | case-insensitive          |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `x !~ y`             | *x* does not contain      | ``'HTSQL' !~ 'sql'``      | ``false()``          |
|                      | *y*; case-insensitive     |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `head(s)`            | first character of *s*    | ``head('HTSQL')``         | ``'H'``              |
+----------------------+---------------------------+---------------------------+----------------------+
| `head(s,n)`          | first *n* characters      | ``head('HTSQL',2)``       | ``'HT'``             |
|                      | of *s*                    +---------------------------+----------------------+
|                      |                           | ``head('HTSQL',-3)``      | ``'HT'``             |
+----------------------+---------------------------+---------------------------+----------------------+
| `tail(s)`            | last character of *s*     | ``tail('HTSQL')``         | ``'L'``              |
+----------------------+---------------------------+---------------------------+----------------------+
| `tail(s,n)`          | last *n* characters       | ``tail('HTSQL',3)``       | ``'SQL'``            |
|                      | of *s*                    +---------------------------+----------------------+
|                      |                           | ``tail('HTSQL',-2)``      | ``'SQL'``            |
+----------------------+---------------------------+---------------------------+----------------------+
| `slice(s,i,j)`       | *i*-th to *j*-th          | ``slice('HTSQL',1,4)``    | ``'TSQ'``            |
|                      | characters of *s*; null   +---------------------------+----------------------+
|                      | or missing index means    | ``slice('HTSQL',-4,-1)``  | ``'TSQ'``            |
|                      | the beginning or the end  +---------------------------+----------------------+
|                      | of the string             | |slice-start-in|          | ``'HT'``             |
|                      |                           +---------------------------+----------------------+
|                      |                           | |slice-end-in|            | ``'SQL'``            |
+----------------------+---------------------------+---------------------------+----------------------+
| `at(s,k)`            | *k*-th character of *s*   | ``at('HTSQL',2)``         | ``'S'``              |
+----------------------+---------------------------+---------------------------+----------------------+
| `at(s,k,n)`          | *n* characters of *s*     | ``at('HTSQL',1,3)``       | ``'TSQ'``            |
|                      | starting with *k*-th      +---------------------------+----------------------+
|                      | character                 | ``at('HTSQL,-4,3)``       | ``'TSQ'``            |
|                      |                           +---------------------------+----------------------+
|                      |                           | ``at('HTSQL,4,-3)``       | ``'TSQ'``            |
+----------------------+---------------------------+---------------------------+----------------------+
| `upper(s)`           | upper case of *s*         | ``upper('htsql')``        | ``'HTSQL'``          |
+----------------------+---------------------------+---------------------------+----------------------+
| `lower(s)`           | lower case of *s*         | ``lower('HTSQL')``        | ``'htsql'``          |
+----------------------+---------------------------+---------------------------+----------------------+
| `trim(s)`            | strip leading and         | ``trim('  HTSQL  ')``     | ``'HTSQL'``          |
|                      | trailing spaces from *s*  |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `ltrim(s)`           | strip leading spaces      | ``ltrim('  HTSQL  ')``    | ``'HTSQL  '``        |
|                      | from *s*                  |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `rtrim(s)`           | strips trailing spaces    | ``rtrim('  HTSQL  ')``    | ``'  HTSQL'``        |
|                      | from *s*                  |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `replace(s,x,y)`     | replace all occurences    | |replace-in|              | ``'HTRAF'``          |
|                      | of *x* in *s* with *y*;   +---------------------------+----------------------+
|                      | in *s* with *y*; null *x* | |replace-null-in|         | ``'HTSQL'``          |
|                      | is treated as an empty    |                           |                      |
|                      | string                    |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+

.. |string-from-date-in| replace:: ``string(date('2010-04-15'))``
.. |slice-start-in| replace:: ``slice('HTSQL',null(),2)``
.. |slice-end-in| replace:: ``slice('HTSQL',2,null())``
.. |replace-in| replace:: ``replace('HTSQL','SQL','RAF')``
.. |replace-null-in| replace:: ``replace('HTSQL',null(),'RAF')``


Date Functions
==============

+----------------------+---------------------------+---------------------------+----------------------+
| Function             | Description               | Example Input             | Output               |
+======================+===========================+===========================+======================+
| `date(x)`            | cast *x* to date          | ``date('2010-04-15')``    |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `date(yyyy,mm,dd)`   | date *yyyy-mm-dd*         | ``date(2010,4,15)``       | |date-out|           |
|                      |                           +---------------------------+----------------------+
|                      |                           | ``date(2010,3,46)``       | |date-out|           |
|                      |                           +---------------------------+----------------------+
|                      |                           | ``date(2011,-8,15)``      | |date-out|           |
+----------------------+---------------------------+---------------------------+----------------------+
| `today()`            | current date              | ``today()``               |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `year(d)`            | year of *d*               | |year-in|                 | ``2010``             |
+----------------------+---------------------------+---------------------------+----------------------+
| `month(d)`           | month of *d*              | |month-in|                | ``4``                |
+----------------------+---------------------------+---------------------------+----------------------+
| `day(d)`             | day of *d*                | |day-in|                  | ``15``               |
+----------------------+---------------------------+---------------------------+----------------------+
| `d + n`              | increment *d* by *n* days | |date-inc-in|             | |date-out|           |
+----------------------+---------------------------+---------------------------+----------------------+
| `d - n`              | decrement *d* by *n* days | |date-dec-in|             | |date-out|           |
+----------------------+---------------------------+---------------------------+----------------------+
| `d1 - d2`            | number of days between    | |date-diff-in|            | ``13626``            |
|                      | *d1* and *d2*             |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+

.. |date-out| replace:: ``date('2010-04-15')``
.. |year-in| replace:: ``year(date('2010-04-15'))``
.. |month-in| replace:: ``month(date('2010-04-15'))``
.. |day-in| replace:: ``day(date('2010-04-15'))``
.. |date-inc-in| replace:: ``date('1991-08-20')+6813``
.. |date-dec-in| replace:: ``date('2028-12-09')-6813``
.. |date-diff-in| replace:: ``date('2028-12-09')-date('1991-08-20')``


Aggregate Functions
===================

+----------------------+---------------------------+---------------------------+----------------------+
| Function             | Description               | Example Input             | Output               |
+======================+===========================+===========================+======================+
| `exists(ps)`         | *TRUE* if *ps* contains   | |exists-in|               |                      |
|                      | at least one *TRUE*       |                           |                      |
|                      | value; *FALSE* otherwise  |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `every(ps)`          | *TRUE* if *ps* contains   | |every-in|                |                      |
|                      | only *TRUE* values;       |                           |                      |
|                      | *FALSE* otherwise         |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `count(ps)`          | number of *TRUE* values   | |count-in|                |                      |
|                      | in *ps*                   |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `min(xs)`            | smallest *x* in *sx*      | ``min(course.credits)``   |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `max(xs)`            | largest *x* in *sx*       | ``max(course.credits)``   |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `sum(xs)`            | sum of *x* in *xs*        | ``sum(course.credits)``   |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `avg(xs)`            | average value of *x*      | ``avg(course.credits)``   |                      |
|                      | in *xs*                   |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+

.. |exists-in| replace:: ``exists(course.credits>5)``
.. |every-in| replace:: ``every(course.credits>5)``
.. |count-in| replace:: ``count(course.credits>5)``


Navigation Operations
=====================

+----------------------+---------------------------+---------------------------+----------------------+
| Function             | Description               | Example Input             | Output               |
+======================+===========================+===========================+======================+
| `chain . link`       | traverse a link           | ``school.program``        |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `chain . attr`       | extract attribute value   | ``school.name``           |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `chain . \*`         | extract all attributes    | ``school.*``              |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `chain ? p`          | records from *chain*      | ``school?code='edu'``     |                      |
|                      | satisfying condition *p*  |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `chain.sort(x,...)`  | records from *chain*      | ``course.sort(credits-)`` |                      |
|                      | sorted by *x*, ...        |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `chain.limit(n)`     | first *n* records from    | ``course.limit(10)``      |                      |
|                      | *chain*                   |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `chain.limit(n,k)`   | *n* records from *chain*  | ``course.limit(10,20)``   |                      |
|                      | starting from *k*-th      |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `chain {x,...}`      | select *x*, ... from      | ``school{code,name}``     |                      |
|                      | *chain*                   |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `root()`             | scalar class              |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `this()`             | current chain             |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+


Decorators
==========

+----------------------+---------------------------+---------------------------+----------------------+
| Function             | Description               | Example Input             | Output               |
+======================+===========================+===========================+======================+
| `as(x,title)`        | set the column title      | ``number :as 'No.'``      |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `x+`                 | sort by *x* in            | ``credits+``              |                      |
|                      | ascending order           |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `x-`                 | sort by *x* in            | ``credits-``              |                      |
|                      | descending order          |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+


Formatters
==========

+----------------------+---------------------------+---------------------------+----------------------+
| Function             | Description               | Example Input             | Output               |
+======================+===========================+===========================+======================+
| `/:html`             | HTML tabular output       |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `/:txt`              | plain text tabular output |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `/:csv`              | CSV (comma-separated      |                           |                      |
|                      | values) output            |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+
| `/:json`             | JSON-serialized output    |                           |                      |
+----------------------+---------------------------+---------------------------+----------------------+


.. vim: set spell spelllang=en textwidth=72:
