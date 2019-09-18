# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
from pyvesync_v2.vesync import VeSync


class VeSyncPowerMonitorPlugin(octoprint.plugin.StartupPlugin,
								octoprint.plugin.TemplatePlugin,
								octoprint.plugin.SettingsPlugin):
	def on_after_startup(self):
		# connect to VeSync using configuration data
		manager = VeSync(self._settings.get(["username"]), self._settings.get(["password"]))

		# check to verify connection was successful
		if manager.login():
			self._logger.info("Successfully connected to VeSync service!")

		manager.update()

		# user will configure name of device here to be used
		for device in manager.get_devices():
			if device.device_name == self._settings.get(["device_name"]):
				self._logger.info("Displaying initial info for " + self._settings.get(["device_name"]))
				self._logger.info(device.get_voltage())
				self._logger.info(device.get_kwh_today())
				self._logger.info(device.get_active_time())
				self._logger.info(device.get_monthly_energy_total())
				self._logger.info(device.get_power())
				self._logger.info(device.get_week_daily_energy())
				self._logger.info(device.get_weekly_energy_total())
				self._logger.info(device.get_yearly_energy_total())

	def get_settings_defaults(self):
		return dict(url="https://en.wikipedia.org/wiki/Hello_world")

	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=False)
		]


__plugin_name__ = "VeSync Power Monitor"
__plugin_implementation__ = VeSyncPowerMonitorPlugin()
