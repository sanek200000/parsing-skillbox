import m3u8

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

uri='https://cdn-g.boomstream.com/adaptive/hash:41be4e4aae7aeceb8e8edf6ec5a5127e/data:eyJ2ZXJzaW9uIjoiMS4yLjg1IiwidXNlX2RpcmVjdF9saW5rcyI6InllcyIsImlzX2VuY3J5cHQiOiJ5ZXMifQ==/IWbrK8C8/playlist.m3u8'

with open('chunklist_1080p.m3u8', 'r', encoding='utf-8') as file:
    res = file.read().replace('\n', ',')
    print(res)

playlist = m3u8.loads(res)
print(playlist.playlists)
