Parser Python script
==================================

The file <code>process_jee_tutorial.py</code> is a simple Python3 script that takes in input a group of files grabbed from the Oracle's website using one of the following two <code>[wget](http://www.gnu.org/software/wget/manual/wget.html)</code> commands:
<pre>wget \
	--recursive \
	--no-clobber \
	--page-requisites \
	--adjust-extension \
	--convert-links \
	--domains docs.oracle.com \
	--no-parent \
	https://docs.oracle.com/javaee/7/tutorial/doc/</pre>

or:

<code>wget -r -nc -p -E -k -D docs.oracle.com -np https://docs.oracle.com/javaee/7/tutorial/doc/</code>

The output is written in the <code>output_dir</code> directory to be eventually imported in the [Sigil](https://code.google.com/p/sigil/)'s ePub project.