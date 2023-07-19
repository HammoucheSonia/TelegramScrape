from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerEmpty
import csv

api_id = input("Entrez votre identifiant d'API : ")
api_hash = input("Entrez votre clé d'API : ")
phone = input("Entrez votre numéro de téléphone (au format international, avec le code du pays) : ")

client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Entrez le code (reçu dans votre application Telegram) : '))

dialogs = client.get_dialogs()
channels = [dialog for dialog in dialogs if dialog.is_channel]

for i, channel in enumerate(channels):
    print(f"{i + 1}. Nom du canal : {channel.title}")
    print(f"   Identifiant du canal : {channel.id}")

channel_index = int(input("Entrez le numéro du canal à scraper : ")) - 1

try:
    target_channel = channels[channel_index]
except IndexError:
    print("Numéro de canal invalide. Veuillez réessayer.")
    exit()

print("Récupération des membres...")
all_participants = []
for participant in client.iter_participants(target_channel):
    all_participants.append(participant)

print("Enregistrement dans le fichier...")
with open("members.csv", "w", encoding="UTF-8") as f:
    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    writer.writerow(
        ["username", "user id", "access hash", "name", "channel", "channel id"]
    )
    for user in all_participants:
        username = user.username if user.username else ""
        first_name = user.first_name if user.first_name else ""
        last_name = user.last_name if user.last_name else ""
        name = (first_name + " " + last_name).strip()
        writer.writerow(
            [
                username,
                user.id,
                getattr(user, "access_hash", ""),
                name,
                target_channel.title,
                target_channel.id,
            ]
        )

print("Scraping des membres terminé avec succès.")

