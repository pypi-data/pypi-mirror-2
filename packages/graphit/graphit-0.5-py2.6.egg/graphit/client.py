#!/usr/bin/env python
#coding=utf8
#
#       Copyright 2009 Antoine Millet <antoine@inaps.org>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import sys

from optparse import OptionParser
from urlparse import urlparse
from socket import gethostname

from restkit import RestClient, httpc

class GraphItAgent:
	
	def __init__(self, base_url, login=None, passwd=None):
		
		self.base_url = base_url
		
		transport = httpc.HttpClient()
		
		if login and passwd:
			transport.add_authorization(
				httpc.BasicAuth((login, passwd))
			)
		
		self._client = RestClient(transport=transport)
		
	def add_value(self, set, feed, value, unit=''):
		''' Add a value in set for feed. '''
		
		self._client.post(
			self.base_url,
			path = '%s/%s' % (set, feed),
			body = {'value': value, 'unit': unit},
			headers = {'Content-type': ('application/x-www-form-urlenco'
										'ded; charset=utf-8')},
		)

class GraphITWatcher(GraphItAgent):
	''' GraphITWatcher is program used to watch a specific ressource
	and submit it values to the GraphIT daemon. '''

	__name__ = None
	__version__ = None
	__wid__ = None
	__author__ = None

	def __init__(self):
		op = OptionParser(usage='usage: %prog [options] url')
		
		self.init_options(op)
		
		op.add_option('-s', '--set',
			help='Set "set" value of request (by default, hostname_wid)'
		)
		op.add_option('-d', '--dry-run', 
			action='store_true',
			default=False,
			help='run watcher but do not submit data to daemon.'
		)
		op.add_option('-v', '--verbose',
			action='store_true',
			default=False,
			help='print submited values on STDOUT'
		)
		op.add_option('--version',
			action='store_true',
			default=False,
			help='print version and exit'
		)
		
		(self._options, args) = op.parse_args()
		
		# --version mode:
		if self._options.version:
			print '%s (%s) v%s by %s' % (
				self.__name__,
				self.__wid__,
				self.__version__,
				self.__author__
			)
			sys.exit(0)
		
		# Validating:
		if len(args) != 1:
			op.error(('Watcher needs URL of GraphIT daemon to'
						' which to send the data'))
		
		self._url = urlparse(args[0])
		
		if self._url.scheme != 'http':
			op.error(('GraphIT only support http protocol'))
		
		if self._url.port is not None:
			port = ':%s' % self._url.port
		else:
			port = ''
		
		url = 'http://%s%s/%s' % (self._url.hostname, port, self._url.query)
		
		self.check_options(op)
		
		# Super
		GraphItAgent.__init__(
			self,
			url, 
			login=self._url.username, 
			passwd=self._url.password
		)
		
		self.run()

	def init_options(self, op):
		pass

	def check_options(self, op):
		pass

	def get_set(self):
		''' Get "set" value for request. By default, I take hostname
			and wid (Watcher ID), but value can be redefined by user
			with "--set" cli option. '''
			
		if self._options.set:
			return self._options.set
		else:
			return '%s_%s' % (gethostname(), self.__wid__)
			
	def submit(self, feed, value, unit=''):
		''' Submit value to GraphITd if dry run mode is not enabled. '''
		
		if self._options.verbose:
			print 'Submitting value %s%s to %s/%s/%s...' % (
				value,
				unit,
				self._url.hostname,
				self.get_set(),
				feed
			)
		
		if not self._options.dry_run:
			self.add_value(
				self.get_set(),
				feed,
				value,
				unit
			)
