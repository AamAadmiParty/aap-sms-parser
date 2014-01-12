formats = """Ankur, 011, RK Puram
Ankur 011 RK Puram
Ankur RK Puram 011
I love AAP Ankur 011
Name:Ankur STD Code:011 VidhanSabha: RK Puram"""

import unittest, csv, re

std_codes = []

def get_std_codes():
	global std_codes
	if not std_codes:
		with open("areacodes.csv", "r") as f:
			reader = csv.reader(f.read().splitlines(True))
	
		std_codes = ["0" + r[3] for r in reader]
		
	return std_codes

def parse(txt):
	std_codes = get_std_codes()
	
	out = {
		"name": None,
		"std": None,
		"area": None,
	}
	
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
		
class TestParser(unittest.TestCase):
	def test_parser(self):
		for f in formats.splitlines():
			r = parse(f)
			self.assertEquals(r["std"], "011")
	
if __name__=="__main__":
	unittest.main()