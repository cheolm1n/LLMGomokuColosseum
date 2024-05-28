from dataclasses import dataclass

import csv
import os


@dataclass
class MoveLog:
    match_id: str
    color: str
    order: int
    x: int
    y: int
    time_spent: int
    moved: int
    valid: int
    retry_count: int


class MoveLogger:
    def __init__(self):
        self.move_logs: list[MoveLog] = []

    def append_log(self, move_log: MoveLog):
        self.move_logs.append(move_log)

    def append_to_csv(self):
        headers = ["match_id", "color", "order", "x", "y", "time_spent", "moved", "valid", "retry_count"]
        with open("move_log.csv", "a") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            if not os.path.isfile("move_log.csv") or os.path.getsize("move_log.csv") == 0:
                writer.writeheader()

            for log in self.move_logs:
                writer.writerow(log.__dict__)

        self.move_logs.clear()

    def clear(self):
        self.move_logs.clear()


if __name__ == "__main__":
    move_logger = MoveLogger()
    # test
    move_logger.append_log(
        MoveLog(
            match_id='test2',
            color='black',
            order=1,
            x=0,
            y=0,
            time_spent=1,
            moved=1,
            valid=1,
            retry_count=0
        )
    )
    move_logger.append_log(
        MoveLog(
            match_id='test2',
            color='black',
            order=1,
            x=0,
            y=0,
            time_spent=1,
            moved=1,
            valid=1,
            retry_count=0
        )
    )
    move_logger.append_to_csv()

