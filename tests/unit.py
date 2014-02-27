import unittest
from mock import patch, ANY
from VMIntegrationManager import VMIntegrationManager
from subprocess import CalledProcessError

# Logging
import logging
logging.basicConfig(filename='/tmp/test.log', level=logging.DEBUG)

class VMIntegrationManagerTestCase(unittest.TestCase):
	
	# Test config values.
	mock_time = 0.3
	mock_frz_id = 'inttest@{0}'.format(mock_time);
	mock_vm_id = '1234'
	
	def setUp(self):
		
		self.config_call_mock()
		self.config_randint_mock()
		
		self._mgr = VMIntegrationManager()
		self._mgr.vm_id = self.mock_vm_id

	def config_call_mock(self):
		
		callPatch = patch('VMIntegrationManager.check_output')
		self.callMock = callPatch.start()
		
		self.callMock.return_value = 'Generic good output'
		
		self.addCleanup(callPatch.stop)
		
	def config_randint_mock(self):
		
		randintPatch = patch('VMIntegrationManager.time')
		
		self.randintMock = randintPatch.start()
		self.randintMock.return_value = self.mock_time
		
		self.addCleanup(randintPatch.stop)
		
class VMIntegrationManagerStartMachineTests(VMIntegrationManagerTestCase):
	
	def act(self):
		self._mgr.start_machine()

	def test_that_process_errors_raise(self):
		self.callMock.side_effect = CalledProcessError(1,"errorcmd")
		self.assertRaises(CalledProcessError, self.act)
	
	def test_for_expected_cli_cmd(self):
		
		self.act()
		
		args = self.callMock.call_args[0]
		cmd_list = args[0]
		
		self.assertIsInstance(cmd_list, list)
		
		self.assertIn('--type', cmd_list)
		self.assertEqual(cmd_list[cmd_list.index('--type')+1], 'headless',
			"should have indicated to start headless")
		
		self.assertEqual(cmd_list[0], 'vboxmanage')
		self.assertEqual(cmd_list[1], 'startvm')
		self.assertEqual(cmd_list[2], self._mgr.vm_id)
		
class VMIntegrationManagerKillMachineTests(VMIntegrationManagerTestCase):
	
	def act(self):
		self._mgr.kill_machine()
		
	def test_that_process_errors_raise(self):
		self.callMock.side_effect = CalledProcessError(1,"errorcmd")
		self.assertRaises(CalledProcessError, self.act)
	
	def test_for_expected_cli_cmd(self):
		
		self.act()
		
		# Identify test properties
		args = self.callMock.call_args[0]
		cmd_list = args[0]
		
		self.assertIsInstance(cmd_list, list)
		self.assertEqual(cmd_list[0], 'vboxmanage')
		self.assertEqual(cmd_list[1], 'controlvm')
		self.assertEqual(cmd_list[2], self._mgr.vm_id)
		self.assertEqual(cmd_list[3], 'poweroff')

class VMIntegrationManagerFreezeStateTests(VMIntegrationManagerTestCase):
	
	
	def act(self):
		self._mgr.freeze_state()

	def test_that_process_errors_raise(self):
		self.callMock.side_effect = CalledProcessError(1,"errorcmd")
		self.assertRaises(CalledProcessError, self.act)

	def test_that_id_obtained(self):
		
		self.act()
	
		# Identify test properties
		args = self.randintMock.call_args[0]
		
		self.randintMock.assert_called_once_with()
		
	def test_for_expected_cli_cmd(self):
		
		self.act()
		
		# Identify test properties
		args = self.callMock.call_args[0]
		cmd_list = args[0]
		
		self.assertIsInstance(cmd_list, list)
		self.assertEqual(cmd_list[0], 'vboxmanage')
		self.assertEqual(cmd_list[1], 'snapshot')
		self.assertEqual(cmd_list[2], self._mgr.vm_id)
		self.assertEqual(cmd_list[3], 'take')
		self.assertEqual(cmd_list[4], self.mock_frz_id)
		
class VMIntegrationManagerRestoreStateTests(VMIntegrationManagerTestCase):
	
	
	def act(self):
		self._mgr._frozen_id = self.mock_frz_id
		self._mgr.restore_state()

	def test_that_process_errors_raise(self):
		self.callMock.side_effect = CalledProcessError(1,"errorcmd")
		self.assertRaises(CalledProcessError, self.act)
		
	def test_for_expected_cli_cmd(self):
		
		self.act()
		
		# Identify test properties
		args = self.callMock.call_args[0]
		cmd_list = args[0]
		
		self.assertIsInstance(cmd_list, list)
		self.assertEqual(cmd_list[0], 'vboxmanage')
		self.assertEqual(cmd_list[1], 'snapshot')
		self.assertEqual(cmd_list[2], self._mgr.vm_id)
		self.assertEqual(cmd_list[3], 'restore')
		self.assertEqual(cmd_list[4], self.mock_frz_id)
