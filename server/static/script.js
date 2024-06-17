const boardContainer = document.getElementById('board-container');
const consoleOutput = document.getElementById('console');
const goSounds = [document.getElementById("goSound1"), document.getElementById("goSound2")];
const winSound = document.getElementById("winSound");
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
for (let x = 0; x < size; x++) {
    const rowLabel = document.createElement('div');
    rowLabel.classList.add('row-label');
    rowLabel.textContent = x + 1;
    boardContainer.appendChild(rowLabel);

    for (let y = 0; y < size; y++) {
        const cell = document.createElement('div');
        cell.classList.add('cell');
        cell.dataset.x = x;
        cell.dataset.y = y;
        boardContainer.appendChild(cell);
    }
}

const appendLog = (log) => {
    consoleOutput.value += `${log}\n`
    consoleOutput.scroll(0, Number.MAX_SAFE_INTEGER)
}
const clearLog = () => {
    consoleOutput.value = ''
}
const clearBoard = () => {
    const stones = document.getElementsByClassName('stone')

    while (stones.length > 0) {
        stones[0].remove()
    }
}
const addStone = (x, y, playerColor) => {
    const grid = document.querySelector(`div[data-x="${x}"][data-y="${y}"]`);
    const stone = document.createElement('div');
    stone.classList.add('stone');
    stone.classList.add(playerColor);
    grid.appendChild(stone);
}

const getPlayerNameFromNumber = (playerNumber) => {
    return document.getElementById(`selectPlayer${playerNumber}`).value;
}

let websocket;
function initWebSocket() {
    clearLog()
    websocket = new WebSocket("ws://localhost:8000/ws")
    appendLog('Connecting...')
    websocket.onopen = () => {
        appendLog(`Connection Success. (${new Date().toLocaleTimeString()})`)
        clearBoard()
    }
    websocket.onmessage = (m) => {
        const {action, x, y, position, valid, player_number, retry_count, winner} = JSON.parse(m.data);
        const color =  (player_number % 2 === 1) ? 'black' : 'white';
        const playerText = `[Player${player_number}][${getPlayerNameFromNumber(player_number)}]`
        if (action === 'move_success') {
            // 돌 놓고 로그
            addStone(x, y, color)
            goSounds[Math.floor(Math.random() * goSounds.length)].play()
            appendLog(`${playerText} 돌을 놓았습니다 (${position})\n`)
        } else if (action === 'move_invalid') {
            // 로그만
            appendLog(`${playerText} 의 ${retry_count}번째 실수.`)
        } else if (action === 'switch_turn') {
            // 로그만
            appendLog(`${playerText}의 반복된 실수로 차례가 넘어갑니다!`)
        } else if (action === 'end') {
            appendLog(`${playerText}의 승리!`)
            winSound.play()
            toggleConfetti()
            setTimeout(toggleConfetti, 1000)
        }

    }
}
initWebSocket()

document.getElementById("playButton").onclick = () => {
    clearBoard()
    const player1 = document.getElementById('selectPlayer1').value;
    const player2 = document.getElementById('selectPlayer2').value;

    const data = {
        action: 'play',
        payload: {
            player1,
            player2
        }
    }
    appendLog("\n게임 시작!\n")
    websocket.send(JSON.stringify(data))
}
document.getElementById("stop").onclick = () => {
    websocket.close(1000, "Stop")
    appendLog("Connection closed")
}
document.getElementById("reconnect").onclick= () => {
    websocket.close(1000, 'Reconnect')
    initWebSocket()
}
