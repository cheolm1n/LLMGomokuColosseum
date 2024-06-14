const boardContainer = document.getElementById('board-container');
const coordinateOutput = document.getElementById('coordinateOutput');
const moveOutput = document.getElementById('moveOutput');
const recordOutput = document.getElementById('recordOutput');
const clearButton = document.getElementById('clear');
const undoButton = document.getElementById('undo');
const size = 15;
const letters = 'ABCDEFGHIJKLMNO';
let turnCount = 0;
let history = [];

// 상단 열 레이블 추가
const topLeft = document.createElement('div');
boardContainer.appendChild(topLeft);  // 빈 셀 추가
for (let x = 0; x < size; x++) {
    const colLabel = document.createElement('div');
    colLabel.classList.add('col-label');
    colLabel.textContent = letters[x];
    boardContainer.appendChild(colLabel);
}

// 왼쪽 행 레이블 및 바둑판 셀 추가
for (let y = 0; y < size; y++) {
    const rowLabel = document.createElement('div');
    rowLabel.classList.add('row-label');
    rowLabel.textContent = y + 1;
    boardContainer.appendChild(rowLabel);

    for (let x = 0; x < size; x++) {
        const cell = document.createElement('div');
        cell.classList.add('cell');
        cell.dataset.x = x + 1;
        cell.dataset.y = y + 1;
        cell.addEventListener('click', handleClick);
        boardContainer.appendChild(cell);
    }
}

function handleClick(event) {
    const x = event.target.dataset.x;
    const y = event.target.dataset.y;

    // 이미 돌이 있는지 확인
    if (event.target.querySelector('.stone')) {
        return;
    }

    // 턴 수 증가
    turnCount++;

    // 현재 플레이어 결정
    const currentPlayer = (turnCount % 2 === 1) ? 'black' : 'white';

    // 좌표 형식
    const coordinateFormat = { 'x': parseInt(x), 'y': parseInt(y) };

    // 기보 형식
    const moveFormat = letters[parseInt(x) - 1] + y;

    const coordinateText = `${JSON.stringify(coordinateFormat)}\n`;
    coordinateOutput.value += coordinateText;

    const moveText = `${moveFormat}\n`;
    moveOutput.value += moveText;

    const recordText = `record.add(player=${currentPlayer == 'black' ? 'test_player' : 'opponent_player'}, x=${x}, y=${y}, valid=True, reason="")\n`;
    recordOutput.value += recordText;

    // 바둑돌 생성
    const stone = document.createElement('div');
    stone.classList.add('stone');
    stone.classList.add(currentPlayer);
    event.target.appendChild(stone);

    // 히스토리에 현재 상태 저장
    history.push({ x, y, stone });
}

function clearBoard() {
    // 보드 초기화
    document.querySelectorAll('.cell').forEach(cell => {
        const stone = cell.querySelector('.stone');
        if (stone) {
            cell.removeChild(stone);
        }
    });
    // 출력 초기화
    coordinateOutput.value = '';
    moveOutput.value = '';
    recordOutput.value = '';
    // 히스토리 초기화
    history = [];
    // 턴 수 초기화
    turnCount = 0;
}

function undoMove() {
    if (history.length === 0) return;

    // 마지막 상태 복원
    const lastMove = history.pop();
    const cell = document.querySelector(`.cell[data-x='${lastMove.x}'][data-y='${lastMove.y}']`);
    if (cell) {
        cell.removeChild(lastMove.stone);
    }

    // 출력 업데이트
    const coordinateLines = coordinateOutput.value.trim().split('\n');
    const moveLines = moveOutput.value.trim().split('\n');
    const recordLines = recordOutput.value.trim().split('\n');

    coordinateOutput.value = coordinateLines.slice(0, -1).join('\n') + '\n';
    moveOutput.value = moveLines.slice(0, -1).join('\n') + '\n';
    recordOutput.value = recordLines.slice(0, -1).join('\n') + '\n';

    // 턴 수 감소
    turnCount--;
}

clearButton.addEventListener('click', clearBoard);
undoButton.addEventListener('click', undoMove);
