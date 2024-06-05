from dataclasses import dataclass, asdict
from datetime import datetime

import csv
import os


@dataclass
class MatchLog:
    match_id: str
    white: str
    black: str
    started: int
    ended: int
    winner: str


class MatchLogger:
    def __init__(self, name:str):
        self.match_logs: list[MatchLog] = []
        self.name = name

    def __enter__(self):
        if not self.name:
            self.name = datetime.now().strftime('%Y%m%d%H%M%S')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        headers = ["match_id", "white", "black", "started", "ended", "winner"]
        if not os.path.exists(os.path.join(os.getcwd(), "logs")):
            os.mkdir(os.path.join(os.getcwd(), "logs"))

        if not os.path.exists(os.path.join(os.getcwd(), "logs", self.name)):
            os.mkdir(os.path.join(os.getcwd(), "logs", self.name))

        with open(os.path.join(os.getcwd(), "logs", self.name, "match_log.csv"), "w") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

            for log in self.match_logs:
                writer.writerow(asdict(log))

        self.match_logs.clear()

    def append_log(self, match_log: MatchLog):
        self.match_logs.append(match_log)


if __name__ == "__main__":
    with MatchLogger("test") as match_logger:
        match_logger.append_log(
            MatchLog(
                match_id='test2',
                white='ClaudeOpusPlayer',
                black='GoogleGeminiProPlayer',
                started=0,
                ended=1,
                winner='ClaudeOpusPlayer'
            )
        )
