# Copyright (c) 2007 Thomas Lotze
# See also LICENSE.txt

"""zc.buildout recipe for building Postgres from source.
"""

import os.path

import gocept.cmmi

from cp.buildout_postgres import config


class Recipe(`gocept.cmmi.Recipe`):
    """zc.buildout recipe for building an Apache HTTP server from source.

    Configuration options:
	For gocept.cmmi:
		version
        url
        md5sum
        extra-options
        extra-vars
	for setup:
		


    Exported options:
        httpd-path
        envvars-path
        apxs-path
        module-dir
        htdocs
    """

    def __init__(self, buildout, name, options):
        super(Recipe, self).__init__(buildout, name, options)

        for key, value in config.items("postgres"):
            options.setdefault(key, value)

        location = options["location"]

        # Export some options.
        for name in "postgres", "envvars":
            options[name + "-path"] = os.path.join(location, "bin", name)
        options["module-dir"] = os.path.join(location, "modules")
        options["postgres-data"] = os.path.join(location, "data")

        options["extra-options"] = (" " +
                                    options.get("extra-options", ""))
	def install(self):
		options = self.options.copy()
		location = options["location"]
		return [location,]

	def update(self):
		pass