# coding=utf-8
from __future__ import absolute_import

__author__ = "Brandon Jones <bjones14@gmail.com>"
__license__ = "AGPLv3"
__copyright__ = "TBD"

import octoprint.plugin
from octoprint.util import RepeatedTimer
from pyvesync_v2.vesync import VeSync


class VeSyncPowerMonitorPlugin(octoprint.plugin.StartupPlugin,
							   octoprint.plugin.TemplatePlugin,
							   octoprint.plugin.AssetPlugin,
							   octoprint.plugin.SettingsPlugin):

	def __init__(self):
		self._vesync_data_engine_timer = None
		self._manager = None

	def on_after_startup(self):
		# check to verify connection was successful - if it was, launch the VeSync data engine
		if self.connect_vesync_cloud():
			self.start_vesync_data_engine()

	def connect_vesync_cloud(self):
		# check to see if VeSync manager is already connected - if so, don't try to connect again
		if not self._manager:
			# try connecting to the VeSync using the provided configuration data
			self._manager = VeSync(self._settings.get(["username"]), self._settings.get(["password"]))

			if self._manager.login():
				self._logger.info("Successfully connected to VeSync cloud service!")
				return True
			else:
				self._logger.info("Could not connect to VeSync cloud service.  Verify username/password and try again")
				self._manager = None
				return False

	def disconnect_vesync_cloud(self):
		self._manager = None

	def start_vesync_data_engine(self):
		# check to see if VeSync data engine is already running - if so, don't try to launch it again
		if not self._vesync_data_engine_timer:
			self._logger.info("Launching the VeSync data engine...")
			self._vesync_data_engine_timer = RepeatedTimer(float(self._settings.get(["update_interval"])),
														   self.get_vesync_data,
														   None, None, True)
			self._vesync_data_engine_timer.start()

	def stop_vesync_data_engine(self):
		# check to see if VeSync data engine is running - if not, it is already stopped
		if self._vesync_data_engine_timer:
			self._logger.info("Stopping the VeSync data engine...")
			self._vesync_data_engine_timer.cancel()
			self._vesync_data_engine_timer = None

	def get_vesync_data(self):
		# only run this code if the VeSync cloud service manager is connected
		if self._manager:
			displayed_statistic = self._settings.get(["displayed_statistic"])
			device_name = self._settings.get(["device_name"])
			statistic_value = None
			statistic_name = None

			self._manager.update()
			for device in self._manager.get_devices():
				if device.device_name == device_name:
					if displayed_statistic == "kWh_now":
						statistic_value = (device.get_power() / 1000)
						statistic_name = "kWh"
					elif displayed_statistic == "kWh_today":
						statistic_value = device.get_kwh_today()
						statistic_name = "kWh Today"
					elif displayed_statistic == "voltage":
						statistic_value = device.get_voltage()
						statistic_name = "Voltage"
					self._logger.debug(statistic_value)
					self._plugin_manager.send_plugin_message(self._identifier, dict(name=statistic_name,
																					value=statistic_value))

	def get_settings_defaults(self):
		return dict(username="user@domain.com",
					password="",
					device_name="",
					displayed_statistic="kWh",
					update_interval=5)

	def on_settings_save(self, data):
		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

		self._logger.info("New configuration received - restarting services...")
		self.stop_vesync_data_engine()
		self.disconnect_vesync_cloud()
		if self.connect_vesync_cloud():
			self.start_vesync_data_engine()

	def get_template_configs(self):
		return [
			dict(type="navbar", custom_bindings=False),
			dict(type="settings", custom_bindings=False)
		]

	def get_assets(self):
		return {
			"js": ["js/vesync-power-monitor.js"]
		}

	def get_update_information(self):
		return dict(
			vesync_power_monitor_plugin=dict(
				displayName="VeSync Power Monitor Plugin",
				displayVersion=self._plugin_version,
				type="github_release",
				user="bjones14",
				repo="OctoPrint-VeSync-Power-Monitor",
				current=self._plugin_version,
				pip="https://github.com/bjones14/OctoPrint-VeSync-Power-Monitor/archive/{target_version}.zip"
			)
		)


__plugin_name__ = "VeSync Power Monitor"
__plugin_author__ = "Brandon Jones"
__plugin_url__ = "https://github.com/bjones14/OctoPrint-VeSync-Power-Monitor"


def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = VeSyncPowerMonitorPlugin()

	global __plugin_hooks_
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
