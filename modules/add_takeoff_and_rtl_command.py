"""
Prefixes a takeoff command and suffixes a RTL command to the end of the list of commands.
"""

import dronekit


MAVLINK_TAKEOFF_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
MAVLINK_RTL_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL
MAVLINK_TAKEOFF_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_TAKEOFF
MAVLINK_RTL_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH


def add_takeoff_and_rtl_command(commands: "list[dronekit.Command]",
                                    altitude: float) -> "tuple[bool, list[dronekit.Command] | None]":
    """
    Prepends a takeoff command and appends a RTL command to a list of dronekit commands.

    Parameters
    ----------
    commands: list[dronekit.Command]
        Dronekit commands that can be sent to the drone.
    altitude: int
        Altitude in meters to command the drone to.

    Returns
    -------
    tuple[bool, list[dronekit.Command] | None]: 
        (False, None) if empty commands list,
        (True, dronekit commands with takeoff and land commands that can be sent to the drone) otherwise.
    """
    if len(commands) == 0:
        return False, None

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

    rtl_command = dronekit.Command(
        0,
        0,
        0,
        MAVLINK_RTL_FRAME,
        MAVLINK_RTL_COMMAND,
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
    commands.append(rtl_command)

    return True, commands