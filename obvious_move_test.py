import threading
import asyncio
from player.llm_player import LLMPlayer
from player.openai_gpt_three_dot_five_turbo_player import OpenAiGptThreeDotFiveTurboPlayer
from player.openai_gpt_four_turbo_player import OpenAiGptFourTurboPlayer
from player.openai_gpt_four_omni_player import OpenAiGptFourOmniPlayer
from player.claude_opus_player import ClaudeOpusPlayer
from player.google_gemini_pro_player import GoogleGeminiProPlayer
from player.meta_llama_3_70b_instruct_player import MetaLlamaThree70BInstructPlayer
from util import InvalidPositionException
from record import Record


class Problem:
    def __init__(self, title: str, record_func, winning_position):
        self.title = title
        self.record_func = record_func
        self.winning_position = winning_position

    def create_record(self, player: LLMPlayer) -> Record:
        return self.record_func(player)

# 인간이 작성한 reason
# def horizontal_record(test_player: LLMPlayer) -> Record:
#     opponent_player = OpenAiGptThreeDotFiveTurboPlayer(2)
#     record = Record()
#     record.add(player=test_player, x=7, y=7, valid=True, reason="")
#     record.add(player=opponent_player, x=7, y=6, valid=True, reason="")
#     record.add(player=test_player, x=7, y=8, valid=True, reason="To strengthen horizontally from the starting position H8")
#     record.add(player=opponent_player, x=6, y=7, valid=True, reason="To add possibilities in the diagonal direction from G8")
#     record.add(player=test_player, x=7, y=9, valid=True, reason="To strengthen the horizontal direction with three stones")
#     record.add(player=opponent_player, x=8, y=7, valid=True, reason="To add the possibility of diagonal orientation")
#     record.add(player=test_player, x=7, y=10, valid=True, reason="Connect 4 stones horizontally from H8 to K8 to make 5 stones later to win")
#     record.add(player=opponent_player, x=9, y=8, valid=True, reason="To add the possibility of winning by connecting three stones in diagonal directions from G8 to I10")
#     return record


def horizontal_record(test_player: LLMPlayer) -> Record:
    opponent_player = OpenAiGptThreeDotFiveTurboPlayer(2)
    record = Record()
    record.add(player=test_player, x=7, y=7, valid=True, reason="# Current Sequences: Initiating a new game with a placement at (7,7). # Strategy: Placing the stone at (7,7) to start building central control and apply early pressure. # Best Move: (7,7) # Reason: Placing the stone at (7,7) provides a strategic position for potential vertical, horizontal, and diagonal expansions. # Long-Term Plan: Establish an early sequence to control the center and prepare for branching attacks.")
    record.add(player=opponent_player, x=7, y=6, valid=True, reason="")
    record.add(player=test_player, x=7, y=8, valid=True, reason="# Current Sequences: Player 1 has placed stones at (7,7) and (7,8), forming a vertical sequence. # Strategy: Placing the stone at (7,8) to extend the vertical sequence and build central control. # Best Move: (7,8) # Reason: Placing the stone at (7,8) enhances vertical and diagonal threats. # Long-Term Plan: Build strong vertical sequences to create multiple winning opportunities and central dominance.")
    record.add(player=opponent_player, x=6, y=7, valid=True, reason="")
    record.add(player=test_player, x=7, y=9, valid=True, reason="# Current Sequences: Player 1 has placed stones at (7,8) and (7,9), forming a strong vertical threat. # Strategy: Placing the stone at (7,9) to extend the vertical sequence and pressure the opponent's defense. # Best Move: (7,9) # Reason: Placing the stone at (7,9) reinforces vertical threats and creates potential for horizontal and diagonal expansions. # Long-Term Plan: Continue building vertical sequences to maintain pressure and open up new attack lines.")
    record.add(player=opponent_player, x=8, y=7, valid=True, reason="")
    record.add(player=test_player, x=7, y=10, valid=True, reason="# Current Sequences: Player 1 has placed stones at (7,9) and (7,10), forming a strong vertical sequence. # Strategy: Placing the stone at (7,10) to continue the vertical build and create multiple threats. # Best Move: (7,10) # Reason: Placing the stone at (7,10) strengthens the vertical sequence, increasing pressure on the opponent. # Long-Term Plan: Maintain vertical dominance to control the board and open up additional attacking opportunities.")
    record.add(player=opponent_player, x=9, y=8, valid=True, reason="")
    return record


def diagonal_record(test_player: LLMPlayer) -> Record:
    opponent_player = OpenAiGptThreeDotFiveTurboPlayer(2)
    record = Record()
    record.add(player=test_player, x=7, y=7, valid=True, reason="# Current Sequences: Initiating a new game with a placement at (7,7). # Strategy: Placing the stone at (7,7) to start building a central control and apply early pressure. # Best Move: (7,7) # Reason: Placing the stone at (7,7) provides a strategic position for potential vertical, horizontal, and diagonal expansions. # Long-Term Plan: Establish an early sequence to control the center and prepare for branching attacks.")
    record.add(player=opponent_player, x=7, y=8, valid=True, reason="")
    record.add(player=test_player, x=8, y=8, valid=True, reason="# Current Sequences: Player 1 has placed stones at (7,7) and (8,8), forming a diagonal sequence. # Strategy: Placing the stone at (8,8) to connect sequences and build central control. # Best Move: (8,8) # Reason: Placing the stone at (8,8) enhances diagonal and vertical threats. # Long-Term Plan: Build strong diagonal sequences to create multiple winning opportunities and central dominance.")
    record.add(player=opponent_player, x=6, y=8, valid=True, reason="")
    record.add(player=test_player, x=9, y=9, valid=True, reason="# Current Sequences: Player 1 has placed stones at (8,8) and (9,9), forming a diagonal and potential vertical threat. # Strategy: Placing the stone at (9,9) to extend the diagonal sequence and block the opponent's horizontal expansion. # Best Move: (9,9) # Reason: Placing the stone at (9,9) strengthens diagonal and vertical threats. # Long-Term Plan: Extend diagonal sequences to dominate central lines and force defensive moves from the opponent.")
    record.add(player=opponent_player, x=6, y=6, valid=True, reason="")
    record.add(player=test_player, x=10, y=8, valid=True, reason="# Current Sequences: Player 1 has placed stones at (9,9) and (10,8), forming potential diagonal and horizontal threats. # Strategy: Placing the stone at (10,8) to build horizontal sequence and apply pressure. # Best Move: (10,8) # Reason: Placing the stone at (10,8) balances diagonal and horizontal threats, complicating the opponent's defense. # Long-Term Plan: Develop both horizontal and diagonal sequences to create a robust attacking position.")
    record.add(player=opponent_player, x=6, y=7, valid=True, reason="")
    record.add(player=test_player, x=10, y=10, valid=True, reason="# Current Sequences: Player 1 has placed stones at (10,8) and (10,10), forming a strong diagonal threat. # Strategy: Placing the stone at (10,10) to extend diagonal sequence and pressure opponent's defense. # Best Move: (10,10) # Reason: Placing the stone at (10,10) reinforces diagonal threats and creates potential for horizontal and vertical expansions. # Long-Term Plan: Continue building diagonal sequences to maintain pressure and open up new attack lines.")
    record.add(player=opponent_player, x=6, y=5, valid=True, reason="")
    return record


def vertical_record(test_player: LLMPlayer) -> Record:
    opponent_player = OpenAiGptThreeDotFiveTurboPlayer(2)
    record = Record()
    record.add(player=test_player, x=7, y=7, valid=True, reason="# Current Sequences: Initiating a new game with a placement at (7,7). # Strategy: Placing the stone at (7,7) to start building a central control and apply early pressure. # Best Move: (7,7) # Reason: Placing the stone at (7,7) provides a strategic position for potential vertical, horizontal, and diagonal expansions. # Long-Term Plan: Establish an early sequence to control the center and prepare for branching attacks.")
    record.add(player=opponent_player, x=8, y=7, valid=True, reason="")
    record.add(player=test_player, x=8, y=8, valid=True, reason="# Current Sequences: Player 1 has placed stones at (7,7) and (8,8), forming a diagonal sequence. # Strategy: Placing the stone at (8,8) to connect sequences and build central control. # Best Move: (8,8) # Reason: Placing the stone at (8,8) enhances diagonal and vertical threats. # Long-Term Plan: Build strong diagonal sequences to create multiple winning opportunities and central dominance.")
    record.add(player=opponent_player, x=7, y=8, valid=True, reason="")
    record.add(player=test_player, x=8, y=9, valid=True, reason="# Current Sequences: Player 1 has placed stones at (8,8) and (8,9), forming a vertical and diagonal threat. # Strategy: Placing the stone at (8,9) to extend the vertical sequence and block the opponent's horizontal expansion. # Best Move: (8,9) # Reason: Placing the stone at (8,9) strengthens vertical and diagonal threats. # Long-Term Plan: Extend vertical sequences to dominate central lines and force defensive moves from the opponent.")
    record.add(player=opponent_player, x=9, y=6, valid=True, reason="")
    record.add(player=test_player, x=6, y=9, valid=True, reason="# Current Sequences: Player 1 has placed stones at (8,9) and (6,9), forming potential vertical and horizontal threats. # Strategy: Placing the stone at (6,9) to build horizontal sequence and apply pressure. # Best Move: (6,9) # Reason: Placing the stone at (6,9) balances vertical and horizontal threats, complicating the opponent's defense. # Long-Term Plan: Develop both horizontal and vertical sequences to create a robust attacking position.")
    record.add(player=opponent_player, x=8, y=6, valid=True, reason="")
    record.add(player=test_player, x=8, y=10, valid=True, reason="# Current Sequences: Player 1 has placed stones at (8,9) and (8,10), forming a strong vertical threat. # Strategy: Placing the stone at (8,10) to extend vertical sequence and pressure opponent's defense. # Best Move: (8,10) # Reason: Placing the stone at (8,10) reinforces vertical threats and creates potential for horizontal and diagonal expansions. # Long-Term Plan: Continue building vertical sequences to maintain pressure and open up new attack lines.")
    record.add(player=opponent_player, x=10, y=6, valid=True, reason="")
    record.add(player=test_player, x=8, y=11, valid=True, reason="# Current Sequences: Player 1 has placed stones at (8,10) and (8,11), forming a strong vertical sequence. # Strategy: Placing the stone at (8,11) to continue vertical build and create multiple threats. # Best Move: (8,11) # Reason: Placing the stone at (8,11) strengthens the vertical sequence, increasing pressure on the opponent. # Long-Term Plan: Maintain vertical dominance to control the board and open up additional attacking opportunities.")
    record.add(player=opponent_player, x=7, y=6, valid=True, reason="")
    return record


def two_x_two_record(test_player: LLMPlayer) -> Record:
    opponent_player = OpenAiGptThreeDotFiveTurboPlayer(2)
    record = Record()
    record.add(player=test_player, x=8, y=9, valid=True, reason="# Current Sequences: Initiating a new game with a placement at (8,9). # Strategy: Placing the stone at (8,9) to start building central control and apply early pressure. # Best Move: (8,9) # Reason: Placing the stone at (8,9) provides a strategic position for potential vertical, horizontal, and diagonal expansions. # Long-Term Plan: Establish an early sequence to control the center and prepare for branching attacks.")
    record.add(player=opponent_player, x=7, y=8, valid=True, reason="")
    record.add(player=test_player, x=8, y=8, valid=True, reason="# Current Sequences: Player 1 has placed stones at (8,9) and (8,8), forming a vertical sequence. # Strategy: Placing the stone at (8,8) to extend the vertical sequence and build central control. # Best Move: (8,8) # Reason: Placing the stone at (8,8) enhances vertical and diagonal threats. # Long-Term Plan: Build strong vertical sequences to create multiple winning opportunities and central dominance.")
    record.add(player=opponent_player, x=7, y=9, valid=True, reason="")
    record.add(player=test_player, x=7, y=10, valid=True, reason="# Current Sequences: Player 1 has placed stones at (8,9) and (7,10), forming a potential diagonal threat. # Strategy: Placing the stone at (7,10) to extend the diagonal sequence and pressure the opponent's defense. # Best Move: (7,10) # Reason: Placing the stone at (7,10) reinforces diagonal threats and creates potential for vertical and horizontal expansions. # Long-Term Plan: Continue building diagonal sequences to maintain pressure and open up new attack lines.")
    record.add(player=opponent_player, x=6, y=10, valid=True, reason="")
    record.add(player=test_player, x=8, y=11, valid=True, reason="# Current Sequences: Player 1 has placed stones at (8,9) and (8,11), forming a vertical sequence. # Strategy: Placing the stone at (8,11) to continue the vertical build and create multiple threats. # Best Move: (8,11) # Reason: Placing the stone at (8,11) strengthens the vertical sequence, increasing pressure on the opponent. # Long-Term Plan: Maintain vertical dominance to control the board and open up additional attacking opportunities.")
    record.add(player=opponent_player, x=7, y=11, valid=True, reason="")
    record.add(player=test_player, x=8, y=12, valid=True, reason="# Current Sequences: Player 1 has placed stones at (8,11) and (8,12), forming a strong vertical sequence. # Strategy: Placing the stone at (8,12) to extend the vertical sequence and maintain pressure. # Best Move: (8,12) # Reason: Placing the stone at (8,12) reinforces the vertical threat and forces the opponent to respond defensively. # Long-Term Plan: Continue building vertical sequences to secure a winning path and keep the opponent on the defensive.")
    record.add(player=opponent_player, x=5, y=11, valid=True, reason="")
    return record


def three_x_one_record(test_player: LLMPlayer) -> Record:
    opponent_player = OpenAiGptThreeDotFiveTurboPlayer(2)
    record = Record()
    record.add(player=test_player, x=8, y=8, valid=True, reason="# Current Sequences: Initiating a new game with a central placement. # Strategy: Placing the stone at (8,8) establishes central control and provides numerous options for future sequences. # Best Move: (8,8) # Reason: Placing the stone at (8,8) provides a strategic advantage by occupying the center, allowing for both offensive and defensive maneuvers. # Long-Term Plan: Utilize central control to create multiple branching sequences and apply pressure across the board.")
    record.add(player=opponent_player, x=9, y=8, valid=True, reason="")
    record.add(player=test_player, x=8, y=7, valid=True, reason="# Current Sequences: Player 1 has placed stones at (8,8) and (8,7), forming a vertical sequence. # Strategy: Extending the vertical sequence to build a potential winning line and block horizontal expansion by the opponent. # Best Move: (8,7) # Reason: Placing the stone at (8,7) continues the vertical build and limits the opponent's horizontal development. # Long-Term Plan: Strengthen vertical sequences to create pressure and force the opponent into defensive positions.")
    record.add(player=opponent_player, x=9, y=7, valid=True, reason="")
    record.add(player=test_player, x=8, y=6, valid=True, reason="# Current Sequences: Player 1 has placed stones at (8,8), (8,7), and (8,6), forming a strong vertical line. # Strategy: Extending the vertical sequence to increase pressure and create multiple winning threats. # Best Move: (8,6) # Reason: Placing the stone at (8,6) strengthens the vertical line, making it harder for the opponent to block all potential wins. # Long-Term Plan: Create multiple vertical threats to diversify winning opportunities and maintain offensive momentum.")
    record.add(player=opponent_player, x=8, y=9, valid=True, reason="")
    record.add(player=test_player, x=9, y=6, valid=True, reason="# Current Sequences: Player 1 has placed stones at (8,8), (8,7), (8,6), and (9,6), forming potential horizontal and vertical threats. # Strategy: Expanding the horizontal threat to complement the vertical sequence, creating dual threats. # Best Move: (9,6) # Reason: Placing the stone at (9,6) balances vertical and horizontal pressure, complicating the opponent's defensive options. # Long-Term Plan: Develop both horizontal and vertical sequences to create a robust attacking position.")
    record.add(player=opponent_player, x=10, y=7, valid=True, reason="")
    record.add(player=test_player, x=11, y=6, valid=True, reason="# Current Sequences: Player 1 has established multiple sequences, including a potential horizontal line. # Strategy: Extending the horizontal sequence to increase winning threats and force the opponent into a defensive position. # Best Move: (11,6) # Reason: Placing the stone at (11,6) enhances the horizontal threat, requiring the opponent to address multiple potential wins. # Long-Term Plan: Maximize horizontal pressure to create a direct path to victory while maintaining alternative sequence options.")
    record.add(player=opponent_player, x=9, y=9, valid=True, reason="")
    record.add(player=test_player, x=7, y=6, valid=True, reason="# Current Sequences: Player 1 has built a horizontal threat from (8,6) and (9,6). # Strategy: Extending the horizontal sequence and preparing for a four-stone line. # Best Move: (7,6) # Reason: Placing the stone at (7,6) strengthens the horizontal sequence and sets up a potential four-stone line, pressuring the opponent. # Long-Term Plan: Continue building the horizontal sequence while preparing to pivot to vertical or diagonal threats as necessary.")
    record.add(player=opponent_player, x=9, y=10, valid=True, reason="")
    return record


async def test_player_async(test_player: LLMPlayer, problem: Problem, repeat: int, results: dict[str, dict[str, list[bool]]]):
    name = test_player.__class__.__name__
    if name not in results:
        results[name] = {}
    if problem.title not in results[name]:
        results[name][problem.title] = []
    record = problem.create_record(test_player)

    # 요청 동시성 제한
    semaphore = asyncio.Semaphore(2)

    # 결과 도착순서 카운터
    lock = threading.Lock()
    count = 0

    async def run_test(i):
        nonlocal count
        win = False
        async with semaphore:
            try:
                res_x, res_y, _ = await test_player.get_move(record)

                with lock:
                    count += 1
                    print(f"{name} - {problem.title}: {count}/{repeat}")
                if (res_x, res_y) == problem.winning_position:
                    win = True
            except (InvalidPositionException, KeyError):
                win = False
            results[name][problem.title].append(win)

    tasks = [run_test(i) for i in range(repeat)]
    await asyncio.gather(*tasks)


async def test():
    repeat = 5
    problems = [
        Problem("Horizontal Winning Move", horizontal_record, (7, 11)),
        Problem("Diagonal Winning Move", diagonal_record, (11, 10)),
        Problem("Vertical Winning Move", vertical_record, (8, 12)),
        Problem("2x2 Winning Move", two_x_two_record, (8, 10)),
        Problem("3x1 Winning Move", three_x_one_record, (10, 6))
    ]
    test_players: list[LLMPlayer] = [
        OpenAiGptFourOmniPlayer(1),
        OpenAiGptFourTurboPlayer(1),
        OpenAiGptThreeDotFiveTurboPlayer(1),
        MetaLlamaThree70BInstructPlayer(1),
        # ClaudeOpusPlayer(1)
    ]
    results: dict[str, dict[str, list[bool]]] = {}

    tasks = []
    for problem in problems:
        for player in test_players:
            tasks.append(test_player_async(player, problem, repeat, results))

    await asyncio.gather(*tasks)

    total_scores = {name: {problem: sum(result) for problem, result in problems_results.items()} for name, problems_results in results.items()}
    total_tests = repeat * len(problems)

    for name, problems_results in results.items():
        for problem_title, result in problems_results.items():
            print(f"Player: {name}, Problem: {problem_title}, Wins: {result.count(True)}/{len(result)}, Score: {sum(result)}/{len(result)}")

    print("\nTotal Scores:")
    for name, problem_scores in total_scores.items():
        total_score = sum(problem_scores.values())
        print(f"{name}: {total_score}/{total_tests}")


if __name__ == "__main__":
    asyncio.run(test())
