from game import Game
from player.claude_opus_player import ClaudeOpusPlayer
from player.google_gemini_pro_player import GoogleGeminiProPlayer
from player.meta_llama_3_70b_instruct_player import MetaLlamaThree70BInstructPlayer
from player.openai_gpt_four_omni_player import OpenAiGptFourOmniPlayer
from player.openai_gpt_four_turbo_player import OpenAiGptFourTurboPlayer
from player.openai_gpt_three_dot_five_turbo_player import OpenAiGptThreeDotFiveTurboPlayer
import asyncio


async def main():
    # player1 = ClaudeOpusPlayer(1, False)
    # player1 = GoogleGeminiProPlayer(1, True)
    # player1 = OpenAiGptFourTurboPlayer(1, False)
    player1 = OpenAiGptThreeDotFiveTurboPlayer(1, True)
    # player1 = MetaLlamaThree70BInstructPlayer(1, False)

    # player2 = ClaudeOpusPlayer(2, False)
    # player2 = GoogleGeminiProPlayer(2, False)
    player2 = OpenAiGptFourOmniPlayer(2, True)
    # player2 = OpenAiGptThreeDotFiveTurboPlayer(2, False)
    # player2 = MetaLlamaThree70BInstructPlayer(2, False)

    game = Game(player1, player2)
    winner = await game.play()
    if winner:
        print(f"Player{winner.player_number} [{winner.__class__.__name__}] wins the match!")


if __name__ == "__main__":
    asyncio.run(main())
