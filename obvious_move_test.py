# 명백히 이길 수 있는 상황에서 이길 수 있는 수를 두는지에 대한 테스트 벤치마크
from player.llm_player import LLMPlayer
from player.openai_gpt_three_dot_five_turbo_player import OpenAiGptThreeDotFiveTurboPlayer
from player.openai_gpt_four_turbo_player import OpenAiGptFourTurboPlayer
from player.openai_gpt_four_omni_player import OpenAiGptFourOmniPlayer
from player.claude_opus_player import ClaudeOpusPlayer
from player.google_gemini_pro_player import GoogleGeminiProPlayer
from player.meta_llama_3_70b_instruct_player import MetaLlamaThree70BInstructPlayer
from player.llm_player import LLMPlayer
from util import InvalidPositionException
from record import Record


def obvious_record(test_player: LLMPlayer) -> Record:
    opponent_player = OpenAiGptThreeDotFiveTurboPlayer(2)
    record = Record()
    record.add(player=test_player, x=7, y=7, valid=True, reason="")
    record.add(player=opponent_player, x=7, y=6, valid=True, reason="")
    record.add(player=test_player, x=7, y=8, valid=True, reason="To strengthen horizontally from the starting position H8")
    record.add(player=opponent_player, x=6, y=7, valid=True, reason="To add possibilities in the diagonal direction from G8")
    record.add(player=test_player, x=7, y=9, valid=True, reason="To strengthen the horizaontal direction with three stones")
    record.add(player=opponent_player, x=8, y=7, valid=True, reason="To add the possibility of diagonal orientation")
    record.add(player=test_player, x=7, y=10, valid=True, reason="Connect 4 stones horizontally from H8 to K8 to make 5 stones later to win")
    record.add(player=opponent_player, x=9, y=8, valid=True, reason="To add the possibility of winning by connecting three stones in diagonal direictions from G8 to I10")
    return record


def test():
    repeat = 10
    winning_position = (7, 11)
    test_players: list[LLMPlayer] = [
        OpenAiGptThreeDotFiveTurboPlayer(1),
        OpenAiGptFourOmniPlayer(1),
        OpenAiGptFourTurboPlayer(1),
        # ClaudeOpusPlayer(1),
        # GoogleGeminiProPlayer(1),
        # MetaLlamaThree70BInstructPlayer(1)
    ]
    results: dict[str, list[bool]] = {}

    for test_player in test_players:
        name = test_player.__class__.__name__
        results[name] = []
        record = obvious_record(test_player)
        for _ in range(repeat):
            win = False
            try:
                res_x, res_y, _ = test_player.get_move(record)
                if (res_x, res_y) == winning_position:
                    win = True
            except (InvalidPositionException, KeyError):
                win = False
            
            results[name].append(win)

    for name, result in results.items():
        print(f"name: {name}, win: {result.count(True)}/{len(result)}")


if __name__ == "__main__":
    test()
    
