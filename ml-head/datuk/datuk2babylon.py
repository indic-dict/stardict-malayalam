# -*- coding: utf-8 -*-
'''
License: GNU GPLv3
	Kailash Nadh, http://nadh.in for datuk corpus and DatukParser class.
'''
from __future__ import unicode_literals
import codecs, sys, csv, re
from collections import namedtuple

class DatukParser:
	data = None

	def __init__(self, filename):
		"""Intitialize by loading the corpus into the memory"""

		try:
			self.data = codecs.open(filename, encoding = 'utf-8', errors = 'ignore').read()
			self.data = self.data.strip().split("\n\n")
		except Exception as e:
			print("Can't read " + filename)
			raise


	def get_all(self):
		"""Get all entries as a list"""
		entries = []

		for entry in self.iterate_all():
			entries.append(entry)

		return entries

	def iterate_all(self):
		"""Compile the line-break and tab separated records into data structures"""

		entry_head = namedtuple("Entry", "letter word origin literal id definitions")
		entry_defition = namedtuple("Definition", "type definition")
		entry = None

		# single record
		for item in self.data:
			lines = item.strip().split("\n")

			head = lines[0].split("\t") # first line is the word, type, id etc.

			if len(head) != 5:
				continue

			head = [h if h != "_" else "" for h in head]
			
			# the rest of the lines are definitions
			defns = []
			for defn in lines[1:]:
				defns.append( entry_defition( *[h if h != "_" else "" for h in  defn.strip().split("\t")] ) )

			# put it all together
			head.append(defns)
			entry = entry_head(*head)

			yield entry



if __name__ == '__main__' :
	args = sys.argv
	args_given = True
	if not args or len(args) == 1:
		args_given = False
	elif len(args)!= 4:
		sys.exit('wrong no of args given')
	
	corpusf = args[1] if args_given else 'datuk.corpus'
	tagsf = args[2] if args_given else 'tags'
	blf = args[3] if args_given else 'datuk.babylon'
	
	tagsd = {row[0].decode('utf-8') : row[-1].decode('utf-8') for row in csv.reader(open(tagsf, 'rb'), delimiter=str(u'\t').encode('utf-8'))}
	#print tagsd
	
	datuk_parser = DatukParser(corpusf)
	
	with open(blf, 'wb') as datuk_bl :
		bl_ifo = "\n#stripmethod=keep\n#sametypesequence=h\n#bookname=ദതുക് (Datuk)\n\n";
		datuk_bl.write(bl_ifo.encode('utf-8'))
		
		for entry in datuk_parser.iterate_all() :
			bl_entry = ''
			ordinal_match = re.compile(r'^(.+)([0-9]+)$').match(entry.word)
			header_line = entry.word + '|' + ordinal_match.group(1) + '\n' if ordinal_match else entry.word + '\n'
			bl_entry+= header_line
			
			descr_line = ''
			origin = '<u><i>' + entry.origin + '</i></u>' if entry.origin else ''
			descr_line+= origin
			descr_line+= '<ul style="list-style-type: none;">'
			for definition in entry.definitions :
				descr_line+= '<li>' + ('<b><small>' + definition.type + '</small></b> ' if definition.type else '') + definition.definition + '</li>'
			descr_line+= '</ul>'
			descr_line+= '\n'
			bl_entry+= descr_line
			
			empty_line = '\n'
			bl_entry+= empty_line
			
			datuk_bl.write(bl_entry.encode('utf-8'))



