from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/api/send-message")
async def send_message(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Wait for a message from the client
            data = await websocket.receive_json()
            print()
            print("User message: ")
            print(data)
            print()

            user_message = data['message']
            bot_response = 'Default Message'

            # TODO: Here you would integrate your actual bot logic
            # For example, parsing the user_message and generating a bot_response

            # Send the bot's response as JSON back to the client
            await websocket.send_json({"bot_response": bot_response})
    except WebSocketDisconnect:
        print("Client disconnected")