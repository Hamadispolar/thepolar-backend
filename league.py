import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RIOT_API_KEY")

if not API_KEY:
    print("❌ No API key found. Check your .env file.")
    exit()
GAME_NAME = "polar"
TAG_LINE = "971"

# Account routing (super-region) — MENA uses europe
ACCOUNT_REGION = "europe"

# Platform routing — MENA = me1
PLATFORM_REGION = "me1"
# ============================================

headers = {"X-Riot-Token": API_KEY}

# ---- Step 1: Get your PUUID from your Riot ID ----
account_url = f"https://{ACCOUNT_REGION}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{GAME_NAME}/{TAG_LINE}"
account_response = requests.get(account_url, headers=headers)

if account_response.status_code != 200:
    print(f"❌ Account lookup failed: {account_response.status_code}")
    print(account_response.text)
    exit()

account_data = account_response.json()
puuid = account_data["puuid"]

print(f"✅ Found account: {account_data['gameName']}#{account_data['tagLine']}")
print(f"   PUUID: {puuid[:20]}...")

# ---- Step 2: Get ranked stats using PUUID ----
league_url = f"https://{PLATFORM_REGION}.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}"
league_response = requests.get(league_url, headers=headers)

if league_response.status_code != 200:
    print(f"❌ League lookup failed: {league_response.status_code}")
    print(league_response.text)
    exit()

league_data = league_response.json()

if not league_data:
    print("\n⚠️ No ranked data found — have you played ranked this season?")
    exit()

print("\n🏆 RANKED STATS:")
for queue in league_data:
    queue_type = queue["queueType"].replace("_", " ").title()
    tier = queue["tier"]
    rank = queue["rank"]
    lp = queue["leaguePoints"]
    wins = queue["wins"]
    losses = queue["losses"]
    total = wins + losses
    wr = round((wins / total) * 100) if total > 0 else 0

    print(f"\n  {queue_type}")
    print(f"  {tier} {rank} · {lp} LP")
    print(f"  {wins}W / {losses}L · {wr}% WR")