from tkinter import *
from tkinter import ttk
from pytube import YouTube
import requests
import json
import time


body = {"Gender":"All", "MacAddress":"b8:27:eb:45:c7:21", "Location":"", "Business":"", "Age":""}

response = requests.post("http://smartgsc.rannlabprojects.com/api/CMS/SearchAdvertisement", json = body)

# for i in response.json():
#     print(i["ID"])
global videosize, reponse_list, videoname

def progress(chunk = None, file_handle = None, bytes_remaining = None):
    #print(filesize, bytes_remaining)
    percent = (100 * (videosize - bytes_remaining)) / videosize
    #print(int(percent),"%")
    progress_bar['value'] = percent
    tkProgressLabel.config(text = videoname+"\n"+str(int(progress_bar['value']))+"% downloaded")
    root.update_idletasks()
    


response_list = json.loads(response.json())


def DownloadUrlVideo():
    global videosize, videoname
    url = tkLink.get()
    tkError.config(text = '')
    if (len(url) > 1):
        yt = YouTube(url, on_progress_callback= progress)
        video = yt.streams.filter(progressive = True, file_extension = 'mp4').first()
        videosize = video.filesize
        videoname = yt.title
        print(videoname)
        video.download()
        tkError.config(text = 'Download completed', fg = 'red')
    else:
        tkError.config(text = 'Paste the link again', fg = 'red')


def DownloadApiVideo():
    global videosize
    global videoname
    tkError.config(text = '')
    for i in response_list:
        url = i['VideoUrl']
        # print(i['ID'], '\t', i['VideoUrl'])
        if (len(url) > 1):
            yt = YouTube(url, on_progress_callback= progress)
            video = yt.streams.filter(progressive = True, file_extension = 'mp4').first()
            videosize = video.filesize
            videoname = i['CompanyName']
            #print("%.2f MB"%((videosize) / 102400))  #Bytes
            video.download(filename = str(i['ID']))
            print('Download done for id : ',i['ID'])
            time.sleep(2)
        else:
            print('Failed')

    tkProgressLabel.config(text = "All videos downloading completed")
            


root = Tk()
root.geometry('400x300')
root.title('YOUTUBE VIDEO DOWNLOAD')
root.columnconfigure(0, weight = 1)

#Label
tklabel = Label(root, text = 'Enter YouTube link:')
tklabel.grid()

#URL input from user
tkLink = Entry(root, width = 50)
tkLink.grid()

#Single Video Download Button
tkDownload = Button(root, width = 10, text = 'Download', command = DownloadUrlVideo)
tkDownload.grid()

#LabelError
tkError = Label(root, text = '')
tkError.grid(pady = 20)

#Label
tklabel1 = Label(root, text = 'To download all videos from API. Click the button below')
tklabel1.grid()

#Download All Button
tkDownAll = Button(root, width = 10, text = 'Download All', command = DownloadApiVideo)
tkDownAll.grid()

#Progress Bar
progress_bar = ttk.Progressbar(root, orient = HORIZONTAL, length = 250, mode = 'determinate')
progress_bar.grid(pady = 30)

#Progressbar Label
tkProgressLabel = Label(root, text = '', fg = 'red')
tkProgressLabel.grid()

root.mainloop()
