import os.path
import shutil
from Crypto.Util.Padding import unpad
from Crypto.Protocol.KDF import PBKDF2
import requests
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import time


def AESDecrypt(cipher_text, key, iv):
    cipher_text = pad(data_to_pad=cipher_text, block_size=AES.block_size)
    aes = AES.new(key=key, mode=AES.MODE_CBC, iv=key)
    cipher_text = aes.decrypt(cipher_text)
    return cipher_text


def parse_m3u8(_url, key, video_path) -> str:
    urldir = os.path.dirname(_url)
    dirname = 'temp_' + str(urldir).split(r'/')[-1].split('.mp4')[0]
    playlist = requests.get(_url).text.split('\n')

    chunklist = [line.strip() for line in playlist if line.startswith('https')]
    # print(chunklist)

    if not os.path.exists(dirname):
        os.mkdir(dirname)

    n = len(chunklist)
    start = time.time()
    size = 0
    media_files = []
    for chunk in chunklist:
        filename = dirname + '/' + chunk.split('/')[-1]
        print(filename)
        media_files.append(filename)

        if not os.path.exists(filename):
            r = requests.get(chunk, allow_redirects=True)
            data = r.content
            data = AESDecrypt(data, key=key, iv=key)
            size += len(data)
            # video_path = path + "videolesson.mp4"
            with open(video_path, "ab") as f:
                f.write(data)
            print(
                f"\r Download Progress({n})，Downloaded:{size / 1024 / 1024:.2f}MB，Download time consumed:{time.time() - start:.2f}s", end=" ")

            # with open(filename, 'wb') as file:
            # 	file.write(r.content)

    if os.path.exists(dirname):
        shutil.rmtree(dirname, ignore_errors=True)

    return video_path


def get_chunk_m3u8(req):
    lines = req.response.body.decode('utf-8').split('\n')

    for i in range(len(lines)):
        if '1920x1080' in lines[i]:
            return lines[i+1]
    return None


if __name__ == '__main__':
    # url = sys.argv[1]
    url = 'https://cdn-g-skb-m4.boomstream.com/vod/hash:e8f22940ae47e89857332a0b898957b2/id:12985.14487.760926.39654071.75377.hls/time:0/data:eyJ2ZXJzaW9uIjoiMS4yLjg1IiwidXNlX2RpcmVjdF9saW5rcyI6InllcyIsImlzX2VuY3J5cHQiOiJ5ZXMifQ==/m65/2022/08/05/omvuSbz8.mp4/chunklist.m3u8'
    password = '17bb96ba-3220-4874-b609-2ea245887c63'
    key = PBKDF2(password, b'r4kIvQ47FFUWgqoP', dkLen=128)
    blob = 'blob:https://go.skillbox.ru/17bb96ba-3220-4874-b609-2ea245887c63'
    key = b'r4kIvQ47FFUWgqoP'
    print(key)

    result = parse_m3u8(url, key, './videolesson.mp4')
    # download_m3u8(result)
