import ast, os, re

#checks for invalid characters in string
#return True if clean, false if not
def cleanString(inputString):
	invalid = re.compile(r"[/[\]{}~`<>]");
	if invalid.search(inputString):
	    return False
	else:
	    return True