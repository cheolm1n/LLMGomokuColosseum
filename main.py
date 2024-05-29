from game import Game
from player.claude_opus_player import ClaudeOpusPlayer
from player.google_gemini_pro_player import GoogleGeminiProPlayer
from player.openai_gpt_four_omni_player import OpenAiGptFourOmniPlayer
from player.openai_gpt_four_turbo_player import OpenAiGptFourTurboPlayer
from player.openai_gpt_three_dot_five_turbo_player import OpenAiGptThreeDotFiveTurboPlayer


def main():
    # player1 = ClaudeOpusPlayer(1)
    # player1 = GoogleGeminiProPlayer(1)
    # player1 = OpenAiGptFourTurboPlayer(1)
    player1 = OpenAiGptThreeDotFiveTurboPlayer(1)

    # player2 = ClaudeOpusPlayer(2)
    # player2 = GoogleGeminiProPlayer(2)
    player2 = OpenAiGptFourOmniPlayer(2)
    # player2 = OpenAiGptThreeDotFiveTurboPlayer(2)

    game = Game(player1, player2)
    winner = game.play(log_move=True, log_match=True)
    if winner:
        print(f"Player {winner} wins the match!")


if __name__ == "__main__":
    main()
