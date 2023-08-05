# Copyright (c) 2007 Thomas Lotze
# See also LICENSE.txt

"""zc.buildout recipe for Postgres.
"""

import os
import os.path
import stat
import subprocess, commands
import re
import gocept.cmmi
import cns.recipe.symlink
import urllib

import pkg_resources
import logging, zc.buildout

from cp.buildout_postgres import config


MOD_LINE = re.compile("^\s*mod_(.*)\.c\s*$")


read_resource = lambda filename: pkg_resources.resource_string(__name__,
															   filename)


class Recipe(object):
	"""zc.buildout recipe for postgres.
   
 	Configuration options:
	For gocept.cmmi:
		version
        url
        md5sum
        extra-options
        extra-vars

	for setup:
		log-dir
		data-dir
		pg-hba-extra
		pg-ident-extra
		pg-conf-extra


    Exported options:
        pg-path
		data-dir
		log-dir
		pid-dir
		startupscript
	"""

	def __init__(self, buildout, name, options):
		
		self.buildout = buildout
		self.name = name
		self.options = options
		self.log = logging.getLogger(self.name)
		self.log.info('constructor options: %s' % self.options)
		self.cmmi = gocept.cmmi.Recipe(buildout,name,options)
		self.symlink = cns.recipe.symlink.Recipe(buildout,name,options)
		#self.log.info(self.cmmi)
		#self.log.info(self.cmmi.options)
		#print dir(self.cmmi)
		for key, value in config.items("postgres"):
			self.log.info('default config: %s: %s' % (key,value))
			options.setdefault(key, value)
		options["location"] = os.path.join(
			buildout["buildout"]["parts-directory"], name)
		return
		# # # Collect and normalize some options for buildout book-keeping.
		# # postgres_options = buildout[options.get("postgres", "postgres")]
		# # for key in "postgres-path", "envvars-path":
		# # 	options.setdefault(key, postgres_options[key])
		# 
		# # for key in "data":
		# # 	options[key] = os.path.normpath(os.path.join(
		# # 		buildout["buildout"]["directory"], options[key]))
		# 
		# # We need to re-install after httpd was built differently in order to
		# # query the built-in modules again.
		# options["postgres-sig"] = (postgres_options.get("md5sum", "") +
		# 						postgres_options.get("extra-options", ""))
		# 
		# # Recursively collect unique config-parts, breadth-first, considering
		# # root as the initial part.
		# config_parts = [(name, options)]
		# for name, part in config_parts:
		# 	parts = [(name, buildout[name])
		# 			 for name in part.get("config-parts", "").split()]
		# 	config_parts.extend(
		# 		part for part in parts if part not in config_parts)
		# 
		# # Collect unique modules from config-parts, in order.
		# self.modules = []
		# for name, part in config_parts:
		# 	self.modules.extend(module
		# 						for module in part.get("modules", "").split()
		# 						if module not in self.modules)
		# options["modules"] = " ".join(self.modules)
		# 
		# # Format other config-parts stuff.
		# for key, format in (
		# 	("extra-env", lambda part: "".join("export %s\n" % line.strip()
		# 									   for line in part.splitlines()
		# 									   if line.strip())),
		# 	("extra-config", lambda part: part),
		# 	("pg-hba-config", lambda part: part),
		# 	):
		# 	options[key] = "\n".join(
		# 		"#\n# Config part: %s\n#\n%s" % (name, value)
		# 		for name, value in ((name, format(part.get(key, "")))
		# 							for name, part in config_parts)
		# 		if value)
	def install(self):
		"""A recipe install method is expected to return a string, or an iterable of strings containing paths to be removed if a part is uninstalled."""
		try:
			options = self.options.copy()
			md5sum = urllib.urlopen(options['md5link']).read()
			#MD5 (postgresql-8.3.1.tar.gz) = 91ae66ca7a6051abe49d8cea737a9acc
			a,b = md5sum.split('=')
			md5sum = b.strip()
			self.options['md5sum'] = md5sum
			cmmiRet = self.cmmi.install()
			self.log.info('cmmiRet: %s' % cmmiRet)
			self.log.info('options in install are: %s' % options)
			location = options["location"]
			self.options['symlink_base'] = os.path.join(location,'bin')
			self.options['symlink_target'] = self.buildout["buildout"]["bin-directory"]
			self.options['symlink'] = "\n".join(os.listdir(self.options['symlink_base']))
			self.log.info('symlink: %s to %s' % (self.options['symlink_base'],self.options['symlink_target']))
			self.log.info('these items: %s' % self.options['symlink'])
			symRet = self.symlink.install()
			self.log.info('symRet: %s', symRet)
			# main server config
			# options["listen"] = "\n".join(
			# 	"Listen " + line for line in options["listen"].split())
			# 
			# builtins = set(builtin_modules(options["pg-path"]))
			# options["load-module"] = "\n".join(
			#	  "LoadModule %s_module %s/mod_%s.so" %
			#	  (module, options["module-dir"], module)
			#	  for module in self.modules
			#	  if module not in builtins)
			# 
			# names = options["servername"].split()
			# options["servername"] = "ServerName " + names.pop(0)
			# options["serveralias"] = "\n".join(
			#	  "ServerAlias " + name for name in names)
			# 
			# admin = options.setdefault("serveradmin", "")
			# if admin:
			#	  options["serveradmin"] = "ServerAdmin " + admin

			self.log.info('starting in on directory additions')
			# directories
			for sub in "",options["data-dir"], "lock", options["log-dir"], "run":
				path = os.path.join(location, sub)
				if not os.path.exists(path):
					os.mkdir(path)
				else:
					assert os.path.isdir(path)
				options[sub] = path

			self.log.info('starting in on file additions')
			#files
			conf_path = os.path.join(location, options["data-dir"])
			ctl_path = os.path.join(self.buildout["buildout"]["bin-directory"],self.name)
		
			options["conf-path"] = conf_path
			options["serverroot"] = location


			cmd = os.path.join(self.options['symlink_target'],'initdb')
		
			#args = '-E UTF8 --locale en_US.UTF-8','-D %s' % (os.path.join(location,options["data-dir"])) 
			run(cmd,'-E UTF8','--locale=en_US.UTF-8','-D %s' % (conf_path))
			self.log.info('setting up config files.')
			
			self.log.info("dir: %s" % os.listdir(conf_path))

			open(os.path.join(conf_path,'pg_hba.conf'), "w").write(read_resource("pg_hba.conf.in") % options)
			open(os.path.join(conf_path,'pg_ident.conf'), "w").write(read_resource("pg_ident.conf.in") % options)
			open(os.path.join(conf_path,'postgresql.conf'), "w").write(read_resource("postgresql.conf.in") % options)
			self.log.info('.finished config files.')
			os.chmod(conf_path,0700)
		except:
			e = LogException()
			self.log.info(e)
		self.log.info("dir: %s" % os.listdir(conf_path))
		return [location,ctl_path,conf_path, ]

	def update(self):
		pass

def run(*args):
	cmd = ' '.join(args)
	print cmd
	ret = commands.getoutput(cmd)
	# sl=os.spawnl
	# ret=apply(sl,(os.P_WAIT,args[0])+args)
	return ret
	# stdout, ignored = subprocess.Popen([cmd,args],stdout=subprocess.PIPE).communicate()
	# return stdout

def LogException():
	"""
	I grab the traceback log it
	And return a happy formatted message back to you

	"""
	import traceback
	msg = traceback.format_exc()
	print msg
	return msg
	
def builtin_modules(httpd_path):
	"""Query the httpd binary for its built-in modules.
	"""
	stdout, ignored = subprocess.Popen([httpd_path, "-l"],
									   stdout=subprocess.PIPE).communicate()
	return (mo.groups(0)[0]
			for mo in (MOD_LINE.search(line)
					   for line in stdout.splitlines())
			if mo)
