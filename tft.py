import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RIOT_API_KEY_2")

if not API_KEY:
    print("❌ No API key found. Check your .env file.")
    exit()

# ============================================
# CONFIG
# ============================================
GAME_NAME = "Bolar"
TAG_LINE = "TFT"
ACCOUNT_REGION = "americas"
PLATFORM_REGION = "na1"
# ============================================

headers = {"X-Riot-Token": API_KEY}

# ---- Step 1: Get PUUID ----
account_url = f"https://{ACCOUNT_REGION}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{GAME_NAME}/{TAG_LINE}"
account_response = requests.get(account_url, headers=headers)

if account_response.status_code != 200:
    print(f"❌ Account lookup failed: {account_response.status_code}")
    print(account_response.text)
    exit()

account_data = account_response.json()
puuid = account_data["puuid"]

print(f"✅ Found account: {account_data['gameName']}#{account_data['tagLine']}")

# ---- Step 2: Get TFT ranked stats ----
tft_url = f"https://{PLATFORM_REGION}.api.riotgames.com/tft/league/v1/by-puuid/{puuid}"
tft_response = requests.get(tft_url, headers=headers)

if tft_response.status_code != 200:
    print(f"❌ TFT lookup failed: {tft_response.status_code}")
    print(tft_response.text)
    exit()

tft_data = tft_response.json()

if not tft_data:
    print("\n⚠️ No TFT ranked data — have you played TFT ranked this set?")
    exit()

print("\n♛ TFT RANKED STATS:")
for queue in tft_data:
    queue_type = queue["queueType"]
    tier = queue["tier"]
    rank = queue["rank"]
    lp = queue["leaguePoints"]
    wins = queue["wins"]      # In TFT, "wins" = top 4 finishes
    losses = queue["losses"]  # "losses" = bottom 4 finishes
    total = wins + losses
    top4_rate = round((wins / total) * 100) if total > 0 else 0

    queue_label = "Ranked TFT" if queue_type == "RANKED_TFT" else queue_type
    print(f"\n  {queue_label}")
    print(f"  {tier} {rank} · {lp} LP")
    print(f"  Top 4: {wins} · Bot 4: {losses} · Top4 rate: {top4_rate}%")