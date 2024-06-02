# 명백히 이길 수 있는 상황에서 이길 수 있는 수를 두는지에 대한 테스트 벤치마크
from player.llm_player import LLMPlayer
from player.openai_gpt_three_dot_five_turbo_player import OpenAiGptThreeDotFiveTurboPlayer
from record import Record


def obvious_record(test_player: LLMPlayer):
    opponent_player = OpenAiGptThreeDotFiveTurboPlayer()
    record = Record()
    record.add(player=test_player, x=7, y=7, valid=True, reason="")


def test():
    repeat = 30




if __name__ == "__main__":
    test()
