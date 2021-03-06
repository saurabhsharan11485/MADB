import json
import requests
import random
import datetime
import csv

data_points = []
prev = ""

class Napster_Track:
	def __init__(self):
		self.id = ""
		self.artist_name = ""
		self.track_name = ""
		self.track_url = ""
		self.genre = ""

# with open('napster_files\\napster_play_' + str(datetime.date.today()) + '.csv', 'a+', newline='', encoding="utf-8") as file:
# 	fieldnames = ['id', 'artist_name', 'track_name', 'track_url', 'genre']
# 	writer = csv.DictWriter(file, fieldnames=fieldnames)
# 	writer.writeheader()

url= "http://api.napster.com/v2.2/genres/"
params = {
	"apikey" : "YTkxZTRhNzAtODdlNy00ZjMzLTg0MWItOTc0NmZmNjU4Yzk4",
	"limit": 100
}

genres_url= "http://api.napster.com/v2.2/genres"
genres_params = {
	"apikey": "YTkxZTRhNzAtODdlNy00ZjMzLTg0MWItOTc0NmZmNjU4Yzk4"
}
genres = {
	"Pop": "g.115",
	"Rock": "g.5",
	"Hip-Hop": "g.146",
	"Soul": "g.194",
	"Jazz": "g.299",
	"Electronic": "g.71",
	"Classical": "g.21",
	"Metal": "g.394"
}

print(data_points)
random_genre = str(random.choice(list(genres.keys())))
for i in list(genres.keys()):
	result = requests.get(url + genres[i] + "/tracks/top", params=params)
	print(result.status_code)
	# print(type(result.text))
	temp2 = json.loads(result.text)
	today = datetime.datetime.now()
	print(temp2["tracks"])
	tcount = 1
	for j in temp2["tracks"]:
		nt = Napster_Track()
		nt.artist_name = j["artistName"]
		nt.id = str(today) + "_" + str(tcount)
		nt.track_name = j["name"]
		# print(j["previewURL"])
		nt.track_url = j["previewURL"]
		nt.genre = i
		data_points.append(nt.__dict__)
		tcount += 1
		with open('napster_files\\napster_play_' + str(datetime.date.today()) + '.csv', 'a+', newline='', encoding="utf-8") as file:
			fieldnames = ['id', 'artist_name', 'track_name', 'track_url', 'genre']
			writer = csv.DictWriter(file, fieldnames=fieldnames)
			writer.writerow({'id': nt.id, 'artist_name': nt.artist_name.replace(",",""), 'track_name': nt.track_name.replace(",", ""),
			'track_url': nt.track_url.replace(",",""), 'genre':nt.genre})