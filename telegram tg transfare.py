from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError, FloodWaitError
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
import time

api_id = '' 
api_hash = ""  
phone_number = ''  

source_channel = -1002262784472  # معرف القناة التريدها  
target_channel = -1002055187095  # معرف قناتك 

client = TelegramClient('session_name', api_id, api_hash)

async def login():
    try:
        await client.start(phone_number)
        print("Logged in successfully!")
    except SessionPasswordNeededError:
        password = input("Two-step verification enabled. Please enter your password: ")
        await client.start(password=password)
        print("Logged in successfully with two-step verification!")

async def transfer_all_messages():
    try:
        print(f"Starting to transfer messages from {source_channel} to {target_channel}...")
        
        source_channel_entity = await client.get_entity(source_channel)
        target_channel_entity = await client.get_entity(target_channel)
        
        async for message in client.iter_messages(source_channel_entity):
            try:
                if message.text:
                    await client.send_message(target_channel_entity, message.text)
                    print(f"Forwarded text message: {message.text}")

                if message.media:
                    if isinstance(message.media, (MessageMediaPhoto, MessageMediaDocument)):
                        await client.send_file(target_channel_entity, message.media)
                        print(f"Forwarded media: {message.media}")
                    else:
                        print("Media type not handled, skipping.")
                
                time.sleep(1) 

            except FloodWaitError as e:
                print(f"Rate limit exceeded, waiting for 222 seconds...")
                time.sleep(222)  
                continue  

        print("All messages have been transferred successfully!")
    except Exception as e:
        print(f"Error during transfer: {e}")

async def main():
    await login()
    print("Client is running...")
    await transfer_all_messages()
    await client.disconnect()

client.loop.run_until_complete(main())
