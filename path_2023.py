"""
Task 1 path.
"""
import pathlib
import time

import dronekit

from modules import add_takeoff_and_landing_command
from modules import load_waypoint_name_to_coordinates_map
from modules import qr_input
from modules import qr_to_waypoint_names
from modules import upload_commands
from modules import waypoint_names_to_coordinates
from modules import waypoints_to_commands
from modules import waypoint_tracking


WAYPOINT_FILE_PATH = pathlib.Path(".", "waypoints", "wrestrc_waypoints.csv")
CAMERA = 0
ALTITUDE = 40
CONNECTION_ADDRESS = "tcp:localhost:14550"
DELAY = 0.1  # seconds


def run() -> int:
    # Wait ready is false as the drone may be on the ground
    drone = dronekit.connect(CONNECTION_ADDRESS, wait_ready = False)

    result, waypoint_name_to_coordinates = load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_map(WAYPOINT_FILE_PATH)
    if not result:
        print("ERROR: load_waypoint_name_to_coordinates_map")
        return -1

    result, qr_text = qr_input.qr_input(CAMERA)
    if not result:
        print("ERROR: qr_input")
        return -1

    result, waypoint_names = qr_to_waypoint_names.qr_to_waypoint_names(qr_text)
    if not result:
        print("ERROR: qr_to_waypoint_names")
        return -1

    result, waypoints = waypoint_names_to_coordinates.waypoint_names_to_coordinates(waypoint_names, waypoint_name_to_coordinates)
    if not result:
        print("ERROR: waypoint_names_to_coordinates")
        return -1
    
    waypoint_commands = waypoints_to_commands.waypoints_to_commands(waypoints, ALTITUDE)
    if len(waypoint_commands) == 0:
        print("Error: waypoints_to_commands")
        return -1
    
    takeoff_landing_commands = add_takeoff_and_landing_command.add_takeoff_and_landing_command(waypoint_commands, ALTITUDE)
    if len(takeoff_landing_commands) == 0:
        print("Error: add_takeoff_and_landing_command")
        return -1
    
    result = upload_commands.upload_commands(drone, takeoff_landing_commands)
    if not result:
        print("Error: upload_commands")
        return -1

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

        time.sleep(DELAY)

    return 0


if __name__ == "__main__":
    result_run = run()
    if result_run < 0:
        print("ERROR")
    print("Done")
