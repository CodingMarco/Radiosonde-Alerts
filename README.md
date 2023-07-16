# Radiosonde Alerts
This scripts checks for radiosonde launches from some location if they land within a specified bounding box.
If so, the script sends an email.
The next day is always checked, so it makes sense to run this script once each evening (eg. using a cron job).
