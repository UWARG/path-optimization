"""
Reads in hardcoded waypoints from CSV file and sends drone commands.
"""

import pathlib
import time

import dronekit

from modules import add_takeoff_and_loiter_command
from modules import check_stop_condition
from modules import load_waypoint_name_to_coordinates_map
from modules import upload_commands
from modules import waypoints_to_commands
from modules import waypoint_tracking
from modules import waypoints_dict_to_list
from modules.common.kml.modules import ground_locations_to_kml


WAYPOINT_FILE_PATH = pathlib.Path("2024", "waypoints", "north_campus_waypoints_task_2.csv")
TAKEOFF_ALTITUDE = 10
DRONE_TIMEOUT = 30.0  # seconds
CONNECTION_ADDRESS = "tcp:localhost:14550"
LOG_DIRECTORY_PATH = pathlib.Path("logs")
KML_FILE_PREFIX = "waypoints"
DELAY = 0.1  # seconds
MAXIMUM_FLIGHT_TIME = 1800  # seconds


def main() -> int:
    """
    Main function.
    """
    pathlib.Path(LOG_DIRECTORY_PATH).mkdir(exist_ok=True)

    # Wait ready is false as the drone may be on the ground
    drone = dronekit.connect(CONNECTION_ADDRESS, wait_ready=False)

    # Read in hardcoded waypoints from CSV file
    # Waypoints are stored in order of insertion, starting with the top row
    (
        result,
        waypoint_name_to_coordinates,
    ) = load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_and_altitude_map(
        WAYPOINT_FILE_PATH,
    )
    if not result:
        print("ERROR: load_waypoint_name_to_coordinates_map")
        return -1

    result, waypoints_list = waypoints_dict_to_list.waypoints_dict_with_altitude_to_list(
        waypoint_name_to_coordinates
    )
    if not result:
        print("ERROR: Unable to convert waypoints from dict to list")
        return -1

    location_ground_list = list(map(lambda waypoint: waypoint.location_ground, waypoints_list))
    result, _ = ground_locations_to_kml.ground_locations_to_kml(
        location_ground_list,
        KML_FILE_PREFIX,
        LOG_DIRECTORY_PATH,
    )
    if not result:
        print("ERROR: Unable to generate KML file")
        return -1

    result, waypoint_commands = waypoints_to_commands.waypoints_with_altitude_to_commands(
        waypoints_list,
    )
    if not result:
        print("Error: waypoints_to_commands")
        return -1

    # get the last waypoint for loitering
    loiter_coordinate = waypoints_list[-1]

    result, takeoff_loiter_commands = add_takeoff_and_loiter_command.add_takeoff_and_loiter_command(
        waypoint_commands,
        loiter_coordinate.location_ground.latitude,
        loiter_coordinate.location_ground.longitude,
        TAKEOFF_ALTITUDE,
        loiter_coordinate.altitude,
    )
    if not result:
        print("Error: add_takeoff_and_loiter_command")
        return -1

    result = upload_commands.upload_commands(drone, takeoff_loiter_commands, DRONE_TIMEOUT)
    if not result:
        print("Error: upload_commands")
        return -1

    start_time = time.time()
    while True:
        result, waypoint_info = waypoint_tracking.get_current_waypoint_info(drone)
        if not result:
            print("Error: waypoint_tracking (waypoint_info)")
        else:
            print(f"Current waypoint sequence: {waypoint_info}")

        result, location = waypoint_tracking.get_current_location(drone)
        if not result:
            print("Error: waypoint_tracking (get_current_location)")
        else:
            print(f"Current location (Lat, Lon): {location}")

        # Send drone back to launch if exceeds time limit
        current_time = time.time()
        is_returning_to_launch = check_stop_condition.check_stop_condition(
            start_time, current_time, drone, MAXIMUM_FLIGHT_TIME
        )
        if is_returning_to_launch:
            break

        print(f"Elapsed time (s): {current_time - start_time}")

        time.sleep(DELAY)

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main < 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
