#bibliotecas
'''
!pip install pyTelegramBotAPI
!pip install pytube
!pip install moviepy
!pip3 install imageio==2.4.1
!pip install --upgrade imageio-ffmpe
'''
#impotações
import random, telebot, os,re,requests,time
from moviepy.editor import *
from pytube import YouTube, Playlist
from tqdm import tqdm as q

TOKEN = "tokem
bot = telebot.TeleBot(TOKEN)
pathd =os.path.join(os.getcwd(),'music')    

def diryt():
    check=True
    for f in os.listdir(os.getcwd()):
        if f == 'music':
            return os.path.join(os.getcwd(),'music')
    os.mkdir('music')
    return os.path.join(os.getcwd(),'music')


def baixar(link,chatid,path='/content/music'):
    path=diryt()
    if 'playlist' in link or len(link) > 43:
        if 'music'in link:
            yt = YouTube(link)
            ys = yt.streams.filter(only_audio=True).first().download(path)
        else:
            yt=Playlist(link)
            cont,n=0,len(yt)

            f=bot.send_message(chatid,f'iniciando o dowload de{YouTube(link).title}')
            for m in q(yt) :
                cont=cont+1
                bot.edit_message_text(f'iniciando o dowload de{YouTube(link).title}\n {cont}-{n} ',chatid,f.message_id)
                try:
                    yt = YouTube(m)
                    ys = yt.streams.filter(only_audio=True).first().download(path)

                except:
                    pass
    else:
        yt = YouTube(link)
        ys = yt.streams.filter(only_audio=True).first().download(path)

    bot.edit_message_text(f'iniciando o dowload de{YouTube(link).title}emviando........... ',chatid,f.message_id)
    for file in os.listdir(path):                  
        if re.search('mp4', file):                                  
            mp4_path = os.path.join(path , file)   
            mp3_path = os.path.join(path, os.path.splitext(file)[0]+'.mp3') 
            new_file = AudioFileClip(mp4_path)  
            new_file.write_audiofile(mp3_path)     
            os.remove(mp4_path)
            os.system('clear')
            bot.send_audio(chatid,audio = open(f"{os.path.join(pathd,file[:-4]+'.mp3')}", 'rb'),caption=file[:-4],disable_notification=True)  
    os.system('clear')
    os.system('rm -r music/')                   
@bot.message_handler(func=lambda messagem:True)
def allmsg(m): 
    link=m.text
    if 'https:/' in link and 'yo' in link:
        baixar(link,int(m.chat.id))
print('rodandando...............')
bot.polling()
