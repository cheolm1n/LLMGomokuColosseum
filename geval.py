from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCaseParams, LLMTestCase

criteria = """
1. Immediate Win
Criterion: The move results in an immediate victory by completing a sequence of five stones in any direction (horizontal, vertical, diagonal).
Evaluation: Check if placing a stone at the suggested position completes a five-stone sequence for an instant win.
Example: Placing at I11 completes a vertical sequence and results in an immediate win.
Exception: This criterion is not evaluated unless the situation requires an immediate victory in the early stages of the game or the current board state.

2. Threat Block
Criterion: The move effectively blocks an immediate threat from the opponent that could lead to their victory.
Evaluation: Determine if the opponent is one move away from completing a sequence of five stones, and if the suggested move prevents this.
Example: Blocking the opponent's potential winning move at J10.

3. Strategic Positioning
Criterion: The move places a stone in a position that is advantageous for long-term strategy, such as controlling the center or key intersections.
Evaluation: Assess whether the move helps to control critical areas of the board, enhancing the player's strategic position.
Example: Placing a stone to control the center of the board or an important intersection.

4. Connectivity
Criterion: The move enhances the connectivity of the player's stones, forming potential sequences or strengthening existing ones.
Evaluation: Check if the move connects well with existing stones to form a stronger formation.
Example: Extending a sequence from three to four stones, or forming multiple potential lines of attack.

5. Potential Sequences
Criterion: The move creates new potential sequences (horizontal, vertical, or diagonal) that can lead to future threats or winning opportunities.
Evaluation: Evaluate if the move opens up new opportunities for creating sequences of five stones in future turns.
Example: Placing a stone to initiate a new line of attack that can be built upon in subsequent moves.

6. Opponent Threat Creation
Criterion: The move forces the opponent to respond defensively, disrupting their strategy and creating threats they must address.
Evaluation: Determine if the move puts the opponent in a position where they must defend against a potential threat, limiting their options.
Example: Creating a dual threat where the opponent can only block one potential sequence.

7. Risk and Reward
Criterion: The move balances the risk of the opponent's counter-moves with the potential reward it brings to the player's strategy.
Evaluation: Analyze the potential risks associated with the move and weigh them against the benefits it offers.
Example: Placing a stone in a position that is risky but offers a significant strategic advantage if not immediately countered.
"""

correctness_metric = GEval(
    name="Correctness",
    criteria=criteria,
    # NOTE: you can only provide either criteria or evaluation_steps, and not both
    # evaluation_steps=[
    #     "Check whether the facts in 'actual output' contradicts any facts in 'expected output'",
    #     "You should also heavily penalize omission of detail",
    #     "Vague language, or contradicting OPINIONS, are OK"
    # ],
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
)


def evaluate(prompt_input, gen_output):
    test_case = LLMTestCase(
        input=prompt_input,
        actual_output=gen_output
    )
    correctness_metric.measure(test_case)
    return {correctness_metric.score, correctness_metric.reason}
