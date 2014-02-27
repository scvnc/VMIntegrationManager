from subprocess import check_output, STDOUT, CalledProcessError
from time import time
import logging
 
class VMIntegrationManager():
	
	def start_machine(self):
		
		cmd = ['vboxmanage', 
			   'startvm', 
			   self.vm_id, 
			   '--type', 'headless' ] 
			   
		self._call_cmd(cmd)
		
		
	def kill_machine(self):
		
		cmd = ['vboxmanage', 
			   'controlvm', 
			   self.vm_id, 
			   'poweroff']
			   
		self._call_cmd(cmd)
	
	
	def freeze_state(self):
		
		self._frozen_id = 'inttest@{0}'.format(time())
		
		cmd = ['vboxmanage', 
			   'snapshot', 
			   self.vm_id, 
			   'take',
			   self._frozen_id]
			   
		self._call_cmd(cmd)
		
		
	def restore_state(self):
		
		cmd = ['vboxmanage', 
			   'snapshot', 
			   self.vm_id, 
			   'restore',
			   self._frozen_id]
			   
		self._call_cmd(cmd)
		
	
	def _call_cmd(self, cmd):
		""" 
		Test smells indicate that this may need 
		to be it's own module
		"""
		
		try:
			
			retval = check_output(cmd, stderr=STDOUT)
			logging.debug(retval)
		
		except CalledProcessError as err:
			logging.error(err)
			logging.error(err.output)
			raise err
		

		
