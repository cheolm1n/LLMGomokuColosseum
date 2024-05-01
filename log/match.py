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
    match_logs: list[MatchLog] = []

    @classmethod
    def append_log(cls, match_log: MatchLog):
        cls.match_logs.append(match_log)

    @classmethod
    def append_to_csv(cls):
        headers = ["match_id", "white", "black", "started", "ended", "winner"]
        with open("match_log.csv", "a") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            if not os.path.isfile("match_log.csv") or os.path.getsize("match_log.csv") == 0:
                writer.writeheader()

            for log in cls.match_logs:
                writer.writerow(log.__dict__)

        cls.match_logs.clear()


if __name__ == "__main__":
    # test
    MatchLogger.append_log(
        MatchLog(
            match_id = 'test2',
            white = 'ClaudeOpusPlayer',
            black = 'GoogleGeminiProPlayer',
            started = 0,
            ended = 1,
            winner = 'ClaudeOpusPlayer'
        )
    )
    MatchLogger.append_log(
        MatchLog(
            match_id = 'test2',
            white = 'ClaudeOpusPlayer',
            black = 'GoogleGeminiProPlayer',
            started = 0,
            ended = 1,
            winner = 'ClaudeOpusPlayer'
        )
    )
    MatchLogger.append_to_csv()

