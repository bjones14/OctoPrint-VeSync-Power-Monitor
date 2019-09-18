# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
from pyvesync_v2.vesync import VeSync


class VeSyncPowerMonitorPlugin(octoprint.plugin.StartupPlugin):
	def on_after_startup(self):
		# connect to VeSync using configuration data from somewhere?
		manager = VeSync("", "")
		manager.login()
		manager.update()

		#switch = manager.get_devices()[0]

		# user will configure name of device here to be used
		device_name = ""
		for device in manager.get_devices():
			if device.device_name == device_name:
				self._logger.info(device.get_voltage())
				self._logger.info(device.get_kwh_today())
				self._logger.info(device.get_active_time())
				self._logger.info(device.get_monthly_energy_total())
				self._logger.info(device.get_power())
				self._logger.info(device.get_week_daily_energy())
				self._logger.info(device.get_weekly_energy_total())
				self._logger.info(device.get_yearly_energy_total())

		#switch.device_name
		# index
		#self._logger.info(manager.get_devices()


		#for device in manager.get_devices():
		#	device.get_voltage()
		#	self._logger.info(device.)


__plugin_name__ = "VeSync Power Monitor"
__plugin_implementation__ = VeSyncPowerMonitorPlugin()
