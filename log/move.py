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
    move_logs: list[MoveLog] = []

    @classmethod
    def append_log(cls, move_log: MoveLog):
        cls.move_logs.append(move_log)

    @classmethod
    def append_to_csv(cls):
        headers = ["match_id", "color", "order", "x", "y", "time_spent", "moved", "valid", "retry_count"]
        with open("move_log.csv", "a") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            if not os.path.isfile("move_log.csv") or os.path.getsize("move_log.csv") == 0:
                writer.writeheader()

            for log in cls.move_logs:
                writer.writerow(log.__dict__)

        cls.move_logs.clear()


if __name__ == "__main__":
    # test
    MoveLogger.append_log(
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
    MoveLogger.append_log(
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
    MoveLogger.append_to_csv()

