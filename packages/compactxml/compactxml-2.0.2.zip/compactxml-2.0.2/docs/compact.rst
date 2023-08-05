===========
Compact XML
===========

--------
Overview
--------

Compact XML is an alternative syntax for representing XML files. It uses
indentation to indicate nesting to give a python like feel, XPath based
prefixes to identify nodes, and has a macro system to shorten common XML
constructs. It is intended for writing element based XML files, especially
those where the XML elements share a common structure, such as XSLT files.

It is not well suited for markup based XML files, such as XHTML files, where
element nesting is less important.

--------
Tutorial
--------

Familiarity with XML is assumed.

Compact XML uses a simple line based syntax for representing XML. The simplest
XML document is a single element::

	Compact XML:

	<root

	Equivalent in XML:

	<root/>

Compact XML identifies each line by its prefix. Notice that the ``<`` prefix
is used to indicate that the line is an element, which is then followed by the
name of the element. Since the tag is not closed, this immediately leads to
nesting elements::

	Compact XML:

	<root
		<one
		<two
		<three

	Equivalent in XML:

	<root><one/><two/><three/></root>

Compact XML uses indentation to indicate nesting, similar to the python
programming language. Such leading whitespace is used only to determine
nesting, and is not considered part of the XML. To add whitespace, or any
other textual data to an element, use the ``"`` prefix::

	Compact XML:

	<root
		"Hello, world.

	Equivalent in XML:

	<root>Hello, world.</root>

Notice that text is indented just like elements are to show which element
contains the text. Notice the difference::

	Compact XML:

	<root
		<nested
		"One
		<nested
		"Two

	Equivalent in XML:

	<root><nested/>One<nested/>Two</root>

Versus::

	Compact XML:

	<root
		<nested
			"One
		<nested
			"Two

	Equivalent in XML:

	<root><nested>One</nested><nested>Two</nested></root>

Whitespace after the prefix is significant, and will show up in the XML.
However, things like trailing spaces can be difficult to see::

	Compact XML:

	<root
		" Hello, world. 

	Equivalent in XML:

	<root> Hello, world. </root>

Because of this, you can also quote the value, using either single(``'``) or
double(``"``) quotes to quote a single line. So, the previous example can be
shown more clearly as::

	Compact XML:

	<root
		"' Hello, world. '

	Equivalent in XML:

	<root> Hello, world. </root>

What about when we need to include a quote in a quoted value? Compact XML uses
a simple escaping rule, just double whichever quote character you're using::

	Compact XML:

	<root
		"' It''s a small world. '

	Equivalent in XML:

	<root> It's a small world. </root>

Now, to include a new line in a text value, use a continuation. Values can be
continued on to the next line using the ``\`` or ``+`` continuation. With the
``\`` continuation, a newline is added, with the ``+`` continuation the text
values are simply concatenated unmodified. Continuations must be indented to
the same level as the line they are continuing::

	Compact XML:

	<root
		"
		\Hello,
		\World.
		\

	Equivalent in XML:

	<root>
	Hello,
	World.
	</root>

Both names and values can be continued, but names can not use the ``\``
continuation, as names do not allow for whitespace. To illustrate, this is an
overly verbose way to specify the same thing as the previous example::

	Compact XML:

	<
	+r
	+o
	+o
	+t
		"
		\
		+H
		+e
		+l
		+l
		+o
		+,
		\World.
		\

	Equivalent in XML:

	<root>
	Hello,
	World.
	</root>

This is of course, ridiculous. Use the ``+`` continuation for formatting when
you have a very long line and use the ``\`` continuation when you want to
insert a new line.

Let's look at the last fundamental type of XML node, attributes. Attributes
are specified using the ``@`` prefix::

	Compact XML:

	<root
		@message=Hello, world.

	Equivalent in XML:

	<root message="Hello, world."/>

Remember value quoting? You can quote attribute values, but it's not required.
The only special rule is that whitespace between the equals sign and the start
of the attribute value is ignored, so the value will need to be quoted to
include whitespace at the start of an attribute value::

	Compact XML:

	<root
		@message=" Hello, world. "

	Equivalent in XML:

	<root message=" Hello, world. "/>

There is a special short form for attributes, that allows them to be included
in-line on the element statement. Quoting is also important here, as it's the
only way to include in-line attribute values with whitespace::

	Compact XML:

	<root @message="Hello, world."

	Equivalent in XML:

	<root message="Hello, world."/>

Notice that the ``@`` prefix may still be included for in-line attributes, but
that it can be omitted::

	Compact XML:

	<root message="Hello, world."

	Equivalent in XML:

	<root message="Hello, world."/>

Namespaces are fully supported by compact XML. A namespace prefix can be
declared using the standard XML attribute::

	Compact XML:

	<test:root
		@xmlns:test=uri:testns

	Equivalent in XML:

	<test:root xmlns:test="uri:testns"/>

However, there's no need to use the long form. The ``#`` prefix can be used to
define a namespace prefix like so::

	Compact XML:

	<test:root
		#test=uri:testns

	Equivalent in XML:

	<test:root xmlns:test="uri:testns"/>

Namespaces work like attributes, and can be declared as either stand alone
statements or in-line::

	Compact XML:

	<test:root #test=uri:testns

	Equivalent in XML:

	<test:root xmlns:test="uri:testns"/>

Declaring default namespaces is just as simple::

	Compact XML:

	<root
		#uri:testns

	Equivalent in XML:

	<root xmlns="uri:testns"/>

That covers all the basic statement types. See the reference documentation for
details on the less common nodes; comments(``!``), processing
instructions(``<?``), and document type declarations(``<!``).

There is another class of statement that begins with the ``?`` prefix. These
are commands for the compact XML converter, and do not directly correspond to
XML nodes. We'll take a look at some of the more common ones. First is
``?default``, which sets a default attribute value. When working with a
document that has many common attribute values, it can help to set this value.
Then, when an attribute is given with no value, the default is used instead::

	Compact XML:

	?default True
	<root @flag

	Equivalent in XML:

	<root flag="True"/>

If no default has yet been set, the value of the flag attribute would be an
empty string::

	Compact XML:

	<root @flag

	Equivalent in XML:

	<root flag=""/>

If a single default isn't enough, variables can be defined using the
``?variable`` statement. This sets a variable value that is global to the
document. To use the value of a variable, use the ``$`` variable continuation.
The variable continuation is similar to the ``+`` continuation, but instead of
inserting a literal value, inserts the value of the named variable::

	Compact XML:

	?variable value=True
	<root
		@flag=
		$value

	Equivalent in XML:

	<root flag="True"/>

Now, the interesting thing about variable evaluation is, if the variable
hasn't been defined, the statement is omitted from the output XML. This can be
used to conditionally include XML parts::

	Compact XML:

	?variable exists=
	<root
		<one
		$exists
		<two
		$does-not-exist

	Equivalent in XML:

	<root><one/></root>

Notice that the ``two`` element is omitted from the XML.

This may seem unnecessary, but is a useful part of defining macros. Element
macros use variables in a very similar way. Say you've got a very repetitive
XML file::

	<root>
		<item name="first" description="stuff" available="True"/>
		<item name="second" description="thingy" available="True"/>
		<item name="third" description="other" available="False"/>
	</root>

You can define an element macro using the ``?element`` command to include the
common parts::

	Compact XML:

	?element item
		@name
		@description
		@available=True
		<item
			@name=
			$name
			@description=
			$description
			@available=
			$available
			?contents
	<root
		item first stuff
		item @name=second @available=thingy
		item third other False

	Equivalent in XML:

	<root><item name="first" description="stuff" available="True"/><item
	name="second" description="thingy" available="True"/><item
	name="third" description="other" available="False"/></root>

Let's take a look at each part of the macro. First, we have the ``?element``
command. All element macro definitions should occur before the document
starts. The ``?element`` command is followed by the name of the macro to
create, in this case ``item``.

Next is a list of attribute values, describing the parameters the macro
accepts. If a value is given, it's used as the default value for the parameter
if it is not passed. Here, only the ``available`` parameter has a default
value, the others must be passed to the macro. The order the parameters are
defined in is important, as values can be passed to the macro both by position
and by name.

Then we have the actual element node that will be inserted for the macro:
``<item``. Next, each of the parameters we created are used as the values for
a similarly named attribute. Note that the same variable continuation syntax
is used for parameters, and the variable name corresponds to the name of the
defined parameter.

Last, we see the special element macro only command ``?contents``. This is a
placeholder value for any extra macro contents that aren't part of a
parameter. Here, it's unused as the ``<item/>`` element is empty.

In the next section, we see where the macro is called. The first uses
positional parameters, in the same order as the parameters were defined.
Notice, since the parameter values don't have spaces, there's no need to quote
them.

The second uses named parameters. Both positional and named parameters can be
used in the same macro call.

Finally, the third uses positional parameters, and overrides the default value
used for the ``available`` parameter.

Remember when we were talking about undefined variables being useful for
element macros? This behaviour can be used to omit parts of the element macro
based on the parameters that are passed. For instance::

	Compact XML:

	?element item
		@name
		@description
		@available=True
		<item
			@name=
			$name
			@description=
			$description
			@available=
			$available
			?contents
	<root
		item first @avaliable=False

	Equivalent in XML:

	<root><item name="first" available="False"/></root>

Notice how the ``description`` attribute just disappears when no value is
given for the description parameter.

There is a different attribute group macro available for working with
attributes.  The ``?attribute`` command defines such an attribute group.
Attribute group macros do not take parameters, only a group of attributes and
namespaces. Attribute groups are used with the ``@@`` prefix::

	Compact XML:

	?attribute grouped
		@message=Hello, world.
		@type=Greeting
	<root
		@@grouped

	Equivalent in XML:

	<root message="Hello, world." type="Greeting"/>

Attribute group statements can be used just like attributes, either in-line or
as a standalone statement.

That's all the major features of compact XML, you should be ready to start
writing!

------
Syntax
------

Compact XML uses a prefix based syntax, with each line generally comprising a
statement and each statement corresponding to a specific XML node. Statements
are comprised of a prefix followed by one or more expressions, and are usually
in one of the following three forms::

	prefix [name expression]
	prefix [value expression]
	prefix [name expression] = [value expression]

Some statements, such as those representing XML elements allow nesting. The
indentation of each line is used to indicate nesting, and is always
significant.

Whitespace is significant throughout, with leading indentation used to
indicate nesting, and other whitespace being considered to be part of data
wherever applicable. Quoting is optional, and is only needed when it is
necessary to resolve ambiguity.

Most parser commands, those statements starting with ``?``, must appear
at the beginning of the document; The exceptions being ``?default`` and
``?variable`` commands. Remaining document structure must follow XML form,
with a single optional document type declaration at the beginning of the
document and a required single root element or element macro. As with XML,
comments and processing instructions may exist before or after the root
element.

-----------
Expressions
-----------

Statements in compact XML are built from three kinds of expressions. There are
name expressions for XML names or internal names, value expressions for
everything else, and in-line expressions for brevity. Expressions always
evaluate to a single text value.

Literals
--------
All literal values are text values which span until the end of the line
(non-inclusive). Literals may contain other whitespace depending on the
context.

Names
-----
Names follow the restrictions for XML names, and are used for both XML names
and for compact XML identifiers. This means they can not contain whitespace
and are limited to alphanumeric characters and three allowed punctuation
characters; dash (``-``), underscore (``_``), and period (``.`` ).

Continuations
-------------
Name or value expressions may be continued over several lines using one of the
special continuation prefixes on the following line. Continuations must be
indented to the same level as the line they are continuing.

The simplest is the addition continuation, which is prefixed with a plus sign
(``+``). This simply continues the name or value onto the next line adding its
literal value.

Next there is the newline continuation, which is prefixed with a backslash
(``\``). Then newline continuation is only valid for value expressions, as it
inserts a new line before appending its literal value. As names can not
contain whitespace such as new lines, it is disallowed in name expressions.

Finally there is the variable continuation, which is prefixed with a dollar
sign (``$``). It is replaced by a variable value as defined for the name
specified.  If the variable is not defined, the whole expression is ignored.
Variable values can be defined globally as with the ``?variable`` command, or
inside element macros by parameters.

Value Expressions
-----------------
Values are used for arbitrary text, and can include whitespace and new lines.
Whitespace is significant and is included in the value no matter where it
occurs, with the special case that whitespace after an '=' sign in name/value
pairs is ignored.

The components of value expressions can be either unquoted or quoted with
either single quotes (``'``) or double quotes (``"``). The entire value is
either quoted or not, depending on if the first non-whitespace character
encountered is a quote. If a quote is found in an unquoted component, it is
used as is, and has no special meaning. Quotes in quoted literals can be
escaped by doubling the quote, as in ``''`` or ``""``.

Name Expressions
----------------
Names are used for XML names and internal compact XML names. Names can not
contain whitespace, and as such it is ignored in name expressions. Due to
this, name expression literals can't be quoted as there is no reason to do so.

In-Line Expressions
-------------------
Attributes, attribute groups and namespace declarations can also be given
in-line on element statements. In-line expressions follow the same content
rules, however as in-line expressions are separated by whitespace, in-line
values must be quoted if they contain whitespace.

In-Line expressions can not be continued. Use the statement form if
continuations are needed.

----------
Statements
----------

A statement in compact XML is a single indented line. The line may be
continued if one of the contained expressions uses one or more continuation
prefixes on the following lines ( ``+``, ``\``, or ``$`` ).

Indentation indicates nesting. Only element macro definitions, attribute macro
definitions, elements and element macros may have nested statements indented
under them. Tabs are always treated as 8 spaces. Mixing of tabs and spaces for
indentation is discouraged, and can create confusion between lines that look
identical in a text editor, but are parsed differently.

Statements are identified by prefix, and are as follows:

:No Prefix:
	`Element Macro`_
:<:
	Element_
:":
	Text_
:@:
	Attribute_
:@@:
	`Attribute Group`_
:#:
	Namespace_
:!:
	Comment_
:<?:
	`Processing Instruction`_
:<!:
	`Document Type Declaration`_
:?attribute:
	`Attribute Group Definition Command`_
:?contents:
	`Contents Command`_
:?default:
	`Default Attribute Value Command`_
:?element:
	`Element Macro Definition Command`_
:?encoding:
	`Encoding Command`_
:?indent:
	`Indent Command`_
:?load:
	`Load Command`_
:?variable:
	`Variable Command`_

.. _element:
.. _elements:

Element (``<``)
---------------
XML elements are prefixed with ``<``, followed by the name of the element as a
name expresssion.  Elements with a namespace are specified as normal for xml
with the prefix followed by a colon, then the remainder of the name. Nodes
contained within an element are indicated by indenting the contained nodes. 

Both namespace and attribute statements can be nested as child elements or
in-line following the element name. If in-line the ``@`` can optionally be
omitted for attribute statements.

Namespace prefixes must be declared before they can be used, either globally
to the compact XML parser or by an explicit namespace declaration. As with
XML, namespaces declared on the element can be used by the element

For example, here are three nested elements::

	Compact XML:

	<one
		<two
			<three


	Equivalent in XML:

	<one><two><three/></two></one>

.. _`element macro`:
.. _`element macros`:

Element Macro (``No Prefix``)
------------------------------
Element macros must first be defined by an ``?element`` `element macro
definition command`_. Attributes defined on the element macro will be used as
parameters for the macro. Parameters may be passed by position or by name.

Positional parameters require no prefix, and can only be passed in-line. Named
parameters and other attributes require the ``@`` prefix, even when passed
in-line, to disambiguate them from positional parameters.

Extra parameters and any nested statements are passed to the macro, and are
available using the ``?contents`` `contents command`_. An element macro will
expand to one or more XML elements.

For details on creating and using macros, see the macros_ section.

.. _attribute:
.. _attributes:

Attribute (``@``)
------------------
XML attributes are prefixed with ``@`` and must appear as the child of an
element or element macro They consist of a name expression, followed by and
optional ``=`` sign and value expression.

If no value expression is given, the attribute will have the current default
attribute value as set by the ``?default`` `default attribute value command`_.

Named parameters are passed to `element macros`_ as attribute values.

For example, here is a single element with an attribute value::

	Compact XML:

	<one
		@name=value

	Or:

	<one @name=value

	Or:

	<one name=value

	Equivalent in XML:

	<one><two><three/></two></one>

.. _`attribute group`:
.. _`attribute groups`:

Attribute Group (``@@``)
------------------------
Attribute groups must first be defined by an ``?attribute`` `attribute group
definition command`_. Once defined, they are included with the ``@@`` prefix
followed by the macro name as a name expression.

Unlike `element macros`_ attribute groups do not have parameters or contents.

See the macros_ section for more details on creating and using attribute
groups.

.. _namespace:
.. _namespaces:

Namespace (``#``)
------------------
XML namespace declarations are prefixed with ``#`` and must appear as the
child of an element or element macro. Namespaces are declared by a prefix name
as a name expression, followed by ``=``, and a value expression declaring the
namespace URI.

Namespace declarations are equivalent to an explicit namespace declaration
done with an attribute, in the ``xmlns`` namespace.

For example, here is an element declared in a namespace::

	Compact XML:

	<test:a
		#test=http://www.testuri.com

	Or:

	<test:a #test=http://www.testuri.com

	Or:

	<test:a @xmlns:test=http://www.testuri.com

	Equivalent in XML:

	<test:a xmlns:test="http://www.testuri.com"/>

Optionally, a default namespace can be declared as a stand alone value
expression. Remember to quote the value expression if it contains an ``=``
sign. For example::

	Compact XML:

	<a
		#http://www.testuri.com

	Or:

	<a #http://www.testuri.com

	Or:

	<a @xmlns=http://www.testuri.com

	Equivalent in XML:

	<a xmlns="http://www.testuri.com"/>

.. _text:
.. _texts:

Text (``"``)
------------
Text is prefixed with ``"`` followed by a value expression.

For example, here is a multi-line text value::

	Compact XML:

	<a
		"Line one.
		\Line two.
		\Line three.

	Equivalent in XML:

	<a>Line one.
	Line two.
	Line three.</a>

.. _comment:
.. _comments:

Comment (``!``)
---------------
Comments are prefixed with ``!`` followed by a value expression.

For example, here is a multi-line comment::

	Compact XML:

	!Line one.
	\Line two.
	\Line three.

	Equivalent in XML:

	<!--Line one.
	Line two.
	Line three.-->

.. _`processing instruction`:
.. _`processing instructions`:

Processing Instruction (``<?``)
-------------------------------
Processing instructions are prefixed with ``<?`` followed by a target as a
name expression, an ``=`` sign, and a value expression for the body of the
instruction. Notice the required ``=`` sign, unlike XML. It will not appear in
the output document.

For example, here is a simple processing instruction::

	Compact XML:

	<?target=instruction

	Equivalent in XML:

	<?target instruction?>

.. _`document type declaration`:
.. _`document type declarations`:

Document Type Declaration (``<!``)
----------------------------------
Document type declarations are prefixed with ``<!`` followed by ``DOCTYPE`` and
a value expression specifying the rest of the document type as required by
XML.

Document type definition can only be specified at the top level of the
document, and only one is allowed per document. A document type declaration is
not required, however.

Due to limitations in the lxml library used, when compacting XML to compact
XML format, inline DTD definitions in DOCTYPE declarations are lost.

For example, the standard XHTML doctype declaration looks like this::

	Compact XML:

	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	\"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"
	<html

	Equivalent in XML:

	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
	<html/>

.. _`attribute group definition command`:
.. _`attribute group definition commands`:

Attribute Group Definition Command (``?attribute``)
---------------------------------------------------
The attribute group definition command is used to create an attribute group.
It expects a name literal to define the attribute group.

Any number of attributes or namespace declarations may be nested under the
command, and become part of the group. The group can be included in an element
or element macro using an `attribute group`_.

A simple attribute group would look like::

	Compact XML:

	?attribute common
		@one=1
		@two=2
		@three=3
	<root
		@@common

	Or:

	<root @@common

	Equivalent in XML:

	<root one="1" two="2" three="3"/>

Attribute groups must be defined at the beginning of a compact XML document,
before any XML elements are created.

See the macros_ section for further details.

.. _`contents command`:
.. _`contents commands`:

Contents Command (``?contents``)
--------------------------------
The contents command is used only within `element macro definition commands`_
to show where extra contents passed to the element macro should be inserted.
By default, all contents will be inserted at the location of the command,
however the contents can be filtered to include only statements of a
particular type. To do so, give the prefix of the command type to include as
an argument, one of:

	* ``<``
	* ``@``
	* ``#``
	* ``"``
	* ``!``
	* ``<?``
	* ``?``

Note that attribute groups are expanded out into their component parts before
being filtered by the contents command.

Here is a simple macro demonstrating filtered contents::

	Compact XML:

	?element filtered
		<root
			<attributes
				?contents @
			<elements
				?contents <
	filtered
		!A comment.
		@one=1
		@two=2
		<nested

	Equivalent in XML:

	<root><attributes one="1" two="2"/><elements><nested/></elements></root>

Notice that the comment is ignored, and that the element and attribute
statements are included in differing spots based on the contents filters. See
the macros_ section for further details on using element macros.

.. _`default attribute value command`:
.. _`default attribute value commands`:

Default Attribute Value Command (``?default``)
----------------------------------------------
This command sets the default attribute value used when no value is given for
an attribute_ statement. It takes a value expression that sets that default
value. If no default has been set using ``?default``, the default attribute
value is an empty (0-length) string.

Unlike most other commands, the default command can be used anywhere in a
document::

	Compact XML:

	root
		?default 1
		<first
			@one
		?default 2
		<second
			@two

	Equivalent in XML:

	<root><first one="1" two="2"/></root>

This can be useful to set when using an XML language that has attribute flag
values which must all be set to ``True`` or something similar.

.. _`element macro definition command`:
.. _`element macro definition commands`:

Element Macro Definition Command (``?element``)
-----------------------------------------------
The element macro definition command is used to create an element macro. It
expects a name literal to define the identifier used by the macro.

Macro parameters are defined as attribute_ statements nested under the
definition. If a value is assigned to the parameter definition, it is used as
a default value for that parameter.

The expansion itself must be an element or element macro, although it can have
any normal element contents nested underneath it.

The `contents command`_ is only used within element macro definitions, and
allows for including unparameterized data in the macro.

A simple attribute group would look like::

	Compact XML:

	?element greeting
		@message=Hello, world.
		<greeting
			@message=
			$message
			?contents
	<root
		greeting
		greeting Goodbye.

	Equivalent in XML:

	<root><greeting message="Hello, world."/><greeting message="Goodbye."/></root>

Element macros must be defined at the beginning of a compact XML document,
before any XML elements are created.

See the macros_ section for further details on creating and using element macros.

.. _`encoding command`:
.. _`encoding commands`:

Encoding Command (``?encoding``)
--------------------------------
The encoding command takes a value expression which specifies the encoding of
the output document. Note, unlike XML, this does not specify the encoding of
the compact XML file itself. Instead, compact XML files are always expected to
be in UTF-8 encoding.

The encoding command can only be given at the beginning of a compact XML
document, before any XML elements are defined.

A simple example::

	Compact XML:

	?encoding iso-8859-1
	<root

	Equivalent in XML:

	<?xml version="1.0" encoding="iso-8859-1"?>
	<root/>

.. _`load command`:
.. _`load commands`:

Load Command (``?load``)
------------------------
The load command takes a value expression specifying a file name to load
element macro definitions and attribute group definitions from. The behaviour
of the loader can be altered in the parser, if simple filenames are not
sufficient.

The file which is loaded must still be a valid compact XML file, and as such
must include the required root element even if it is never used.

External macros must be loaded at the beginning of a compact XML document,
before any XML elements are created.

.. _`indent command`:
.. _`indent commands`:

Restart Indentation Command (``?indent``)
------------------------------------------
Due to indentation based nesting, deeply nested documents can become difficult
to work with. This command, in ``?indent restart`` and ``?indent resume``
pairs, provides a workaround.  When the restart command is given, indentation
is reset to the first column, but all following statements will still be
nested under the same element as the restart command until a resume command is
encountered. At which point indentation will be reset to the previous level.

Note, due to parser limitations, the resume command must not be indented.

Here's a simple example of the syntax::


	Compact XML:

	<root
		<nested
			?indent restart
	<reset
	?indent resume
			<resume

	Equivalent in XML:

	<root><nested><reset/><resume/></nested></root>

Notice how the reset element and resume element are in the same place in the
output document.

.. _`variable command`:
.. _`variable commands`:

Variable Command (``?variable``)
--------------------------------
The variable command takes a name expression, an ``=`` sign, and a value
expression. It creates a variable with the given name, and assigns it that
value. This variable is then added to the global scope, and any expression can
access it using a ``$`` continuation.

Note that this can be used to create variables with whitespace or other
characters which are invalid for name expressions. Using such a variable value
in a name expression will trigger a run time error in the parser.

The global namespace can be shadowed in `element macro definition commands`_,
so be careful using the same names for global variables as in element macro
definitions.

Variables can be defined anywhere in the document. As with the `default
command`, execution occurs top to bottom. Any expression on a later line can
access the variable.

.. _macros:

------
Macros
------

Compact XML contains a macro syntax for defining commonly used elements and
groups of attributes. Element macros and attribute groups must be defined at
the top level of a document, before any XML nodes (including document type
definitions).

Once created, libraries of macros or groups can be kept in separate files and
loaded using the `load command`_.

Attribute Groups
----------------
Attribute groups are defined with the `attribute group definition command`_.
The declaration may contain any number of attribute (``@`` statements) or
namespace (``#`` statements) declarations.

Attribute group names may contain namespace prefixes, but they aren't attached
to a particular namespace. Instead, the prefix itself is simply part of the
name.

When an attribute group is included by a ``@@`` statement, the defined
attributes and namespaces are inserted at that location. This can be as a
child for an element or element macro, or even inside an element macro
definition.

Attribute groups can be nested to create groups of groups. Expansion of
attribute groups happens when used, not at definition.

Element Macros
--------------
Element macros are used to declare a common form for an XML element. It allows
for shortening common structures, as well as declaring attributes by
declaration position as well as by name.

Element macros are defined using the `element macro definition command`_,
followed by a macro name and a list of parameters and default values. The
definition must contain one or more elements or element macros, which will be
what the macro is actually expanded to.

Macro names may contain namespace prefixes, but they aren't attached to a
particular namespace. Instead, the prefix itself is simply part of the name.

Element macros can be used within element macro definitions, if necessary. If
an error occurs, a stack trace will be shown listing all of the element macros
involved in the expansion.

Parameters are given as `attributes`_, and may have default values. The order
parameters are defined in is important, positional parameters will be assigned
to names in this same order. When expanded, both positional and named
parameters may be passed. If both are encountered, named parameters are
applied first and positional parameters are applied to the remaining
parameters. Any extra parameters are considered attribute contents, and can be
inserted using the `contents command`_ inside the macro definition.

Each macro definition creates its own parameter namespace scope, with the
global variable scope (as created by the `variable command`_ or by the parser)
as the containing scope.

If a macro has optional parts, it's important to take advantage of the
expression variable continuation behaviour. If an expression tries to expand a
variable or parameter name that doesn't exist, the entire statement (and any
nested children of the statement the expression is a part of), will be omitted
from the output document.  If a parameter has no default value, if used as a
variable it will be considered undefined and trigger this omission behaviour.

The most common use for element macros is when dealing with an element which
has several required attributes, often with commonly used values. Macros allow
the attributes to be assigned an order, and the short positional form to be
used.

XSLT Macro Example
------------------

As a detailed example, presented here is a sample set of element macro
definitions for XSLT 1.0. The ``xsl:`` prefix is used for these macro
definitions to avoid confusion, if you never deal with namespaces this could
easily be removed for brevity. This covers the commonly used attributes, all
others must be specified by name. All elements are mapped, however.
::

	?element xsl:stylesheet
		@version=1.0
		<xsl:stylesheet
			#xsl=http://www.w3.org/1999/XSL/Transform
			@version=
			$version
			?contents
	?element xsl:include
		@href
		<xsl:include
			@href=
			$href
			?contents
	?element xsl:import
		@href
		<xsl:import
			@href=
			$href
			?contents
	?element xsl:strip-space
		@elements
		<xsl:strip-space
			@elements=
			$elements
			?contents
	?element xsl:preserve-space
		@elements
		<xsl:preserve-space
			@elements=
			$elements
			?contents
	?element xsl:template
		@match
		@name
		@priority
		@mode
		<xsl:template
			@match=
			$match
			@name=
			$name
			@priority=
			$priority
			@mode=
			$mode
			?contents
	?element xsl:apply-templates
		@select
		@mode
		<xsl:apply-templates
			@select=
			$select
			@mode=
			$mode
			?contents
	?element xsl:apply-imports
		<xsl:apply-imports
			?contents
	?element xsl:call-template
		@name
		<xsl:call-template
			@name=
			$name
			?contents
	?element xsl:namespace-alias
		@result-prefix
		@stylesheet-prefix
		<xsl:namespace-alias
			@result-prefix=
			$result-prefix
			@stylesheet-prefix=
			$stylesheet-prefix
			?contents
	?element xsl:element
		@name
		@namespace
		@use-attribute-sets
		<xsl:element
			@name=
			$name
			@namespace=
			$namespace
			@use-attribute-sets=
			$use-attribute-sets
			?contents
	?element xsl:attribute
		@name
		@namespace
		<xsl:attribute
			$@ name = @name
			$@ namespace = @namespace
			?contents
	?element xsl:attribute-set
		@name
		@use-attribute-sets
		<xsl:attribute-set
			@name=
			$name
			@use-attribute-sets=
			$use-attribute-sets
			?contents
	?element xsl:text
		@disable-output-escaping
		<xsl:text
			@disable-output-escaping=
			$disable-output-escaping
			?contents
	?element xsl:processing-instruction
		@name
		<xsl:processing-instruction
			@name=
			$name
			?contents
	?element xsl:comment
		<xsl:comment
			?contents
	?element xsl:copy
		@use-attribute-sets
		<xsl:copy
			@use-attribute-sets=
			$use-attribute-sets
			?contents
	?element xsl:value-of
		@select
		<xsl:value-of
			@select=
			$select
			?contents
	?element xsl:number
		<xsl:number
			?contents
	?element xsl:for-each
		@select
		<xsl:for-each
			@select=
			$select
			?contents
	?element xsl:if
		@test
		<xsl:if
			@test=
			$test
			?contents
	?element xsl:choose
		<xsl:choose
			?contents
	?element xsl:when
		@test
		<xsl:when
			@test=
			$test
			?contents
	?element xsl:otherwise
		<xsl:otherwise
			?contents
	?element xsl:sort
		@select
		<xsl:sort
			@select=
			$select
			?contents
	?element xsl:variable
		@name
		@select
		<xsl:variable
			@name=
			$name
			@select=
			$select
			?contents
	?element xsl:param
		@name
		@select
		<xsl:param
			@name=
			$name
			@select=
			$select
			?contents
	?element xsl:copy-of
		@select
		<xsl:copy-of
			@select=
			$select
			?contents
	?element xsl:with-param
		@name
		@select
		<xsl:with-param
			@name=
			$name
			@select=
			$select
			?contents
	?element xsl:key
		@name
		@match
		@use
		<xsl:key
			@name=
			$name
			@match=
			$match
			@use=
			$use
			?contents
	?element xsl:decimal-format
		<xsl:decimal-format
			?contents
	?element xsl:message
		@terminate
		<xsl:message
			@terminate=
			$terminate
			?contents
	?element xsl:fallback
		<xsl:fallback
			?contents
	?element xsl:output
		@method
		@indent
		@media-type
		<xsl:output
			@method=
			$method
			@indent=
			$indent
			@media-type=
			$media-type
			?contents
