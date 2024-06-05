from dataclasses import dataclass, asdict
from datetime import datetime

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
    position: str
    reason: str


class MoveLogger:
    def __init__(self, name:str):
        self.move_logs: list[MoveLog] = []
        self.name = name

    def __enter__(self):
        if not self.name:
            self.name = datetime.now().strftime('%Y%m%d%H%M%S')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        headers = ["match_id", "color", "order", "time_spent", "moved", "valid", "retry_count", "x", "y", "position", "reason"]
        if not os.path.exists(os.path.join(os.getcwd(), "logs")):
            os.mkdir(os.path.join(os.getcwd(), "logs"))

        if not os.path.exists(os.path.join(os.getcwd(), "logs", self.name)):
            os.mkdir(os.path.join(os.getcwd(), "logs", self.name))

        with open(os.path.join(os.getcwd(), "logs", self.name, "move_log.csv"), "w") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

            for log in self.move_logs:
                writer.writerow(asdict(log))

        self.move_logs.clear()

    def append_log(self, move_log: MoveLog):
        self.move_logs.append(move_log)


if __name__ == "__main__":
    with MoveLogger("test") as move_logger:
        move_logger.append_log(
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
                position="T1",
                reason='test'
            )
        )
