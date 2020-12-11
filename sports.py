import smtplib
from datetime import date
from googleapiclient.discovery import build

# Global data
api_key = 'API-KEY' # Real API key issued by YouTube developer accounts
youtube = build('youtube', 'v3', developerKey=api_key)
today = date.today()


def get_todays_from_channel(channel_id):
    upload_id = youtube.channels().list(
        part='contentDetails',
        id=channel_id,
        maxResults=100
    ).execute()['items'][0]['contentDetails']['relatedPlaylists']['uploads']


    list_of_uploads = youtube.playlistItems().list(
        part='snippet',
        playlistId=upload_id,
        maxResults=100
    ).execute()

    video_list = ""

    for video in list_of_uploads['items']:
        if str(video['snippet']['publishedAt'].split("T")[0]) == str(today):
            video_list += video['snippet']['title'] + "\n"

    return video_list


def send_email(message):
    sender_email = "abc@gmail.com" 
    receiver_email = "xyz@gmail.com" # Examples

    password = 'password' # Example. Could also be set as environment variable for better security

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(sender_email, password)

    to_be_sent = message.decode('ascii')
    server.sendmail(sender_email, receiver_email, to_be_sent)


def main():
    # Youtube channels from which data is pulled
    channel_ids = ['UCLXzq85ijg2LwJWFrz4pkmw', 'UCVSSpcmZD2PwPBqb8yKQKBA', "UCDVYQ4Zhbm3S2dlz7P1GBDg"]
    data = ""

    for channel in channel_ids:
        data += get_todays_from_channel(channel) + "\n"

    data = data.encode('ascii', 'ignore')
    send_email(data)


if __name__ == "__main__":
    main()
