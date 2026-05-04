
import requests

# CHANGE THIS to your RuneScape 3 username
USERNAME = "IReal7MD"

URL = f"https://secure.runescape.com/m=hiscore/index_lite.ws?player={USERNAME}"

response = requests.get(URL)

if response.status_code != 200:
    print(f"Error: got status code {response.status_code}")
    print("Check the username spelling and that the account is on hiscores")
    exit()

lines = response.text.strip().split("\n")
overall_rank, total_level, total_xp = lines[0].split(",")

print(f"Player: {USERNAME}")
print(f"Total Level: {total_level}")
print(f"Total XP: {int(total_xp):,}")
print(f"Overall Rank: #{int(overall_rank):,}")