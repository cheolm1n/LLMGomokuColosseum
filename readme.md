# About this
Inspired by the LLM Colosseum, I created the LLM Gomoku(Omok) Competition.

# Presentation slides:
https://docs.google.com/presentation/d/1NPmviwlpYiAffYz7Ztqqeqz706kRmw4BV9lIW0RayUg/edit?usp=sharing

# Dependencies 
```shell
pip install anthropic
pip install google.generativeai
pip install openai
pip install boto3 # For llama 3 70b AWS bedrock endpoint
pip install numpy
```
# How to play
1. API KEY environment settings

```shell
export OPENAI_API_KEY="blahblah..."
export GOOGLE_API_KEY="blahblah..."
export ANTHROPIC_API_KEY="blahblah..."
export AWS_ACCESS_KEY_ID="blahblah..."
export AWS_SECRET_ACCESS_KEY="blahblah..."
```

2. Player selection

Uncomment main.py and select player1 and player2.

```python
def main():
    # player1 = ClaudeOpusPlayer(1)
    player1 = GoogleGeminiProPlayer(1)
    # player1 = OpenAiGptFourTurboPlayer(1)
    # player1 = OpenAiGptThreeDotFiveTurboPlayer(1)

    # player2 = ClaudeOpusPlayer(2)
    # player2 = GoogleGeminiProPlayer(2)
    player2 = OpenAiGptFourOmniPlayer(2)
    # player2 = OpenAiGptThreeDotFiveTurboPlayer(2)

    game = Game(player1, player2)
    winner = game.play()
    if winner:
        print(f"Player {winner} wins the match!")
```

3. Run

```python
python main.py
```
