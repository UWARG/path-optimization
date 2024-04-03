"""
Checks whether the drone has reached its max flight time and sends it back to launch.
"""

import time

from . import condition


class MissionTimeCondition(condition.Condition):
    """
    Checks if drone exceeds the maximum flight time limit, inherits from Evaluate class
    """

    __create_key = object()

    @classmethod
    def create(
        cls, start_time: "float | None", maximum_flight_time: "float | None"
    ) -> "tuple[bool, MissionTimeCondition | None]":
        """
        start_time: float
            The time the drone started the mission in seconds.
         maximum_flight_time: float
            Max flight time for drone in seconds.
        """
        if start_time is None:
            return False, None

        if maximum_flight_time is None:
            return False, None

        return True, MissionTimeCondition(cls.__create_key, start_time, maximum_flight_time)

    def __init__(
        self, class_private_create_key: object, start_time: float, maximum_flight_time: float
    ) -> None:
        """
        Private constructor, use create() method
        """
        assert class_private_create_key is MissionTimeCondition.__create_key
        self.start_time = start_time
        self.maximum_flight_time = maximum_flight_time

    def evaluate_condition(self) -> bool:
        """
        Evaluates whether the drone should land based on time remaining.
        """
        current_time = time.time()
        if current_time - self.start_time < self.maximum_flight_time:
            return False

        return True

    def output_time_elapsed(self) -> None:
        """
        Outputs the total time elapsed during the mission.
        """
        current_time = time.time()
        print(f"Elapsed time (s): {current_time - self.start_time}")

    def message(self) -> None:
        """
        Outputs status when the drone has exceeded the time limit.
        """
        print("This mission has exceeded the maximum flight time limit.")
        print(f"Specified maximum flight time limit: {self.maximum_flight_time}")
        print(f"Mission start time: {self.start_time}")
        print(f"Time when condition was met: {time.time()}")
