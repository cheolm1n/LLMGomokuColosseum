class LLMPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.history = []

    def get_move(self, board):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def add_history(self, content):
        self.history.append(content)
