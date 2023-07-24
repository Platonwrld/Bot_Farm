from pyrogram import Client


client = Client("checker", 8, "7245de8e747a0d6fbe11f7cc14fcc0bb", in_memory=True)
client.start()
session_string = client.export_session_string()
with open("subscribe_checker.txt", 'w') as file:
    file.write(str(session_string))
client.stop()

client = Client("checker", 8, "7245de8e747a0d6fbe11f7cc14fcc0bb", in_memory=True)
client.start()
session_string = client.export_session_string()
with open("checker.txt", 'w') as file:
    file.write(str(session_string))
client.stop()
