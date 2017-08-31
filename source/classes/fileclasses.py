import csv, ast, os, time
class IDfile():
	def __init__(self, filename):
		self._name = filename


class textfile(IDfile):
	def getcurrentID(self):
		fileID = open(self._name,"r+")
		val = fileID.read()
		if val == "":
			return 0
		fileID.close()
		return str(val)
	def updateID(self):
		new_val = int(self.getcurrentID())
		IDfile = open(self._name,"w")
		new_val += 1
		IDfile.write(str(new_val))
		return str(new_val)


class csvfile(IDfile):
	def writeto(self,ID,name,course,time):
		with open(self._name,'a') as csv_out:
			writer = csv.writer(csv_out)
			writer.writerow([ID,name,course,time])
	def readfrom(self):
		with open(self._name,'r') as csv_in:
			reader = csv.reader(csv_in)
			namelist = []
			for row in reader:
				namelist.append(row)
			return namelist