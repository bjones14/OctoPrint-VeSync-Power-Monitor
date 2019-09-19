/*
 * View model for OctoPrint-VeSync-Power-Monitor
 *
 * Author: Brandon Jones
 * License: AGPLv3
 */
$(function() {
    function VeSyncPowerMonitorViewModel(parameters) {
        var self = this;

        self.vesyncData = ko.observable(null);

        // TODO: Implement your plugin's view model here.

        self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin != "vesync_power_monitor") {
                return;
            }
            else {
                self.vesyncData(_.sprintf("%s: %.4f", data.name, data.value));
            }
        };
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: VeSyncPowerMonitorViewModel,
        dependencies: [],
        elements: [ "#vesync-data-display" ]
    });
});
