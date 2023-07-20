"""
Prefixes a takeoff command and suffixes a landing command to the end of the list of commands.
"""

import dronekit


MAVLINK_TAKEOFF_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
MAVLINK_LANDING_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL
MAVLINK_TAKEOFF_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_TAKEOFF
MAVLINK_LANDING_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH


def add_takeoff_and_landing_command(commands: "list[dronekit.Command]",
                                    altitude: float) -> "list[dronekit.Command]":
    """
    Prepends a takeoff command and appends a landing command to a list of dronekit commands

    Parameters
    ----------
    commands: list[dronekit.Command]
        Dronekit commands that can be sent to the drone.
    altitude: int
        Altitude in meters to command the drone to.

    Returns
    -------
    list[dronekit.Command]
        Dronekit commands with takeoff and land commands that can be sent to the drone.
    """
    takeoff_command = dronekit.Command(
        0,
        0,
        0,
        MAVLINK_TAKEOFF_FRAME,
        MAVLINK_TAKEOFF_COMMAND,
        0,
        0,
        0,  # param1
        0,
        0,
        0,
        0,
        0,
        altitude,
    )
    commands.insert(0, takeoff_command)

    landing_command = dronekit.Command(
        0,
        0,
        0,
        MAVLINK_LANDING_FRAME,
        MAVLINK_LANDING_COMMAND,
        0,
        0,
        0,  # param1
        0,
        0,
        0,
        0,
        0,
        0,
    )
    commands.append(landing_command)

    return commands
