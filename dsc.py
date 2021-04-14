import discord
from json import dumps
from base64 import urlsafe_b64encode
from requests import get
import PySimpleGUI as sg
layout = [[sg.Text("Discord Token:")],
          [sg.Input(key='-INPUT-')],
          [sg.Button('Ok')]]


window = sg.Window('Enter Token', layout)

_, values = window.read()
token = values['-INPUT-'].strip().strip("\"")
print(token)
window.close()
del window
del layout
layout = [[sg.Text("Enter Channel ID")],
          [sg.Input(key='-INPUT-')],
          [sg.Button('Ok')]]


window = sg.Window('Enter Channel ID', layout)

_, values = window.read()
selectedchannelid = int(values['-INPUT-'].strip().strip("\""))
window.close()
del window
del layout
client = discord.Client()

serverport = 5080

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    ch = client.get_channel(selectedchannelid)
    chhist = []
    async for message in ch.history(limit=20):
        chhist.append(message)
    for message in reversed(chhist):
        msd = urlsafe_b64encode(
            bytes(dumps({"uname": message.author.display_name, "content": message.clean_content}), 'utf-8')).decode(
            "utf-8")
        get("http://localhost:" + str(serverport) + "/" + msd)

@client.event
async def on_message(message):
    if message.channel.id != selectedchannelid: return
    msd = urlsafe_b64encode(bytes(dumps({"uname": message.author.display_name, "content": message.clean_content}), 'utf-8')).decode("utf-8")
    get("http://localhost:"+str(serverport)+"/"+msd)


client.run(token, bot=False)