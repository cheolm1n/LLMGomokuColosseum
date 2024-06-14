import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from game import Game
from player.openai_gpt_three_dot_five_turbo_player import OpenAiGptThreeDotFiveTurboPlayer
from player.openai_gpt_four_omni_player import OpenAiGptFourOmniPlayer
from player.meta_llama_3_70b_instruct_player import MetaLlamaThree70BInstructPlayer
from player.google_gemini_pro_player import GoogleGeminiProPlayer
from player.claude_opus_player import ClaudeOpusPlayer

app = FastAPI()
app.mount("/static", StaticFiles(directory="server/static"), name="static")


@app.get("/")
async def main():
    with open('./server/index.html') as f:
        return HTMLResponse(f.read())


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            message_text = await websocket.receive_text()
            data = json.loads(message_text)
            if data.get('action') == 'play':
                player1 = data.get('payload').get('player1')
                player2 = data.get('payload').get('player2')

                async def callback(action: str, x: int, y: int, position: str, valid: bool, player_number: int, retry_count: int = 0, winner: int = None):
                    data = {
                        'action': action,
                        'x': x,
                        'y': y,
                        'position': position,
                        'valid': valid,
                        'player_number': player_number,
                        'retry_count': retry_count,
                        'winner': winner
                    }
                    await websocket.send_text(json.dumps(data))

                game = Game(
                    get_player(player1, 1),
                    get_player(player2, 2),
                )
                await game.play(move_callback=callback)
        except WebSocketDisconnect as e:
            print("WebSocket disconnect")
            return
        # await websocket.send_text(f"Message text was: {data}")

def get_player(player_text, player_number):
    if player_text == 'GPT3.5':
        return OpenAiGptThreeDotFiveTurboPlayer(player_number, is_evaluate=False)
    if player_text == 'GPT4o':
        return OpenAiGptFourOmniPlayer(player_number, is_evaluate=False)
    if player_text == 'Llama3':
        return MetaLlamaThree70BInstructPlayer(player_number, is_evaluate=False)
    if player_text == 'Gemini':
        return GoogleGeminiProPlayer(player_number, is_evaluate=False)
    if player_text == 'Claude':
        return ClaudeOpusPlayer(player_number, is_evaluate=False)