from game import play_game
from player.claude_opus_player import ClaudeOpusPlayer
from player.google_gemini_pro_player import GoogleGeminiProPlayer
from player.openai_gpt_four_turbo_player import OpenAiGptFourTurboPlayer
from player.openai_three_dot_five_turbo_player import OpenAiGptThreeDotFiveTurboPlayer


def main():
    # player1 = ClaudeOpusPlayer(1)
    player1 = GoogleGeminiProPlayer(1)
    # player1 = OpenAiGptFourTurboPlayer(1)
    # player1 = OpenAiGptThreeDotFiveTurboPlayer(1)

    # player2 = ClaudeOpusPlayer(2)
    # player2 = GoogleGeminiProPlayer(2)
    player2 = OpenAiGptFourTurboPlayer(2)
    # player2 = OpenAiGptThreeDotFiveTurboPlayer(2)

    winner = play_game(player1, player2)
    if winner:
        print(f"Player {winner} wins the match!")


if __name__ == "__main__":
    main()
