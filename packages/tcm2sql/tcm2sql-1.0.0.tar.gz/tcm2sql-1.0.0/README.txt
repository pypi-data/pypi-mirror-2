=========
 tcm2sql
=========


What is this?
=============

tcm2sql is a tool for generating SQL commands from a tcm static
structure diagram (SSD). It was developed by Christian Zagrodnick for
gocept to generate some large PostgreSQL databases out of diagrams.

This diagram type is normally used for object structures in UML. If you are
familliar with the UML notation, you should get the tcm2sql conventions
fairly fast into your brain.

Renderers can be plugged in to tcm2sql quite easy. Currently there is only
a renderer for PostgreSQL. It creates PostgreSQL compatible `create table`
and related queries. The documentation is mostly based on PostgreSQL terms.
There is a section which deals with other renderers.

In prior versions there were also:

    * DBObjects -- for creating some code which might be useful if you are using DBObjects.

    * Prolog -- for creating Prolog terms.

Those have been removed because of vast changes in tcm2sql's internal API
and no actualy need for them. If you like to see those or others please
contact me.

There is also a mode for generating the difference between two SSDs. This
allows to semi automatic updating of databases.

TCM can be obtained from `University of Twente`_. There is versionavailable
on Debian, too.

Thanks to Christian Theune for reviewing the documentation.


The conventions
===============

You might want to open an `Example*.ssd` in the `doc` directory of this
package.

`Double Class Boxes` and `Triple Class Boxes` are used for tables.
As in UML the top is for the name, the middle for the attributes. The
bottom part is used for constraints in tcm2sql.

Name
----

The name is just passed to the `create table <name>`.

Attributes
----------

Basically an attribute definition looks like:

	<AttributeName>: <Datatype>

i.e.

	title: varchar(32)

Row constraints are just written after the datatype:

	name: varchar(64) not null


So far so good. But there also are a few special characters:

	``#`` -- marks one more more columns as the PRIMARY KEY

	``~`` -- marks a column as a FOREIGN KEY

	``-`` -- marks a column as private

i.e.

	#id: serial

defines a single row primary key, whereas

	#~foo: integer

	#~bar: integer

defines a double row PRIMARY KEY, while simultaneously marking
them as two FOREIGN KEYs.

So the whole attribute definition looks like this:

<Attribute> ::=
	["#"]{0,1}["~"]{0,1}<AttributeName>: <Datatype> <RowConstraint>



Constraints
===========

As stated above, what the operations are in UML, are the
constraints in tcm2sql.

Constraints have a similar definition as attributes:

<Constraint> ::= <ConstraintName>: <ConstraintOperation>

For example:

	invalidFoo: check (foo>47)
	dupeFooBar: unique (foo,bar)

To avoid very large boxes in the diagram you also have the
possibilty to add constraints using the annotation of your table.
It then has to be prefixed by an questionmark (?). Since tcm has
no indicator for boxes which have an annotation you might write
`<ext>` as constraint, which is just ignored and is a good remember for
yourself.

<Constraints> ::= [[<Constraint>|"<ext>"]\n]*


Relations
=========

In UML there are different types of relations between classes,
which I tried to adapt to PostgreSQL.

Implemented in tcm2sql:

	* Aggregation (white diamond)

		results in an `on delete set null`

		The diamond has to be connected to the table
		with the referenced PRIMARY KEY.

	* Composition (black diamond)

		results in an `on delete cascade on update cascade`

		The diamond has to be connected to the table
		with the referenced PRIMARY KEY.

	* Generalisation (arrow)

		results in `inherits (foo)` See `PostgreSQL documentation`_ for
		details.

		The parent table is where the arrow points to.

	* Binary relationship

		results in an ordinary relation between two
		tables.

		You have to write a 1 on *one* end in the
		cardinality field. This is where die PK resides.


So what's the ~ for?

	Within a table every FOREIGN KEY has to be prefixed with
	the ~. There are two ways for assigning a row to a
	relation.

	1. Write the FK's name as ROLE on the relation.

	2. Name it <Othertable>_<OthertablePK>

How to reference a composite primary key?

    Make a single relation between the tables and put the
    names of the foreign keys komma separated into the "role
    name" of the foreign key side of the relation.


Views and Private Attributes
============================

    For every table a view `sv<TableName>` is created with only public
    attributes.  If you need access to the database with ODBC but cannot
    allow access to all attributes you just mark the private attributes
    with `-` and let ODBC only access the views.


The modes
=========


Create Mode
-----------

Usage: bin/tcm2sql -n <file.ssd> ...

Generates a full sql file (actualy it prints to stdout) with the
necessary `CREATE TABLE` commands. The constraints  are added
afterwards, since this is much easier.

Diff Mode
---------

Usage: bin/tcm2sql -o <old.ssl> -n <new.ssd> ...

Generates sql wich does the following:

	- copy data to temporary tables
	- drop tables
	- create new tables
	- drop sequences of deleted tables
	- create sequences for new tables
	- copy data back


The diff mode seems to work pretty well, but please ensure you
have a recent backup.


Using multiple ssd files to create a single database
====================================================

As the database grows you get more and more junctions. Furthermore tcm
allows only six pages which become full.  To avoid both problems you can
split your database into several files.

The file you pass as parameter to tcm2sql is started with. To have a
connection to another ssd file you create a class node with a stereotype.
The stereotype is the relative (to the master ssd) or absolute file name of
the ssd to be included. The table name references the actual table in the
included ssd. See ExampleInclude*.ssd for an expamle.

It is possible to build include circles and including forth and back
without any problem.


Examples
========

There are two example ssds, just try tcm2sql on them.

References
==========

.. _`PostgreSQL documentation`: http://www.postgresql.org/idocs/index.php?inherit.html

.. _`University of Twente`: http://wwwhome.cs.utwente.nl/~tcm/


