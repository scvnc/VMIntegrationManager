import fabric
from fabric.api import run, env
import unittest
from VMIntegrationManager import VMIntegrationManager

import logging
logging.basicConfig(filename='/tmp/test.log', level=logging.DEBUG)

# Fabric config
env.host_string = 'deb'
env.use_ssh_config = True
env.connection_attempts = 30

class VMIntegrationManagerTestCase(unittest.TestCase):
	
	def setUp(self):
		self._mgr = VMIntegrationManager()
		self._mgr.vm_id = 'Debian VPS Testing'
	
	def test_using_existing_freeze_state(self):
		
		self._mgr.freeze_id = 'Fresh_State'
		
		self._mgr.restore_state()
		
		self._mgr.start_machine()
		
		self.assertFalse(self.file_exists('testXYZ'))
		
		run('echo hi > testXYZ')
		
		self.assertTrue(self.file_exists('testXYZ'))
		
		fabric.network.disconnect_all()
		self._mgr.kill_machine()
		
		self._mgr.restore_state()
		
		self._mgr.start_machine()
		
		self.assertFalse(self.file_exists('testXYZ'))
	
	def test_routine(self):
		
		self._mgr.start_machine()
		
		# Ensure there is no test file
		run('rm -f testXYZ')
		self.assertFalse(self.file_exists('testXYZ'))
		
		self._mgr.freeze_state()
		
		# Restore the file
		run('echo hi > testXYZ')
		
		# Stop machine
		fabric.network.disconnect_all()
		self._mgr.kill_machine()
		
		self._mgr.restore_state()
		
		self._mgr.start_machine()
		
		# Are we back to where we were?
		self.assertFalse(self.file_exists('testXYZ'))

	
	def file_exists(self, path):
		return not run('test ! -f {0}'.format(path),
			warn_only=True).succeeded
