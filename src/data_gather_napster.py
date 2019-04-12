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

url= "http://api.napster.com/v2.2/genres/"
params = {
	"apikey" : "YTkxZTRhNzAtODdlNy00ZjMzLTg0MWItOTc0NmZmNjU4Yzk4",
	"limit": 10
}

genres_url= "http://api.napster.com/v2.2/genres"
genres_params = {
	"apikey": "YTkxZTRhNzAtODdlNy00ZjMzLTg0MWItOTc0NmZmNjU4Yzk4"
}
genres = {}

result = requests.get(genres_url, params=genres_params)
print(result.status_code)
temp1 = json.loads(result.text)

for i in temp1["genres"]:
	genres[i["id"]] = i["name"]

print(genres)
print(data_points)
try:
	with open("napster_play.csv", mode="r") as file:
		if(sum(1 for line in file) == 0):
			print("Empty file")
		else:
			csv_reader = csv.DictReader(file, delimiter=',')
			line_count = 0
			for row in csv_reader:
				if line_count == 0:
					print(f'Column names are {", ".join(row)}')
					data_points.append((",".join(row)))
					line_count += 1
				else:
					# print(f'\t{row["n"]} works in the {row[1]} department, and was born in {row[2]}.')
					data_points.append((row["id"], row["name"], row["email"], row["genre"]))
					line_count += 1
except Exception as e:
	print(e)

print(data_points)
random_genre = str(random.choice(list(genres.keys())))
result = requests.get(url + random_genre + "/tracks/top", params=params)
print(result.status_code)
# print(type(result.text))
temp2 = json.loads(result.text)
today = datetime.datetime.now()
print(temp2["tracks"])
tcount = 1
for i in temp2["tracks"]:
	nt = Napster_Track()
	nt.artist_name = i["artistName"]
	nt.id = str(today) + "_" + str(tcount)
	nt.track_name = i["name"]
	nt.track_url = i["previewURL"]
	nt.genre = genres[random_genre]
	data_points.append(nt.__dict__)
	tcount += 1
	with open('napster_play.csv', 'a', newline='') as file:
		fieldnames = ['id', 'artist_name', 'track_name', 'track_url', 'genre']
		writer = csv.DictWriter(file, fieldnames=fieldnames)
		# writer.writeheader()
		writer.writerow({'id': nt.id, 'artist_name': nt.artist_name, 'track_name': nt.track_name,
		                 'track_url': nt.track_url, 'genre':nt.genre})