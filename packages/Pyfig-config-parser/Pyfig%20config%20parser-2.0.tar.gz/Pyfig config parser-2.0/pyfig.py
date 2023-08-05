"""
pyfig.py
Pyfig is an easy and quick way for you to open, parse, and return values of config files.
$author: alecwh
$version: 2.0
$date: Aug 2008
$website: http://pyfig.alecwh.com/

Copyright 2008-09 Alec Henriksen
This software is released under the GNU GPL v2, see the COPYING file.
"""
import sys

# important seperator/comment variables
comment_characters = ['#', ';']  # items must be 1 char long
config_seperator = '\n'
individual_seperator = '='

class ConfigError(Exception):
	# used if an error was found while parsing
	pass
	
class ConfigFileError(Exception):
	# used if files are not found/wrong permissions
	pass
	
class ConfigCategory(object):
	"""
	Container for config pairs and more categories
	"""
	def __init__(self):
		self.meta = {}
		
	def __setitem__(self, name, value):
		setattr(self, name, value)
		
	def __iter__(self):
		self.meta["config_list"] = [x for x in dir(self) if x[:2] != "__"]
		
		# remove known and irrelevant attrs
		self.meta["config_list"].remove("meta")
		self.meta["config_list"].remove("next")
		
		self.meta["count"] = 0
		return self
		
	def next(self):
		try:
			next = self.meta["config_list"][self.meta["count"]]
			self.meta["count"] += 1
		except IndexError:
			raise StopIteration
			
		if next != "next" and next != "meta":
			# return a tuple of key, values
			return next, getattr(self, next)
		
class Pyfig:
	"""
	Holds and parses a configuration file.
	To use:
	>>> config = Pyfig("/path/to/config/")
	>>> config.name
	
	All meta information about the file is held in
	Pyfig.meta (dict)
	"""
	
	def __init__(self, config_file=None):
		"""
		Init meta dictionary, open and read file.
		"""
		self.meta = {}
		# init meta information (dict so I don't cloud the namespace)
		self.meta["config_file"] = config_file
		self.meta["raw"] = "" # raw file, string
		self.meta["count"] = 0 # how many configurations
		self.meta["keys"] = [] # stores the config keys found
		self.meta["config"] = {} # the actual dict of configurations
		self.meta["config_temp"] = [] # for temp storing
		
		# default category, for global configs
		self.general = ConfigCategory()
		
		# is config file existant?
		if self.meta["config_file"] == None:
			raise ConfigFileError("No file path was given for config file")
		else:
			config_file = open(self.meta["config_file"])
			self.meta["raw"] = config_file.read().strip()
			config_file.close()
			
		self._parse()
		
	def __iter__(self):
		self.meta["category_list"] = [x for x in dir(self) if x[:1] != "_" and x != "meta"]
		self.meta["count"] = 0
		return self
		
	def next(self):
		try:
			next = self.meta["category_list"][self.meta["count"]]
			self.meta["count"] += 1
		except IndexError:
			raise StopIteration
			
		return next, getattr(self, next)
		
	def _get_type(self, name, value):
		"""
		Finds out what type is intended with this value
		Default is string
		"""
		types = {
			"int": int,
			"integer": int,
			"str": str,
			"string": str,
			"fl": float,
			"float": float
			}
			
		# name should either be 'name' or 'name/int' (& variations)
		if '/' in name:
			name = name.split("/")
			# find out what the type is,
			# convert, return
			x = types[name[1].strip()]
			
			return x(value)
		
		else:
			return str(value).strip()
		
		
	def _parse(self):
		"""
		Parses the file in self.meta["raw"]
		with comment configurations at the top
		"""
		# get list of key/value pairs (configname=configvalue)
		self.meta["config_temp"] = self.meta["raw"].split(config_seperator)
		
		# remove blanks (list filtering)
		self.meta["config_temp"] = [line for line in self.meta["config_temp"] if line]
		
		# default category is global
		# all pairs not in a category will be put in here
		current_category = "general"
		
		# iterate through the new dict
		# skip over any lines that begin with comment_character
		for item in self.meta["config_temp"]:
			if item.strip()[0] in comment_characters: continue
			if item.strip()[0] == "[":
				# this is a category, create category object
				category_name = item.strip().replace("[", "").replace("]", "")
				
				# create category object
				setattr(self, category_name, ConfigCategory())
				
				# remember for subsequent parses
				current_category = category_name
				
				# this isn't a config, only a category, skip rest
				continue
				
			try:
				# split the name/value pair
				# broken pairs (bad seperator) will register ValueError
				name, value = item.split(individual_seperator, 1)
				
				# we need to strip type indicators (like age/int), `/` doesn't
				# play well in naming attributes
				if '/' in name:
					safe_name = name.split('/')[0].strip()
				else:
					safe_name = name.strip()
				
				# set to instance namespace, basically add the pair to Category
				# _get_type() will return a string, int, or float of the value
				getattr(self, current_category, self)[safe_name] = self._get_type(name, value)
				
				# stats update
				self.meta["keys"].append(name.strip())
				self.meta["count"] += 1
			except ValueError:
				raise ConfigError("Improper seperator found in config file")
		
if __name__ == "__main__":
	error_message = "File not found (or bad permissions), try again."
	if len(sys.argv) > 1:
		try:
			pyfig = Pyfig(sys.argv[1])
		except ConfigFileError:
			print error_message
			sys.exit()
	else:
		while True:
			file_ = raw_input("Enter the config filename: ")
			# try parsing with given input
			try:
				pyfig = Pyfig(file_)
				break
			except ConfigFileError:
				print error_message
				
	print "Config keys found:"
	print pyfig.meta["keys"]
