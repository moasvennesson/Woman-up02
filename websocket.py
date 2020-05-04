import asyncio
import json
import websockets

# Här sparas alla våra connections
CONNECTIONS = set() # ett `set` är typ som en lista/dictionary

# Vår websockets `state`, här håller vi koll på bla. vilka användare vi har m.m.
# här kan vi givetvis lägga till mer vi vill hålla koll på, som användarnas
# longitude och latitude
STATE = {
    "users": []
}

# När en användare joinar
async def user_joined(data):
    # Säkerställ att vi har någon som är connectad
    if CONNECTIONS:
        user_id = data["userID"]

        # Lägg till användarens id i vår lista över användare
        # NOTE: här kan man lägga till ev. longitude/latitude
        STATE["users"].append({ "userID": user_id })

        users = STATE["users"]
        # Meddelande som skickas ut till alla som är connectade, vi konverterar
        # det till JSON så vi kan använda oss av det i vår JavaScript sen
        message = json.dumps({
            "action": "joined",
            "userID": user_id,
            "users": users # vi skickar med listan över alla nuvarande användare varje gång någon connectar
        })
        # Detta skickar ut meddelande till alla connectade användare
        await asyncio.wait([conn.send(message) for conn in CONNECTIONS])

# När en användare lämnar
async def user_leave(data):
    # Säkerställ att vi har någon som är connectad
    if CONNECTIONS:
        user_id = data["userID"]
        # Lägg till användarens id i vår lista över användare
        # STATE["users"].remove(user_id)

        # Gå igenom användarna, om den användaren som lämnade (dvs. från `data`)
        # har samma ID som en i vår lista så raderar vi just den
        for i in range(len(STATE["users"])):
            if STATE["users"][i]["userID"] == user_id:
                del STATE["users"][i]
                break

        users = STATE["users"]
        # Meddelande som skickas ut till alla som är connectade, vi konverterar
        # det till JSON så vi kan använda oss av det i vår JavaScript sen
        message = json.dumps({
            "action": "leave",
            "userID": user_id,
            "users": users # vi skickar med listan över alla nuvarande användare varje gång någon connectar
        })
        # Detta skickar ut meddelande till alla connectade användare
        await asyncio.wait([conn.send(message) for conn in CONNECTIONS])

# Ta emot ett chatt meddeleande
async def received_chat_message(data):
    if CONNECTIONS:
        user_id = data["userID"]
        chat_message = data["message"]

        # Vårat meddelande till alla connectade
        message = json.dumps({
            "action": "message",
            "userID": user_id,
            "message": chat_message
        })

        # Detta skickar ut meddelande till alla connectade användare
        await asyncio.wait([conn.send(message) for conn in CONNECTIONS])

# Registrera en ny användares connection
async def register(websocket):
    CONNECTIONS.add(websocket)

# Avregistrera en användares connection
async def unregister(websocket):
    CONNECTIONS.remove(websocket)

# Här hade vi kunnat hantera felmeddelande som dyker upp
def error_handler(loop, context):
    return

async def main(websocket, path):
    # Varje gång någon connectar till vår websocket sparar vi deras connection
    await register(websocket)

    try:
        async for message in websocket:
            # Vi tar emot data i form av JSON, med denna kan vi konvertera
            # JSON till en python dictionary
            data = json.loads(message)
            print(data)

            # Baserat på vilken `action` vi får så kan vi göra olika saker,
            # vi delegerar till andra funktioner för enkelhetens skull
            if data["action"] == "joined":
                await user_joined(data)
            if data["action"] == "leave":
                await user_leave(data)
            elif data["action"] == "message":
                await received_chat_message(data)

    except websockets.ConnectionClosed:
        print("[Websocket]: Connection closed")

    finally:
        # Avregistrera när dom slutar vara connectade
        await unregister(websocket)

start_server = websockets.serve(main, "127.0.0.1", 5678)
print("[Websocket]: Listening on ws://127.0.0.1:5678")

asyncio.get_event_loop().set_exception_handler(error_handler)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
