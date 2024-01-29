import asyncio
import csv
import json
import logging
import os
import random
import threading
import time
import requests
import websockets
import pandas as pd
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import APIError
from googleapiclient.discovery import build
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


class WebSocketServer:

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive.file',
             'https://www.googleapis.com/auth/drive']
    
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name('ranking-automation-33939eb3373d.json', scope)
    client = gspread.authorize(credentials)
    
    drive_service = build('drive', 'v3', credentials=credentials)
    sheets_service = build('sheets', 'v4', credentials=credentials)
    
    
    
    def __init__(self, port, host='localhost'):
        #print(port)
        self.csv_file = open('logs_data.csv', mode='a', newline='')
        self.csv_writer = csv.writer(self.csv_file)

        
        if self.csv_file.tell() == 0:
            self.csv_writer.writerow(['Date', 'Time', 'IP', 'Click URL', 'Type', 'Behaviour File'])
        
        self.host = host
        self.port = port
        self.server = None
        self.connected_clients = set()
        self.result = None
        self.th = None
        self.run()
        self.wait_for_connected()

    
    def insert_logs_csv(self, data):
        
        self.csv_writer.writerow(data)
        self.csv_file.flush()

    async def handler(self, websocket, path):
        self.connected_clients.clear()
        self.connected_clients.add(websocket)
        try:
            print('socket', websocket)
            async for message in websocket:
                if message == 'ping':
                    await websocket.send(json.dumps({"action": "ack"}))
                    continue
                self.result = message
                print("Message Received: ", message)
            
        except Exception as e:
            print(f"Connection closed exception: {e}")
            logging.error(e)
            #self.restart_server()
        
        except websocket.exceptions.ConnectionClosedOK as e:
            print(f"Connection closed with exception: {e}")
            logging.error(e)
            #self.restart_server()

        finally:
            #self.connected_clients.remove(websocket)
            print("client is removed...")
           
            
    async def start_serve(self):
        while True:
            try:
                self.server = await websockets.serve(self.handler, self.host, self.port, max_size=None)
                print(f"server started on {self.host}:{self.port}")
                await self.server.wait_closed()
            except Exception as ex:
                print(f"Server encountered an error: {ex}")
                print("Restarting server in 5 seconds...")
                await asyncio.sleep(5)

    async def stop_serve(self):
        
        if self.server:
            try:
                self.th.join(1)
                await self.server.wait_closed()
                print("self stopped")
            finally:
                self.server = None
        else:
             print("Server is not running")
    
    def stop_self(self):
        asyncio.run(self.stop_serve())

    async def send_message(self, message):
        self.result = None
        if self.connected_clients:
            await asyncio.wait([asyncio.create_task(client.send(message)) for client in self.connected_clients])
            print(f"Message sent: {message}")
        else:
            print("No clients connected")


    def wait_for_result(self):
        try_for_secs = 7
        while not self.result and try_for_secs > 0:
            time.sleep(0.7)
            try_for_secs -= 0.5
            print('wait for result')
    
    # def wait_for_result(self):
       
    #     while not self.result:
    #         time.sleep(0.5)
    #         print('wait for result')

    def run_main(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.start_serve())
            loop.run_forever()
        except KeyboardInterrupt:
            asyncio.run(self.stop_serve())


    def wait_for_connected(self):
        while not self.is_connected():
            time.sleep(0.5)

    def is_connected(self):
        return len(self.connected_clients) > 0

    def run(self):
        self.th = threading.Thread(target=self.run_main)
        self.th.start()
    
    def restart_server(self):
        print("Restarting server...") 
        self.stop_self() 
        time.sleep(3)  
        self.run()
        self.wait_for_connected()
        print("Server restarted")

    def clickButtonByXpath(self, xpath):
        
        asyncio.run(self.send_message(json.dumps(
        {
            "action": "clickButtonByXpath",
            "payload": {
                "selector": xpath
            }
        })))
        self.wait_for_result()
        return self.result
    
    def clickButtonBySelector(self, selector):
        
        asyncio.run(self.send_message(json.dumps(
        {
            "action": "clickButtonBySelector",
            "payload": {
                "selector": selector
            }
        })))
        self.wait_for_result()
        return self.result
    
    def clickAds(self, xpath):
        
        asyncio.run(self.send_message(json.dumps(
        {
            "action": "clickAds",
            "payload": {
                "selector": xpath
            }
        })))
        self.wait_for_result()
        return self.result
    
    def clickRandomAds(self, selector1, selector2):
        
        asyncio.run(self.send_message(json.dumps(
        {
            "action": "clickRandomAds",
            "payload": {
                "selector": selector1,
                "selector2": selector2
            }
        })))
        self.wait_for_result()
        return self.result
    
    def clickRandomAds1(self, selector1):
        
        asyncio.run(self.send_message(json.dumps(
        {
            "action": "clickRandomAds1",
            "payload": {
                "selector": selector1
            }
        })))
        self.wait_for_result()
        return self.result
    
    def closeTab(self,):
        asyncio.run(self.send_message(json.dumps(
        {
            "action": "closeTab",
        })))
        self.wait_for_result()
        return self.result
    
    def openMainTab(self,url):
        asyncio.run(self.send_message(json.dumps(
        {
            "action": "openMainTab",
            "payload": {
                "selector": url
            }
        })))
        self.wait_for_result()
        return self.result
    
    def scrollUp(self,up):
        asyncio.run(self.send_message(json.dumps(
        {
            "action": "scrollUp",
            "payload": {
                "selector": up
            }
        })))
        self.wait_for_result()
        return self.result
    
    def scrollDown(self,down):
        asyncio.run(self.send_message(json.dumps(
        {
            "action": "scrollDown",
            "payload": {
                "selector": down
            }
        })))
        self.wait_for_result()
        return self.result
    
    def goBack(self):
        asyncio.run(self.send_message(json.dumps(
        {
            "action": "goBack",
        })))
        self.wait_for_result()
        return self.result
    
    def doesElementExist(self,css_selector):
        asyncio.run(self.send_message(json.dumps(
        {
            "action": "doesElementExist",
            "payload": {
                "selector": css_selector
            }
        })))
        self.wait_for_result()
        return self.result
    
    def clearCookies(self):
        asyncio.run(self.send_message(json.dumps(
        {
            "action": "clearCookies",
        })))
        self.wait_for_result()
        return self.result
    
    def openUrlNewTab(self,url):
        asyncio.run(self.send_message(json.dumps(
        {
            "action": "openUrlNewTab",
            "payload": {
                "selector": url
            }
        })))
        self.wait_for_result()
        return self.result
    
    def refreshPage(self):
        asyncio.run(self.send_message(json.dumps(
        {
            "action": "refreshPage",
        })))
        self.wait_for_result()
        return self.result


    def get_public_ip(self):
        try:
            #print(self.port)
            
            if self.port == 9000:
                proxy_port=10001
            
            elif self.port == 9001:
                proxy_port=10002
            
            elif self.port == 9002:
                proxy_port=10003
            
            elif self.port == 9003:
                proxy_port=10004
            
            elif self.port == 9004:
                proxy_port=10005

            
            # Your proxy details
            proxies = {
                'http': f'http://geonode_d1vJLEIwnO:3bad8f97-9371-47e6-9c6b-1f65a174b0b2@premium-residential.geonode.com:{proxy_port}',
                'https': f'http://geonode_d1vJLEIwnO:3bad8f97-9371-47e6-9c6b-1f65a174b0b2@premium-residential.geonode.com:{proxy_port}'
            }
        
            response = requests.get('https://httpbin.org/ip', proxies=proxies)
            #print(response.json()['origin'])
            return response.json()['origin']
        except Exception as e:
            print(f"Error getting IP address: {str(e)}")
            return None

    
    def get_date_and_time(self):
        current_datetime = datetime.datetime.now()
        date_part = current_datetime.date()
        time_part = current_datetime.strftime('%H:%M:%S')  # Format to exclude milliseconds
        
        return str(date_part), str(time_part)
    
    def insert_logs_spreadsheet(self, spreadsheet_name, sheet_name, starting_cell, data_list):
        print(starting_cell)
        success = False
        row = int(starting_cell[1:])
        col = ord(starting_cell[0]) - 64  

        for data_row in data_list:
            col_num = col  
            while not success:
                try:
                    sheet = self.client.open(spreadsheet_name).worksheet(sheet_name)
                    start_range = f"{chr(col_num + 64)}{row}"
                    end_range = f"{chr(col_num + len(data_row) - 1 + 64)}{row}"
                    cell_range = f"{start_range}:{end_range}"
                    values = [value for value in data_row]
                    sheet.update(cell_range, [values])

                    success = True  
                    row += 1  

                except APIError as error:
                    if error.response.status_code == 429:
                        print("Quota exceeded. Retrying in 40 seconds...")
                        time.sleep(40)  
                        continue
                    else:
                        print("APIError occurred: ", error)
                        print("Retrying in 10 seconds...")
                        time.sleep(10)  
                        continue

                except (ConnectionError, Timeout, TooManyRedirects) as error:
                    print("Connection error occurred: ", error)
                    print("Retrying in 10 seconds...")
                    time.sleep(10)  
                    continue

                except Exception as error:
                    print("An error occurred: ", error)
                    print("Retrying in 10 seconds...")
                    time.sleep(10)  
                    continue
    
    def get_random_csv_file(self,folder_path):
        csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
        if not csv_files:
            raise ValueError("No CSV files found in the specified folder.")
        
        return random.choice(csv_files)
    
    def get_intensity(self):
        df = pd.read_csv("heat_maps.csv", converters={'Time': str})
        df = df.astype(str)

        now = datetime.datetime.now()
        df["Time"] = df["Time"].apply(str)

        matching_rows = df[
            (df["Time"] == now.strftime("%I"))
            & (df["Day"] == now.strftime("%A"))
            & (df["Period"] == now.strftime("%p"))
        ]
        if len(matching_rows) == 0:
            print("No matching rows found")
        else:
            intensity = matching_rows["Times"].values[0]
            print(intensity)
            return int(intensity)
    
    def get_sleep_time(self, intensity):
        time_for_itrations = 4 * int(intensity)
        total_time = 60
        time_sleep =  (total_time - time_for_itrations)/intensity
        return time_sleep
    
    def should_pick_extra(self, n1):

        avg_iterations, remainder = divmod(n1, 5)
        # Calculate the weighted probabilities
        p_extra = remainder / 5
        p_no_extra = 1 - p_extra     
        # Decide based on weighted random choice
        choice = random.choices([0, 1], weights=[p_no_extra, p_extra], k=1)[0]
    
        return choice == 1

    def get_random_sleep_integers(self, target_sleep):
        
        # Generate the first three random numbers
        a = random.randint(0, target_sleep)
        b = random.randint(0, target_sleep - a)
        c = random.randint(0, target_sleep - a - b)
    
        # Calculate the fourth number so that the sum is target_sleep
        d = target_sleep - a - b - c

        # Return the four numbers as a list
        return [a, b, c, d]
    
    def solveCaptcha(self):

        self.clickButtonBySelector("#recaptcha-anchor")
        time.sleep(4)
        self.clickButtonBySelector("div.button-holder.help-button-holder")
        time.sleep(4)
        self.openMainTab('https://www.google.com/search?q=sodaTaste&sca_esv=559361602&ei=0tT1ZMSiCIzTsAeawrBQ&ved=0ahUKEwjE0421gZGBAxWMKewKHRohDAoQ4dUDCBE&uact=5&oq=sodaTaste&gs_lp=Egxnd3Mtd2l6LXNlcnAiCXNvZGFUYXN0ZTILEC4YgAQYxwEYrwEyBBAAGB4yBBAAGB4yBBAAGB4yBBAAGB4yBhAAGB4YCjIEEAAYHjIEEAAYHjIEEAAYHjIEEAAYHjIaEC4YgAQYxwEYrwEYlwUY3AQY3gQY4ATYAQFIq1NQkgtY2jhwBXgAkAEAmAGjAaABwwOqAQMwLjO4AQPIAQD4AQHCAgsQABgHGB4YsAMYCsICCBAAGIAEGLADwgIHEAAYHhiwA8ICCRAAGB4YsAMYCsICBxAAGA0YgATiAwQYASBBiAYBkAYKugYGCAEQARgU&sclient=gws-wiz-serp')
        time.sleep(4)
    
    
    def automate(self,server,intensity):
            
            while(not server.is_connected()):
                time.sleep(2)
            print(server.connected_clients)

            if self.should_pick_extra(intensity):
                print(f'Pick one extra visit for this server: {server}')
                intensity += 1
            
            sleep_time = self.get_sleep_time(intensity)
            if sleep_time <= 0 :
                sleep_time = 0.5 
            #random_sleep = self.get_random_sleep_integers(sleep_time)

            
            random_selector1 = "div[data-dtld='sodataste.com']"
            #random_selector2 = "div.v5yQqb"   #div.v5yQqb  #a[data-pcu="https://sodataste.com/"]
            random_selector2 = 'div.v5yQqb'
            for i in range(intensity):
                search= ['sodataste']
                random_item = random.choice(search)
                loop_start_time = time.time()
                if self.doesElementExist(random_selector1) == 'false' and self.doesElementExist('a[data-pcu="https://sodataste.com/"]') == 'false' :
                    self.clearCookies()
                    time.sleep(random.randint(7, 9))
                    self.openMainTab(random_item)
                    time.sleep(random.randint(13, 16))
                    self.scrollDown(1500)
                    time.sleep(random.randint(5, 7))
                
                ip = self.get_public_ip()
                
                if self.doesElementExist(random_selector1) == 'true' or self.doesElementExist(random_selector2) == 'true' :
                    
                    click_url = self.clickRandomAds(random_selector1,random_selector2)
                    time.sleep(random.randint(15, 18))
                    self.clickButtonBySelector('.btn-accept .btn-btn-accept-all')
                    time.sleep(random.randint(2, 4))
                    self.clickButtonBySelector('button.recommendation-modal__button')
                    time.sleep(random.randint(4, 6))
                    result=self.doesElementExist("button.quantity__button[name='plus']")
                    
                    if result== 'true':
                        folder_path = 'behaviours/type1/'
                        print(result)
                        file = self.get_random_csv_file(folder_path)
                        print(file)
                    else:
                        folder_path = 'behaviours/type2/'
                        file = self.get_random_csv_file(folder_path)
                        print(file)       
                    #actions by csv file
                    time.sleep(2)
                    csv_file_path = os.path.join(folder_path, file)
                    actions= pd.read_csv(csv_file_path)
                    for index, row in actions.iterrows():
                        
                        action= row['action']
                        data= row['url']
                        
                        if action== 'clickbyxpath':
                            self.clickButtonByXpath(data)
                        
                        if action== 'clickbyselector':
                            self.clickButtonBySelector(data)
                        
                        if  action == 'sleep':
                            time.sleep(random.randint(5, 15))
                        
                        if action == 'goback':
                            self.goBack()
                        
                        if action == 'ScrollUp':
                            self.scrollUp(data)
                        
                        if action == 'ScrollDown':
                            self.scrollDown(data)

                    time.sleep(random.randint(5, 7))
                    self.clearCookies()
                    time.sleep(random.randint(4, 6))
                    date,time1 = self.get_date_and_time()
                    file_path = csv_file_path.replace('behaviours/', '', 1)
                    data= [date,time1,ip,click_url,'Web',file_path]
                    self.insert_logs_csv(data)
                
                else:
                    print('Ads not found waiting for 3 minutes and try again...')
                    self.clearCookies()
                    time.sleep(1*60)
                
                self.openMainTab(random_item)
                time.sleep(random.randint(10, 15))
                if self.doesElementExist('div.QS5gu.sy4vM[role="none"]') == 'false' :
                    self.clearCookies()
                    time.sleep(random.randint(5, 10))
                    self.openMainTab(random_item)
                    time.sleep(random.randint(10, 15))
                    

                self.clickButtonBySelector('div.QS5gu.sy4vM[role="none"]')
                print(f"{i+1}: Itration complate. \nNow sleep for {sleep_time} minutes ..." )
                
                end_time = time.time()
                total_time = (end_time - loop_start_time) / 60
                print(f"Total time took by the Itration: {total_time:.2f} minutes")
                time.sleep(random.randint(7, 10))
                self.refreshPage()
                time.sleep(sleep_time*60)
               


        
    
    
    
    
    
    

