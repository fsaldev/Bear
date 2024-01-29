import asyncio
import json
import time

import websockets


async def echo(websocket, path):

    message = await websocket.recv()
    print(message)


    # Getting HTMl Page
    await websocket.send(json.dumps({
        "action": "getHTML",
        "payload": {}
    }))

    # Get the HTML content from the client
    html = await websocket.recv()
    #print(html)
    # Save the HTML content to a file
    with open('page.html', 'wb') as f:
        f.write(html.encode('utf-8'))

    
    time.sleep(5)
    # Clicking Button by CSS selector
    await websocket.send(json.dumps({
        "action": "clickButtonByCSS",
        "payload": {}
    }))
    message = await websocket.recv()
    print(message)

    
    time.sleep(5)
    # Clicking Button by Xpath selector
    await websocket.send(json.dumps({
        "action": "clickButtonByXpath",
        "payload": {}
    }))
    message = await websocket.recv()
    print(message)

    
    time.sleep(5)
    # Getting HTML Content by CSS selector
    await websocket.send(json.dumps({
        "action": "getHtmlContentByCssSelector",
        "payload": {}
    }))
    
    # Getting the HTML content from the client
    html_css = await websocket.recv()

    # Save the HTML content to a file
    with open('HTML_content_Css.html', 'wb') as f:
        f.write(html_css.encode('utf-8'))

    time.sleep(5)
    # Performing bet
    await websocket.send(json.dumps({
        "action": "placeBet",
        "payload": {}
    }))
    message = await websocket.recv()
    print(message)


async def start_server():
    async with websockets.serve(echo, "localhost", 9000):
        print("WebSocket server started")
        await asyncio.Future()  # keep the server running


async def main():
    server_task = asyncio.create_task(start_server())
    await asyncio.gather(server_task)


if __name__ == "__main__":
    asyncio.run(main())
