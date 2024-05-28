from dataclasses import dataclass

import csv
import os


@dataclass
class MoveLog:
    match_id: str
    color: str
    order: int
    time_spent: int
    moved: int
    valid: int
    retry_count: int
    x: int
    y: int
    reason: str


class MoveLogger:
    move_logs: list[MoveLog] = []

    @classmethod
    def append_log(cls, move_log: MoveLog):
        cls.move_logs.append(move_log)

    @classmethod
    def append_to_csv(cls):
        headers = ["match_id", "color", "order", "time_spent", "moved", "valid", "retry_count", "x", "y", "reason"]
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
            time_spent=1,
            moved=1,
            valid=1,
            retry_count=0,
            x=0,
            y=0,
            reason='test'
        )
    )
    MoveLogger.append_log(
        MoveLog(
            match_id='test2',
            color='black',
            order=1,
            time_spent=1,
            moved=1,
            valid=1,
            retry_count=0,
            x=0,
            y=0,
            reason='test'
        )
    )
    MoveLogger.append_to_csv()
