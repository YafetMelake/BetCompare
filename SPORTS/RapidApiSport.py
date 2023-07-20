import requests

url = "https://odds.p.rapidapi.com/v4/sports"

querystring = {"all":"true"}

headers = {
	"X-RapidAPI-Key": "c7d2f04cc3msh688208d8fd9079dp1d3c72jsnfa46ed8c8d2f",
	"X-RapidAPI-Host": "odds.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())