import json

with open("products.txt", "r") as f:
    data = json.load(f)

img = []
card_title = []
for house in data["Houses"]:
    img.append(house["image"])
    card_title.append(house["House-title"])

print(card_title[0])



