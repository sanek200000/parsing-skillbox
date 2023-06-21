# Скрипт выводит в консоль содержимое файла в двоичном виде
# Можно использовать перенаправление вывода для сохранения файла
# Использование vkontakte_m3u8_downloader.py ссылка на аудиозапись > имя файла
# Для работы скрипта нужен ffmpeg
import re
import os.path
import sys
import tempfile
import subprocess
from urllib.request import urlopen
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import requests

def parse_m3u8(_url):
	urldir = os.path.dirname(_url)
	playlist = requests.get(_url).text
	print('urldir: ', urldir)
	print(playlist)

	# парсим секции #EXT-X-KEY, складываем в список [файл, метод шифрования, url к ключу]
	chunks = []
	for match in re.finditer(r'(#EXT-X-KEY:(?:(?!#EXT-X-KEY:).)*)', playlist, re.DOTALL):
		# получили секцию, смотрим метод шифрования и URL к файлу ключа
		section = match.group(0)
		section_match = re.match(r'.*?METHOD=(?P<METHOD>[^,\n\r]+)(?:,URI=(?P<URI>[^\n]+)|)', section, re.IGNORECASE)
		key_method = section_match.group('METHOD')
		key_url = section_match.group('URI')
		# удаляем кавычки из URL
		if key_url:
			key_url = key_url.strip("'\"")
		# смотрим список файлов в этой секции, добавляем в список chunks
		for match2 in re.finditer(r'.*?(?P<file>^[^\r\n]+\.ts)(?P<extra>[^\n\r]+)', section, re.IGNORECASE | re.DOTALL | re.MULTILINE):
			file = match2.group('file')
			extra = match2.group('extra')
			file_url = f'{urldir}/{file}{extra}'
			chunks.append({'file_url': file_url, 'key_method': key_method, 'key': key_url, 'file_name': file})

	# для созданного списка файлов, достаем содержимое ключей (URL ключа, меняем на сам текст ключа), используя кэширование (пока что один ключ на все части)
	cached_urls = []
	for chunk in chunks:
		key_url = chunk['key']
		if not key_url:
			continue
		value = ''
		# если url ключа уже скачивалась, достаём кэшированное значение
		for cached_url in cached_urls:
			if key_url == cached_url[0]:
				value = cached_url[1]
				break
		# делаем запрос только если значение не найдено, и кэшируем ответ
		if not value:
			value = requests.get(key_url).text
			cached_urls.append([key_url, value])
		# в общем списке заменяем url ключа на его значение
		chunk['key'] = value
	del cached_urls
	return [chunks, playlist]


def download_m3u8(job, output=None):
	chunks = job[0]
	playlist = job[1]
	try:
		with tempfile.TemporaryDirectory() as _dir:
			print(f'Скачиваем части в каталог {_dir}')

			# если не задано в какой файл объединять все части
			if not output:
				output = f'{_dir}/megred.mp3'

			# проходим по всем частям, скачиваем и расшифровываем при необходимости
			file_num = 1
			for chunk in chunks:
				file_name = str(file_num).zfill(5) + " " + chunk['file_name']
				print(file_name)
				file_num += 1
				# скачиваем как есть или расшифровываем
				if chunk['key']:
					print(chunk['key'])
					key = chunk['key']
					key = key.encode()
					file_in = urlopen(chunk['file_url'])
					iv = file_in.read(16) # Read the iv out - this is 16 bytes long
					ciphered_data = file_in.read() # Read the rest of the data
					file_in.close()
					cipher = AES.new(key, AES.MODE_CBC, iv=iv)  # Setup cipher
					data = unpad(cipher.decrypt(ciphered_data), AES.block_size) # Decrypt and then up-pad the result
				else:
					print(chunk['key'])
					data = requests.get(chunk['file_url']).content
				# пишем данные в файл
				if data:
					file_path = f'{_dir}/{file_name}'
					with open(file_path, 'wb') as audio:
						audio.write(data)
						chunk['file_url'] = file_path
						print(f'Скачан файл {file_name}')
				else:
					print(f'Ошибка получения части {chunk["file_name"]}')

			# на всякий случай сохраняем исходный плейлист
			with open('playlist.txt', 'w') as file:
				file.write(playlist)

			# создаем список для ffmpeg
			ffmpeg_queue = '# queue'
			for chunk in chunks:
				ffmpeg_queue += f"\nfile '{chunk['file_url']}'"
			queue_lst = 'queue.txt'
			with open(queue_lst, 'w') as file:
				file.write(ffmpeg_queue)
			# запускаем склеивание ffmpeg output должен быть .mp3 на конце
			try:
				subprocess.call(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', f'{queue_lst}', '-c', 'copy', f'{output}'])
			except Exception as e:
				print(f'Ошибка склеивания ffmpeg: {e}')
	except Exception as e:
		print(f'Ошибка {e}')
	#return open(output, 'rb').read()
	return output



if __name__ == '__main__':
	# url = sys.argv[1]
	url = 'https://cdn-g-skb-m7.boomstream.com/vod/hash:4fb2ef034568874f4bd2812ee0f49d2d/id:12985.14487.760926.39654069.75373.hls/time:0/data:eyJ2ZXJzaW9uIjoiMS4yLjg1IiwidXNlX2RpcmVjdF9saW5rcyI6InllcyIsImlzX2VuY3J5cHQiOiJ5ZXMifQ==/m57/2022/08/05/gE3hbXDp.mp4/chunklist.m3u8'
	result = parse_m3u8(url)
	# sys.stdout.buffer.write(download_m3u8(result))