import re
import os.path
import sys
import tempfile
import subprocess
from urllib.request import urlopen
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Protocol.KDF import PBKDF2
import requests

def parse_m3u8(_url):
	urldir = os.path.dirname(_url)
	dirname = 'temp_' + str(urldir).split(r'/')[-1].split('.mp4')[0]
	playlist = requests.get(_url).text.split('\n')

	chunklist = [line.strip() for line in playlist if line.startswith('https')]
	print(chunklist)

	if not os.path.exists(dirname):
		os.mkdir(dirname)

	media_files = []
	for chunk in chunklist:
		filename = dirname + '/' + chunk.split('/')[-1]
		print(filename)
		media_files.append(filename)

		if not os.path.exists(filename):
			r = requests.get(chunk, allow_redirects=True)
			with open(filename, 'wb') as file:
				file.write(r.content)

	return media_files


def download_m3u8(result):

	pass

if __name__ == '__main__':
	# url = sys.argv[1]
	url = 'https://cdn-g-skb-m7.boomstream.com/vod/hash:4fb2ef034568874f4bd2812ee0f49d2d/id:12985.14487.760926.39654069.75373.hls/time:0/data:eyJ2ZXJzaW9uIjoiMS4yLjg1IiwidXNlX2RpcmVjdF9saW5rcyI6InllcyIsImlzX2VuY3J5cHQiOiJ5ZXMifQ==/m57/2022/08/05/gE3hbXDp.mp4/chunklist.m3u8'
	password = '17bb96ba-3220-4874-b609-2ea245887c63'
	key = PBKDF2(password, b'...', dkLen=128)
	blob = 'blob:https://go.skillbox.ru/17bb96ba-3220-4874-b609-2ea245887c63'
	print(key)

	result = parse_m3u8(url)
	# download_m3u8(result)