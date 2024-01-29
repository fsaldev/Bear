import threading
import time
from websocket_server import WebSocketServer


if __name__ == "__main__":
    ports = [9000, 9001, 9002, 9003, 9004]
    #ports = [9000]
    servers = []

    for port in ports:
        server = WebSocketServer(port)
        servers.append(server)
    
    while True:
        
        print("Getting Intensity and staring bots..")
        
        total_intensity = servers[0].get_intensity() 
        intensity_level = int(total_intensity // len(servers))
        
        print("Intensity for each bot is: " , intensity_level)
        threads = []

        for server in servers:
            thread = threading.Thread(target=server.automate, args=(server, intensity_level))
            threads.append(thread)
        
        
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
            
