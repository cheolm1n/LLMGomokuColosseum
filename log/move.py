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
    geval_score: float
    geval_reason: str


class MoveLogger:
    def __init__(self, name:str):
        self.move_logs: list[MoveLog] = []
        self.name = name

    def __enter__(self):
        if not self.name:
            self.name = datetime.now().strftime('%Y%m%d%H%M%S')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        headers = ["match_id", "color", "order", "time_spent", "moved", "valid", "retry_count", "x", "y", "position", "reason", "geval_score", "geval_reason"]
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

    def get_geval_average(self):
        # 모든 move_logs에서 black과 white 플레이어의 geval_score를 분리하여 저장
        black_scores = [log.geval_score for log in self.move_logs if log.color == 'black']
        white_scores = [log.geval_score for log in self.move_logs if log.color == 'white']

        # 각 플레이어의 평균 점수를 계산
        black_avg = sum(black_scores) / len(black_scores) if black_scores else 0
        white_avg = sum(white_scores) / len(white_scores) if white_scores else 0
        total_avg = sum([log.geval_score for log in self.move_logs]) / len(self.move_logs)
        return {total_avg, black_avg, white_avg}


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
                reason='test',
                geval_score=1.0,
                geval_reason='test'
            )
        )
