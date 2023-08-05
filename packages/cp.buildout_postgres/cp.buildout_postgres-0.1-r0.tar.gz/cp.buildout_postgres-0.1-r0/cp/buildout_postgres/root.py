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
		options["bin-dir"] = os.path.join(options["location"],'bin')
		options['conf-dir'] = os.path.join(options["location"],options["data-dir"])
		conf_path = os.path.join(options["location"], options["data-dir"])
		options['ctl_path'] = os.path.join(self.buildout["buildout"]["bin-directory"],self.name)
		options['lib-dir'] = os.path.join(options['location'],'lib')
		options["conf-path"] = conf_path
		options["serverroot"] = options["location"]
		# directories
		for sub in "",options["data-dir"], "lock", options["log-dir"], "run":
			path = os.path.join(options["location"], sub)
			options[sub] = path
		return

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

			self.log.info('starting in on directory additions')
			# directories
			for sub in "lock",options["data-dir"], options["log-dir"], "run":
				path = os.path.join(location, sub)
				if not os.path.exists(path):
					os.mkdir(path)
				else:
					assert os.path.isdir(path)
				options[sub] = path

			self.log.info('starting in on file additions')
			#files
			conf_path = options['conf-path']
			ctl_path = options['ctl_path']

			cmd = os.path.join(self.options['symlink_target'],'initdb')
		
			#args = '-E UTF8 --locale en_US.UTF-8','-D %s' % (os.path.join(location,options["data-dir"])) 
			cmd += ' -E UTF8 --locale en_US.UTF-8 -D %s' % (conf_path)
			ret = commands.getoutput(cmd)
			self.log.info('returning: %s' % ret)
			#ret = self.run(cmd,'-E UTF8','--locale=en_US.UTF-8','-D %s' % (conf_path))
			#self.log.info('run returned: ' % ret)
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
		return [location,ctl_path,conf_path] + symRet

	def update(self):
		pass

	def run(self,*args):
		cmd = ' '.join(args)
		self.log.info('running: %s' % cmd) 
		ret = commands.getoutput(cmd)
		# sl=os.spawnl
		# ret=apply(sl,(os.P_WAIT,args[0])+args)
		self.log.info('returning: %s' % ret)
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