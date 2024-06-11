from game import Game
from player.claude_opus_player import ClaudeOpusPlayer
from player.google_gemini_pro_player import GoogleGeminiProPlayer
from player.meta_llama_3_70b_instruct_player import MetaLlamaThree70BInstructPlayer
from player.openai_gpt_four_omni_player import OpenAiGptFourOmniPlayer
from player.openai_gpt_four_turbo_player import OpenAiGptFourTurboPlayer
from player.openai_gpt_three_dot_five_turbo_player import OpenAiGptThreeDotFiveTurboPlayer
import asyncio


async def main():
    players1 = [
        OpenAiGptThreeDotFiveTurboPlayer(1, True),
        OpenAiGptFourOmniPlayer(1, True),
        ClaudeOpusPlayer(1, True),
        GoogleGeminiProPlayer(1, True),
        # OpenAiGptFourTurboPlayer(1, False)
        MetaLlamaThree70BInstructPlayer(1, True)
    ]

    players2 = [
        OpenAiGptThreeDotFiveTurboPlayer(2, True),
        OpenAiGptFourOmniPlayer(2, True),
        ClaudeOpusPlayer(2, True),
        GoogleGeminiProPlayer(2, True),
        # OpenAiGptFourTurboPlayer(2, False)
        MetaLlamaThree70BInstructPlayer(2, True)
    ]

    for i in range(len(players1)):
        for j in range(len(players2)):
            # 동일한 모델인 경우 경기를 하지 않음
            if i == j:
                continue

            player1 = players1[i]
            player2 = players2[j]

            for k in range(1, 4):  # 3판 경기
                match_description = f"{player1.__class__.__name__} vs {player2.__class__.__name__} - Match {k}"
                print(f"Starting {match_description}")
                error_count = 0
                while error_count < 3:
                    try:
                        game = Game(player1, player2)
                        winner = await game.play(match_description)
                        if winner:
                            print(f"Player{winner.player_number} [{winner.__class__.__name__}] wins the match!")
                        break
                    except Exception as e:
                        error_count += 1
                        print(f"Error occurred during {match_description}: {e}. Retry... ({error_count}/3)")

                if error_count == 3:
                    print(f"Skipping {match_description} after 3 failed attempts.")

if __name__ == "__main__":
    asyncio.run(main())
