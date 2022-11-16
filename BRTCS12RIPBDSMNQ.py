import asyncio
import websockets
import json
from PIL import ImageGrab, Image

print('/connect localhost:19131')                  #if localhost doesnt work, replace it with your own ip address
async def mineproxy(websocket):
    print('Connected')
    tosend_queue = []

    def send_vid(px_num):
        x = px_num%x_img_vid
        y = px_num//x_img_vid
        if invert:
            particle_num = int((255-pixel[x,y][2])//16 + (255-pixel[x,y][1])//16*16 + (255-pixel[x,y][0])//16*256)
        else:
            particle_num = int(pixel[x,y][2] //16 + pixel[x,y][1]//16*16 + pixel[x,y][0]//16*256)
        return {
            "header": {
                "requestId": 'e7d0d7e9-21d5-4e6c-9d6f-0092c2fcd6ac',
                "messagePurpose": "commandRequest"
            },
            "body": {
                "commandLine": 'particle "minecraft:{:}" {:.1f} {:} {:.1f}'.format(particle_num, ((x-x_px)/5)+x_coord, y_coord, ((y-y_px)/5)+z_coord)
            }
        }
    def send_pic(px_num):
        x = px_num%x_img_pic
        y = px_num//x_img_pic
        if invert:
            particle_num = int((255-pixel[x,y][2])//16 + (255-pixel[x,y][1])//16*16 + (255-pixel[x,y][0])//16*256)
        else:
            particle_num = int(pixel[x,y][2] //16 + pixel[x,y][1]//16*16 + pixel[x,y][0]//16*256)
        return {
            "header": {
                "requestId": 'e7d0d7e9-21d5-4e6c-9d6f-0092c2fcd6ac',
                "messagePurpose": "commandRequest"
            },
            "body": {
                "commandLine": 'particle "minecraft:{:}" {:.2f} {:} {:.2f}'.format(particle_num, ((x-x_px)/50)+x_coord, y_coord, ((y-y_px)/50)+z_coord)
            }
        }
    
    await websocket.send(                                                    #allows messages to be received
        json.dumps({
            "header": {               
                "requestId": 'e7d0d7e9-21d5-4e6c-9d6f-0092c2fcd6ac',
                "messagePurpose": "subscribe"     
            },
            "body": {
                "eventName": "PlayerMessage"
            }
        }))

    def cc(command):                               #custom command
        return {
            "header": {
                "requestId": 'e7d0d7e9-21d5-4e6c-9d6f-0092c2fcd6ac',
                "messagePurpose": "commandRequest"
            },
            "body": {
                "commandLine": 'say test'
            }
        }

#{"body":{"message":"t","receiver":"","sender":"NNCOS","type":"chat"},"header":{"eventName":"PlayerMessage","messagePurpose":"event","version":16973824}}             #sample (print(msg_raw))

    x_coord,y_coord,z_coord = -5.2,300.8,-5.2                                   #mc coords top left
    x_ratio, y_ratio = 16,9                                                     #mc particle dimensions
    mul_vid = 3
    mul_pic = 30
    x_img_vid, y_img_vid = int(x_ratio*mul_vid),int(y_ratio*mul_vid)          #overall image dimensions for vid
    x_px, y_px = 0,0                                                          #selected top left corner position of image to use
    x_change, y_change = x_img_vid, y_img_vid                                 #selected dimensions of image to use
    count = 100
    x_img_pic,y_img_pic = int(x_ratio*mul_pic),int(y_ratio*mul_pic)
    type = 0                                                                    #1=printer, 0=live video player
    a = True
    play = False
    invert = False
    
    try:
        async for msg_raw in websocket:
            #if a:                                              #for printer: starts printing after i reaches 10000
            #    for i in range(0,10000):
            #        print(i)
            #a=False
            msg_json = json.loads(msg_raw)                       #convert message received into json format
            try:                                                 #if player says play then start
                if msg_json['body']['message'] == 'invert':
                    invert = True
                elif msg_json['body']['message'] == 'normal':
                    invert = False
                if msg_json['body']['message'] == 'play' and play == False:
                    play = True
                elif msg_json['body']['message'] == 'stop':
                    play = False
                else:
                    continue
            except KeyError:
                pass
            if len(tosend_queue) <= 0 and type == 0 and play:          #max 620px
                pixel = ImageGrab.grab().resize((x_img_vid,y_img_vid), resample=Image.Resampling.BILINEAR).load()
                #pixel = ImageEnhance.Color(ImageGrab.grab().resize((x_img_vid,y_img_vid), resample=Image.Resampling.BILINEAR)).enhance(1.5).load()
                tosend_queue = list(map(send_vid, range(0,x_change*y_change)))        #create list with command for every particle
            
            if len(tosend_queue) <= 0 and type == 1:
                pixel = ImageGrab.grab().resize((x_img_pic,y_img_pic), resample=Image.Resampling.BILINEAR).load()
                tosend_queue = list(map(send_pic, range(0,x_img_pic*y_img_pic)))
            
            for command in tosend_queue[:count]:                            #for first 100 elements in list
                await websocket.send(json.dumps(command))
            tosend_queue = tosend_queue[count:]                             #removes first 100 from list

    except websockets.exceptions.ConnectionClosedError:
        print('Disconnected')

async def main():
    async with websockets.serve(mineproxy, 'localhost', 19131):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())


