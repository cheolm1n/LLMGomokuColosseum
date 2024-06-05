from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCaseParams, LLMTestCase

criteria = """1. 위치와 맥락 
    - 수의 위치: 해당 수가 어디에 두어졌는지에 따라 평가가 달라집니다. 중심부나 변, 귀 등에 두어진 수의 가치가 다릅니다.
    - 상황적 맥락: 현재 게임의 상황에서 해당 수가 전략적으로 어떤 의미를 가지는지 평가합니다. 공격인지, 수비인지, 혹은 특정한 함정을 노리는 수인지 등이 포함됩니다.

2. 전략적 가치:
    - 장기적인 가치: 해당 수가 게임의 장기적인 관점에서 어떤 이점을 가져오는지 평가합니다. 예를 들어, 바둑에서는 중앙을 차지하거나 대규모의 세력을 형성하는 것이 중요합니다.
    - 즉각적인 효과: 해당 수가 즉각적으로 게임 상황을 어떻게 바꾸는지 평가합니다. 상대방의 수를 차단하거나 포위하는 등의 효과가 포함됩니다.
    - 가로와 세로 혼동 여부: 해당 수가 가로와 세로를 명확히 구분하고 두었는지, 혼동하지 않았는지 평가합니다.

3. 수의 효율성:
    - 최적의 수: 해당 상황에서 최선의 수인지, 아니면 다른 더 좋은 수가 있었는지 비교합니다.
    - 필수 수: 해당 수가 필수적인 수인지, 즉 두지 않으면 게임이 불리하게 되는 상황인지 평가합니다.

4. 상대방에 대한 영향:
    - 상대방의 대응: 해당 수에 대해 상대방이 어떻게 대응할 가능성이 높은지, 그리고 그 대응에 대한 대비가 되어 있는지를 평가합니다.
    - 심리적 압박: 상대방에게 심리적인 압박을 줄 수 있는 수인지 평가합니다. 예를 들어, 체스에서는 특정한 수로 상대방을 강하게 압박할 수 있습니다.

5. 공간적 활용:
    - 공간 확보: 해당 수가 판에서 얼마나 많은 공간을 차지하고 있는지, 혹은 상대방의 공간을 얼마나 제한하는지를 평가합니다.
    - 구조 강화: 자신의 구조를 얼마나 강화하는 수인지 평가합니다. 예를 들어, 오목에서는 연속된 돌을 연결하는 것이 중요합니다.

6. 수의 위험도:
    - 위험 분석: 해당 수가 얼마나 위험한 수인지, 즉 공격을 받기 쉬운 위치에 두어진 수인지 평가합니다.
    - 안전성: 해당 수가 얼마나 안전한 수인지, 상대방의 즉각적인 반격이 어려운지 평가합니다.

7. 게임 결과에 미치는 영향:
    - 승부에 미치는 영향: 해당 수가 게임의 결과에 얼마나 큰 영향을 미치는지, 승리로 이어질 가능성이 높은지, 패배로 이어질 가능성이 높은지 평가합니다.
    
8. 오목 룰에 대한 이해:
    - 오목은 두 명의 플레이어가 번갈아가며 흑돌과 백돌을 놓아 가로, 세로, 또는 대각선으로 연속된 다섯 개의 돌을 먼저 만드는 게임입니다.
    - 게임 보드: 오목은 15x15 또는 19x19 크기의 격자 보드에서 진행됩니다.
    - 돌의 배치: 두 명의 플레이어가 번갈아가며 돌을 놓습니다. 흑돌을 놓는 플레이어가 먼저 시작합니다.
    - 승리 조건: 가로, 세로, 또는 대각선 방향으로 연속된 다섯 개의 돌을 먼저 만들면 그 플레이어가 승리합니다.
    - 금지된 수에 대한 규칙은 따로 없습니다.
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
