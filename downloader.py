from bs4 import BeautifulSoup
from urllib import request
from queue import Queue
import time
import threading
import urllib
import requests
import os.path
path = ""
song_name = ""
songs = []
start = time.time()
q = Queue()
print_lock = threading.Lock()

with open('songs.txt','r') as f:
	for line in f:
		songs.append(line.replace('\n',''))


def Threader():
	while True:
		worker = q.get()
		print(songs[worker])
		Start(songs[worker])
		q.task_done()

def StartThreading():

	for x in range(5):
		t = threading.Thread(target = Threader)
		t.daemon = True
		t.start()

	for worker in range(len(songs)):
		q.put(worker)

	q.join()

def Start(name):
	links = Get_Links(name)
	final = Get_MP3(links)
	Download_MP3(final,name)
	

def Get_Links(song_Name):
	
	final_links = []
	song_name = song_Name
	url = "https://www.youtube.com/results?search_query=" + song_Name
	source_code = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
	if source_code == None:
		print("Error: Reuqest.get failed")
	plain_text = source_code.text
	soup = BeautifulSoup(plain_text,"html.parser")
	for link in soup.find_all('a',{"class": "yt-uix-sessionlink        spf-link "}):
		if link.get('href') is not None:
			final_links.append(link.get('href'))
	with print_lock:
		print(final_links[0])
	return final_links

def Get_MP3(final_Links):
	base_URL="https://www.youtubeinmp3.com"
	yt_URL = "https://www.youtube.com"
	nm_URL = "https://www.youtubeinmp3.com/download/?video="
	url = nm_URL + yt_URL + final_Links[0]
	source_code = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
	plain_text = source_code.text
	soup = BeautifulSoup(plain_text,"html.parser")
	for link in soup.find_all('a',{"id": "download"}):
		download = link.get('href');
		URL = base_URL + download
		print(URL)
		return URL
		
def Download_MP3(url,name):

	with print_lock:
		print("downloading " + name)
	mp3_file = request.urlopen(url).read()

	path = "Music\\" + name[:10].replace('-','') + ".mp3"
	with print_lock:
		print(path)
	if os.path.isfile(path):
		os.remove(path)
	with open(path,"wb") as f:
		f.write(mp3_file)


	#os.startfile(path)
		

StartThreading()



print("Entire Download took:",time.time()-start)