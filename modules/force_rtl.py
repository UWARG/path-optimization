"""
Forces drone to return to launch (RTL).
"""

import dronekit

from . import upload_commands
from . import generate_command

MAVLINK_RTL_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL
MAVLINK_RTL_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH
DRONE_TIMEOUT = 30.0  # seconds


def force_rtl(drone: dronekit.Vehicle) -> bool:
    """
    Sends RTL command using the upload_command module.

    Parameters
    -----------
    drone: dronekit.Vehicle
        The connected drone.

    Returns
    -------
    bool: True if uploading RTL command is successful, False otherwise.
    """

    # Generate and set RTL command
    rtl_command = generate_command.return_to_launch()

    # Change drone mode
    drone.mode = dronekit.VehicleMode("RTL")

    # Utilize upload_command function to give RTL command to drone
    result = upload_commands.upload_commands(drone, [rtl_command], DRONE_TIMEOUT)

    # Error if unsuccessful
    if not result:
        print("Unable to upload RTL command to drone command sequence.")

    return result
