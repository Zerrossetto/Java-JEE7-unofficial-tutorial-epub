#!/usr/bin/python

from os import listdir
from os.path import isfile, join, split, splitext
from html.parser import HTMLParser
from html import escape

class JavaTutParser(HTMLParser):
	"""docstring for JavaTutParserHTMLParser"""

	html_canvas = '<?xml version=\"1.0\" encoding=\"utf-8\"?>' + \
			'<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.1//EN\" ' + \
    		'\"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd\">' + \
			'<html xmlns=\"http://www.w3.org/1999/xhtml\">' + \
			'<head>' + \
			'<title></title>' + \
			'<link href=\"../Styles/javaee-darb.css\" rel=\"stylesheet\" type=\"text/css\" />' + \
			'</head>' + \
			'<body>{}</body>' + \
			'</html>'

	def __init__(self):
		super(JavaTutParser, self).__init__()
		self.recording = 0
		self.data = ''

	def handle_starttag(self, tag, attrs):
		try:
			tag_handler = getattr(self, 'handle_starttag_' + tag)
			tag_handler(attrs)
		except AttributeError:
			self.handle_starttag_default(tag, attrs)

	def handle_starttag_div(self, attrs):
		if len([(k, v) for k, v in attrs if k == 'class' and 'ind' in v]) > 0 or self.recording > 0:
			self.recording += 1
			self.handle_starttag_default('div', attrs)

	def handle_starttag_a(self, attrs):
		if self.recording > 0:
			for i in range(len(attrs)):
				if attrs[i][0] == 'href':
					splitted = attrs[i][1].split('#')
					fname = splitext(splitted[0])[0]
					section = splitted[-1]
					if fname[-3:].isnumeric():
						fname = fname[:-3]
					attrs[i] = ('href', '../Text/%s.xhtml#%s' % (fname, section))
					break
			self.handle_starttag_default('a', attrs)

	def handle_starttag_default(self, tag, attrs):
		if self.recording > 0:
			self.data += '<%s%s>' % (tag, ''.join([' %s=\"%s\"' % (k, v.encode('ascii', 'xmlcharrefreplace').decode('ascii')) for k, v in attrs]))


	def handle_endtag(self, tag):
		try:
			tag_handler = getattr(self, 'handle_endtag_' + tag)
			tag_handler()
		except AttributeError:
			self.handle_endtag_default(tag)

	def handle_endtag_div(self):
		if self.recording > 0:
			self.handle_endtag_default('div')
			self.recording -= 1
				
	def handle_endtag_default(self, tag):
		if self.recording > 0:
			self.data += '</%s>' % (tag)

	def handle_startendtag(self, tag, attrs):
		try:
			tag_handler = getattr(self, 'handle_startendtag_' + tag)
			tag_handler(attrs)
		except AttributeError:
			self.handle_startendtag_default(tag, attrs)

	def handle_startendtag_img(self, attrs):
		if self.recording > 0:
			for i in range(len(attrs)):
				if attrs[i][0] == 'src':
					src = split(attrs[i][1])[-1]
					src = '../Images/' + src
					attrs[i] = ('src', src)
					break

	def handle_startendtag_default(self, tag, attrs):
		if self.recording > 0:
			self.data += '<%s%s/>' % (tag, ''.join([' %s=\"%s\"' % (k, v.encode('ascii', 'xmlcharrefreplace').decode('ascii')) for k, v in attrs]))


	def handle_data(self, data):
		if self.recording > 0:
			self.data += data

	def handle_entityref(self, name):
		if self.recording > 0:
			self.data += '&%s;' % (name)

	def handle_charref(self, name):
		if self.recording > 0:
			self.data += '&#%s;' % (name)

	def output(self):
		return self.html_canvas.format(self.data)

if __name__ == '__main__':
	"""Before launching this script you should grab 
	   the content of the JEE tutorial website by launching the command below (wget required):

	   wget \
	   --recursive \
	   --no-clobber \
	   --page-requisites \
	   --adjust-extension \
	   --convert-links \
	   --domains docs.oracle.com \
	   --no-parent \
	   https://docs.oracle.com/javaee/7/tutorial/doc/

	   or:

	   wget -r -nc -p -E -k -D docs.oracle.com -np https://docs.oracle.com/javaee/7/tutorial/doc/"""

	base_dir = ''			# Your base directory here (remember the trailing slash)
	start_dir = ''			# Path for the grabbed input files
	output_dir = ''			# Path for the output files (directory must exist)

	start_dir = base_dir + start_dir
	output_dir = base_dir + output_dir

	files = [f for f in listdir(start_dir) if isfile(join(start_dir,f)) and not f.startswith('.') and f.endswith('.htm')]
	aggregated = dict()
	
	# Aggregating files
	for i in range(len(files)):
		fname = files[i][:-len(splitext(files[i])[-1])]
		if fname[-3:].isnumeric():
			fname = fname[:-3]
		if fname not in aggregated:
			aggregated[fname] = list()
		aggregated[fname].append(files[i])

	# Feeding the parser
	for filekey in aggregated:
		
		print('parsing %s group... ' % (filekey))
		parser = JavaTutParser()
		
		for filename in aggregated[filekey]:
			f = open(start_dir + filename, 'r')
			content = f.read()
			f.close()
			print('\tFile %s...' % (filename))
			parser.feed(content)

		f = open('%s%s.xhtml' % (output_dir, filekey), 'w')
		f.write(parser.output())
		f.close()
		print('end')