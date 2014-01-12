# source for std codes (seems reasonable?) 
# http://www.simbazar.com/upload/download/174ALL%20INDIA%20STD%20CODE%20LIST.xls

formats = """Ankur, 011, RK Puram
Ankur 011 RK Puram
Ankur RK Puram 011
I love AAP Ankur 011
Name:Ankur STD Code:011 VidhanSabha: RK Puram"""

import unittest, csv, re, json

std_codes = []
assemblies = []

def get_std_codes():
	global std_codes
	if not std_codes:
		with open("areacodes.csv", "r") as f:
			reader = csv.reader(f.read().splitlines(True))
	
		std_codes = ["0" + r[3] for r in reader]
		
	return std_codes
	
def get_assemblies():
	global assemblies
	if not assemblies:
		with open("assemblies.json", "r") as f:
			data = json.loads(f.read())
			for state, dists in data.iteritems():
				for dist, _assemblies in dists.iteritems():
					assemblies += _assemblies
	
	return assemblies
	
def parse(txt):
	std_codes = get_std_codes()
	assemblies = get_assemblies()

	out = {
		"name": None,
		"std": None,
		"assembly": None,
	}
		
	for assembly in assemblies:
		if assembly in txt:
			out["assembly"] = assembly
		
			# found, remove from text
			txt.replace(assembly, "")
			break
	
	# remove prefixes
	if ":" in txt:
		txt =  re.sub("[a-zA-Z]*:", "", txt)
	
	# with commas
	if "," in txt:
		parts = txt.split(",")
		parts = [p.strip() for p in parts]
	else:
		parts = txt.split()
		
	for p in parts:
		if p.isdigit():
			if p in std_codes:
				out["std"] = p
			if "0" + p in std_codes:
				out["std"] = "0" + p
				
	return out
	
def parse_and_dump():
	import config
	import MySQLdb
	
	cursor = MySQLdb.connect("localhost", config.db_user, config.db_password).cursor()
	cursor.execute("use %s" % config.db_name)
	
	cursor.execute("show tables")
	if not "members" in [d[0] for d in cursor.fetchall()]:
		cursor.execute("create table members (name varchar(255), std varchar(10), assembly varchar(255)) engine myisam")
	
	with open(config.source_file, "r") as f:
		data = f.read()
		
	for txt in data.splitlines():
		out = parse(txt)
		
		cursor.execute("insert into members (name, std, assembly) values (%s, %s, %s)", 
			(out["name"], out["std"], out["assembly"]))
				
class TestParser(unittest.TestCase):
	def test_parser(self):
		for f in formats.splitlines():
			r = parse(f)
			self.assertEquals(r["std"], "011")
			if "RK Puram" in f:
				self.assertEquals(r["assembly"], "RK Puram")
	
if __name__=="__main__":
	#	unittest.main()
	parse_and_dump()