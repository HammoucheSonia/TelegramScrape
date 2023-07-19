from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import traceback
import time
import random

api_id = 25471012
api_hash = 'bf05a79074a5b09ee0f1607c2abbbe63'
phone = '0033782517103'

def add_members_to_channel(input_file, group_index, mode):
    client = TelegramClient(phone, api_id, api_hash)
    client.connect()
    
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('Enter the code: '))

    try:
        users = []
        with open(input_file, encoding='UTF-8') as f:
            rows = csv.reader(f, delimiter=",", lineterminator="\n")
            next(rows, None)
            for row in rows:
                user = {}
                user['username'] = row[0]
                user['id'] = int(row[1])
                user['access_hash'] = int(row[2])
                user['name'] = row[3]
                users.append(user)
    except FileNotFoundError:
        print('Filepath not found, please specify the full path if necessary')
        return

    chats = []
    last_date = None
    chunk_size = 200
    groups = []

    result = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))
    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat.megagroup == True:
                groups.append(chat)
        except:
            continue

    if group_index >= len(groups):
        print('Invalid group index')
        return

    target_group = groups[group_index]
    target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

    n = 0
    for user in users:
        n += 1
        if n % 50 == 0:
            time.sleep(900)
        try:
            print("Adding {}".format(user['id']))
            if mode == 1:
                if user['username'] == "":
                    continue
                user_to_add = client.get_input_entity(user['username'])
            elif mode == 2:
                user_to_add = InputPeerUser(user['id'], user['access_hash'])
            else:
                sys.exit("Invalid Mode Selected. Please Try Again.")
            client(InviteToChannelRequest(target_group_entity, [user_to_add]))
            print("Waiting ...")
            time.sleep(random.randrange(1, 18))
        except PeerFloodError:
            sys.exit("Getting Flood Error from Telegram. Script is stopping now. Please try again after some time.")
        except UserPrivacyRestrictedError:
            print("The user's privacy settings do not allow you to do this. Skipping.")
        except Exception as e:
            traceback.print_exc()
            print("Unexpected Error:", str(e))
            continue

# Exemple d'utilisation de la fonction
input_file = "members.csv"
group_index = 1  # Indice du groupe cible (0 pour le premier groupe de la liste)
mode = 2  # Mode d'ajout par ID
add_members_to_channel(input_file, group_index, mode)

