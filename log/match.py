from dataclasses import dataclass

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
    def __init__(self):
        self.match_logs: list[MatchLog] = []

    def append_log(self, match_log: MatchLog):
        self.match_logs.append(match_log)

    def append_to_csv(self):
        headers = ["match_id", "white", "black", "started", "ended", "winner"]
        with open("match_log.csv", "a") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            if not os.path.isfile("match_log.csv") or os.path.getsize("match_log.csv") == 0:
                writer.writeheader()

            for log in self.match_logs:
                writer.writerow(log.__dict__)

        self.match_logs.clear()

    def clear(self):
        self.match_logs.clear()


if __name__ == "__main__":
    # test
    match_logger = MatchLogger()
    match_logger.append_log(
        MatchLog(
            match_id = 'test2',
            white = 'ClaudeOpusPlayer',
            black = 'GoogleGeminiProPlayer',
            started = 0,
            ended = 1,
            winner = 'ClaudeOpusPlayer'
        )
    )
    match_logger.append_log(
        MatchLog(
            match_id = 'test2',
            white = 'ClaudeOpusPlayer',
            black = 'GoogleGeminiProPlayer',
            started = 0,
            ended = 1,
            winner = 'ClaudeOpusPlayer'
        )
    )
    match_logger.append_to_csv()

