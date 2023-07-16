from sondehub_api import ApiSettingsStuttgart, get_final_coordinates
from datetime import datetime, timezone, timedelta
from bbox import BBox
from send_mail import send_email
import config

my_bbox = BBox(8.832943, 48.458465, 9.167872, 48.773893)

def main():
    # Launch datetimes to check: tomorrow at 6:00 UTC and at 12:00 UTC.
    tomorrow = datetime.now(timezone.utc) + timedelta(days=1)
    launch_datetimes = [
        datetime(tomorrow.year, tomorrow.month, tomorrow.day, 6, 0, 0, tzinfo=timezone.utc),
        datetime(tomorrow.year, tomorrow.month, tomorrow.day, 12, 0, 0, tzinfo=timezone.utc),
    ]

    # Get API settings for Stuttgart.
    api_settings = ApiSettingsStuttgart()

    # Get API URLs for the launch datetimes.
    api_urls = [api_settings.with_launch_datetime(launch_datetime).api_url() for launch_datetime in launch_datetimes]

    # Get final coordinates for the launch datetimes.
    final_coordinates = [get_final_coordinates(api_url) for api_url in api_urls]

    # Print the final coordinates.
    for launch_datetime, final_coordinate in zip(launch_datetimes, final_coordinates):
        if my_bbox.is_inside(final_coordinate[0], final_coordinate[1]):
            print(f"FOUND: {launch_datetime}: {final_coordinate[0]}, {final_coordinate[1]}")
            send_email(
                subject="Radiosonde: Found launch!",
                body=f"Found launch at {launch_datetime}: {final_coordinate[0]}, {final_coordinate[1]}\n" + \
                    "https://predict.sondehub.org/",
                sender=config.sender,
                recipients=config.recipients,
                password=config.password,
            )


if __name__ == "__main__":
    main()
