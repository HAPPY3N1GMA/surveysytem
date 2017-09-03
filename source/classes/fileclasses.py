import csv, ast, os, time
#Classes for different file types
class IDfile():
	def __init__(self, filename):
		self._name = filename

#class for textfiles, accessing mainly ID files
class textfile(IDfile):
	def getcurrentID(self):
		try:
			fileID = open(self._name,"r+")
		except FileNotFoundError:
			return 0
		else:
			val = fileID.read()
			if val == '':
				val = 0
			fileID.close()
			return str(val)
	def updateID(self):
		new_val = int(self.getcurrentID())
		IDfile = open(self._name,"w")
		new_val += 1
		IDfile.write(str(new_val))
		return str(new_val)

#Writing to and from CSV files
class csvfile(IDfile):
	def writeto(self,ID,name,course,time,questions):
		with open(self._name,'a') as csv_out:
			writer = csv.writer(csv_out)
			writer.writerow([ID,name,course,time,list(questions)])
	def readfrom(self):
		with open(self._name,'r') as csv_in:
			reader = csv.reader(csv_in)
			namelist = []
			for row in reader:
				namelist.append(row)
			return namelist
	def readfromid(self,rowID):
		file = self.readfrom()
		for row in file:
			if row[0]==str(rowID):
				return row

	def appendfield(self,rowID,fieldID,content):
		tmp = "tmp.csv"
		with open(self._name, 'r+') as csvReadFile:
			reader = csv.DictReader(csvReadFile)
			with open (tmp, 'w') as write_row:
				#get list of fields from the csv header
				fields = reader.fieldnames;
				#rowIDField is always the first field/column
				rowIDField = fields[0]
				writer=csv.DictWriter(write_row, fieldnames=fields)
				writer.writeheader() #write headerfiles
				for row in reader:
					if(row[rowIDField]==rowID):
						tmp_list=ast.literal_eval(row[fieldID])
						tmp_list.append(content)
						row[fieldID] = tmp_list
					writer.writerow(row)				
		os.remove(self._name)
		os.rename(tmp, self._name)
