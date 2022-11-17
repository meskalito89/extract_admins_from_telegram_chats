import telethon 
from telethon.tl.types import ChannelParticipantsAdmins
from pdb import set_trace
from pprint import pprint
import argparse
from json import loads
from operator import itemgetter
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import ChatAdminRequiredError, UsernameInvalidError, ChannelPrivateError
import pandas as pd

argparser = argparse.ArgumentParser('Extract admins from telegram channels')
argparser.add_argument(
    '-i',
    '--input',
    help="path to XLSX file",
    required=True
)
argparser.add_argument(
    '-o',
    '--output',
    help="path to output file",
    required=True
)
argparser.add_argument(
    '-t',
    '--tg_config',
    default='telegram_config.json',
    help='path to telegram config file'
)

arguments = argparser.parse_args()


def get_channels_from_input_file(path_to_input_file):
    excel_table = pd.read_excel(path_to_input_file)
    channels = excel_table.iloc[:,0]
    return channels.array

def parse_telegram_config(telegram_config_file):
    with open(telegram_config_file) as config_file:
        config = loads(config_file.read())
        return config
        
def extract_admins_from_channel(url_of_channel):
    with client:
        try:
            admin_iter = client.iter_participants(
                url_of_channel,
                filter=ChannelParticipantsAdmins
            )
        
            admins = [admin for admin in admin_iter]
            return admins
        except (ChatAdminRequiredError, ValueError, UsernameInvalidError, ChannelPrivateError):
            return []

def entity_is_chat(entity):
    return not entity.to_dict()['broadcast']


telegram_config = parse_telegram_config(arguments.tg_config)
telegram_config_tupple = itemgetter('username', 'api_id', 'api_hash')(telegram_config)

client = TelegramClient(*telegram_config_tupple)

if __name__ == '__main__':
    telegram_channels = get_channels_from_input_file(arguments.input)
    with client:
        for channel in telegram_channels:
            try:
                entity = client.get_entity(channel)
            except:
                continue
            if entity_is_chat(entity):
                print(entity.to_dict())
            else:
                print("channel {channel} is not chat")
        
        # admins = extract_admins_from_channel(channel)
        # print("{<50 } {}".format(channel, admins))


