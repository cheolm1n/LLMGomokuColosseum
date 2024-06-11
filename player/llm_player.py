from geval import evaluate


class LLMPlayer:
    def __init__(self, player_number: int):
        self.player_number = player_number
        self.history = []

    async def get_move(self, record) -> tuple[int, int, str, str, float, str]:
        raise NotImplementedError("This method should be implemented by subclasses.")

    def add_history(self, content):
        self.history.append(content)

    @staticmethod
    def gen_evaluate(prompt, gen_output):
        return evaluate(prompt, gen_output)
