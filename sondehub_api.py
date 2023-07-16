import requests
import urllib.parse
from dataclasses import dataclass
from datetime import datetime

def get_api_url(
    launch_datetime: datetime,
    launch_latitude: float,
    launch_longitude: float,
    launch_altitude: float,
    ascent_rate=5,
    burst_altitude=30000,
    descent_rate=5,
    profile="standard_profile",
    pred_type="single",
):
    # Create the API URL
    api_url = "https://api.v2.sondehub.org/tawhiri?"
    api_url += urllib.parse.urlencode(
        {
            "profile": profile,
            "pred_type": pred_type,
            "launch_datetime": launch_datetime.isoformat(),
            "launch_latitude": launch_latitude,
            "launch_longitude": launch_longitude,
            "launch_altitude": launch_altitude,
            "ascent_rate": ascent_rate,
            "burst_altitude": burst_altitude,
            "descent_rate": descent_rate,
        }
    )
    return api_url


@dataclass
class ApiParameters:
    """Class to hold API parameters."""

    launch_datetime: datetime
    launch_latitude: float
    launch_longitude: float
    launch_altitude: float
    ascent_rate: int = 5
    burst_altitude: int = 30000
    descent_rate: int = 5
    profile: str = "standard_profile"
    pred_type: str = "single"

    
    def with_launch_datetime(self, launch_datetime):
        """Create a new ApiParameters object with a different launch_datetime."""
        return ApiParameters(
            launch_datetime,
            self.launch_latitude,
            self.launch_longitude,
            self.launch_altitude,
            self.ascent_rate,
            self.burst_altitude,
            self.descent_rate,
            self.profile,
            self.pred_type,
        )

    def api_url(self):
        return get_api_url(
            self.launch_datetime,
            self.launch_latitude,
            self.launch_longitude,
            self.launch_altitude,
            self.ascent_rate,
            self.burst_altitude,
            self.descent_rate,
            self.profile,
            self.pred_type,
        )


def ApiSettingsStuttgart():
    return ApiParameters(
        launch_datetime=datetime(1000, 1, 1, 1, 1, 1),
        launch_latitude=48.8283,
        launch_longitude=9.2,
        launch_altitude=300,
        ascent_rate=5,
        burst_altitude=30000,
        descent_rate=5,
        profile="standard_profile",
        pred_type="single",
    )


def get_final_coordinates(api_url):
    # Get the API response.
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()

    final_data = data["prediction"][-1]["trajectory"][-1]

    # Get the final coordinates.
    final_latitude = final_data["latitude"]
    final_longitude = final_data["longitude"]

    return final_latitude, final_longitude
