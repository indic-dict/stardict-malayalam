#-*-encoding=utf8-*-
from __future__ import unicode_literals
import sys
import csv, json, re


class Entry(object) :
    def __init__(self, id, en_word, pos, ml_def) :
        self.id = re.sub('[\r\n]+', ' ', id.decode('utf-8'))
        self.en_word = re.sub('[\r\n]+', ' ', en_word.decode('utf-8'))
        self.pos = re.sub('[\r\n]+', ' ', pos.decode('utf-8') if len(pos) else '-'.decode('utf-8'))
        self.ml_def = re.sub('[\r\n]+', ' ', ml_def.decode('utf-8'))
        self.isgood = re.match(r'^[a-zA-Z].*$', self.en_word)



args = sys.argv
args_given = True
if not args or len(args)==1:
    args_given = False
elif len(args)!=4 :
    sys.exit('wrong no of args given'+str(args))

csvf = args[1] if args_given else 'olam-enml.csv'
posf = args[2] if args_given else 'parts-of-speech.txt'
blf = args[3] if args_given else 'olam-enml.babylon'

posd = json.load(open(posf))
entries_map = {}
olam_reader = csv.reader(open(csvf, 'rb'), delimiter=str(u'\t').encode('utf-8'))

for row in olam_reader :
    if len(row) != 4 :
        continue
    if row[0].startswith('#') :
        continue
        
    entry = Entry(*row)
    if not entry.isgood :
        continue
        
    if entry.en_word not in entries_map :
        entries_map[entry.en_word] = {}
    
    pos_maps = entries_map[entry.en_word]
    if entry.pos not in pos_maps :
        pos_maps[entry.pos] = []
    
    pos_maps[entry.pos].append(entry.ml_def)

with open(blf, 'wb') as olam_bl :
    bl_ifo = "\n#stripmethod=keep\n#sametypesequence=h\n#bookname=ഓളം (Olam)\n\n";
    olam_bl.write(bl_ifo.encode('utf-8'))

    for en_word, pos_maps in entries_map.iteritems() :
        bl_entry = ''
        if not len(pos_maps) :
            continue
        
        bl_entry+= en_word+'\n'
        
        for pos, ml_def_list in pos_maps.iteritems() :
            if not len(ml_def_list) :
                continue
            pos_name = posd.get(pos, {'en' : '-', 'ml' : '-'})
            pos_header = '<b>' + pos_name['ml'] + '    :' + pos_name['en'] + '</b>'
            bl_entry+= pos_header
            
            bl_entry+= '<ul>'
            for ml_def in ml_def_list :
                bl_entry+= '<li>' + ml_def + '</li>'
            bl_entry+= '</ul>'
        
        bl_entry+= '\n\n'
        olam_bl.write(bl_entry.encode('utf-8'))



    
    
