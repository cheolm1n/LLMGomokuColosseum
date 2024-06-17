const minConfettiScale = 0.5
const maxConfettiScale = 1

const minConfettiSpeed = 50
const maxConfettiSpeed = 60

const minConfettiGravity = 0.8
const maxConfettiGravity = 1.3

const colors = [
  "#FF3B30", // 빨간색
  "#FF9500", // 주황색
  "#FFCC00", // 노란색
  "#34C759", // 초록색
  "#007AFF", // 파란색
  "#5856D6", // 보라색
  "#FF2D55"  // 분홍색
]
let interval = null

const createConfetti = () => {

  // Left Confetti
  confetti.create({
    x: 0.001,
    y: 0.5,
    count: 20,
    gravity: [
      randomNumber(minConfettiGravity, maxConfettiGravity),
      randomNumber(minConfettiGravity, maxConfettiGravity),
      randomNumber(minConfettiGravity, maxConfettiGravity),
    ],
    ticks: 300,
    scale: [
      randomNumber(minConfettiScale, maxConfettiScale),
      randomNumber(minConfettiScale, maxConfettiScale),
      randomNumber(minConfettiScale, maxConfettiScale)
    ],
    speed: randomNumber(minConfettiSpeed, maxConfettiSpeed),
    decay: 0.95,
    spread: 50,
    angle: 50,
    shapes: [ 'square', 'ellipse' ],
    colors: colors
  })

  // Right Confetti
  confetti.create({
    x: 1.99,
    y: 0.5,
    count: 20,
    gravity: [
      randomNumber(minConfettiGravity, maxConfettiGravity),
      randomNumber(minConfettiGravity, maxConfettiGravity),
      randomNumber(minConfettiGravity, maxConfettiGravity),
    ],
    ticks: 300,
    scale: [
      randomNumber(minConfettiScale, maxConfettiScale),
      randomNumber(minConfettiScale, maxConfettiScale),
      randomNumber(minConfettiScale, maxConfettiScale)
    ],
    speed: randomNumber(minConfettiSpeed, maxConfettiSpeed),
    decay: 0.95,
    spread: 50,
    angle: 130,
    shapes: [ 'square', 'ellipse' ],
    colors: colors
  })

}

function toggleConfetti() {
  console.log(interval)
  if (interval) {
    clearInterval(interval)
    interval = null
  } else {
    interval = setInterval(() => {
      createConfetti()
    }, 50)
  }
}

function randomNumber(min, max) {
  return Math.random() * (max - min) + min
}