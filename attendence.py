import random, subprocess, sys, os
from civi import civicrm
import json

classes = ( ('Pre-K', ['Grade P1', 'Grade P2', 'Grade P3', 'Grade P4', 'Grade P5']),
		    ('K-4',  ['Grade K', 'Grade 1', 'Grade 2', 'Grade 3', 'Grade 4']), 
			('5-6th Grade',  ['Grade 5', 'Grade 6']), 
			('7th Grade', ['Grade 7']), 
			('OWL', ['Grade 8']), ('COA', ['COA']), ('Youth Group', ['Youth Group']) )

exe = r'dmtxwrite'

def checksum(num):
	fact = 3
	sum = 0
	for c in str(num):
		sum += int(c) * fact
		fact = 4 - fact
	return sum % 10

page_size = 18
def class_print_info(min_empties):
	groups = []
	for title, grades in classes:
		contacts = []
		for name in grades:
			v = civicrm({'entity':'Group', 'action':'get', 'title':name})
			d = json.loads(v)
			if not d['values']:
				raise Exception("There is a problem with %s group in %s" % (name, title))
				
			group_id = d['values'][0]['id']
			v = civicrm({'entity':'Contact', 'action':'get', 'group':group_id, 'rowCount':'9999', 'return.display_name':1})
			d = json.loads(v)
			for hash in d['values']:
				name = hash['display_name']
				id = hash['id']
				ck = checksum(int(id))
				txt = '%s%d' % (id, ck)
				img_file = 'static/barcodes/%s.png' % id
				if not os.path.isfile(img_file):
					subprocess.check_call("echo %s | %s -e c -o %s" % (txt, exe, img_file), shell = True)
				contacts.append((name, id, img_file))
		# Ensure we have pages of 20, and at least min_empties empty slots
		contacts = sorted(contacts)
		for i in range(0,min_empties):
			contacts.append(None)
		pages = []
		for idx in range(0, len(contacts), page_size):
			g = contacts[idx:idx+page_size]
			while len(g) < page_size:
				g.append(None)
			pages.append(g)
		groups.append( (title, pages))
	return groups
