from http.server import BaseHTTPRequestHandler
import requests
import os
import json


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        api_key = os.environ.get("RIOT_API_KEY")

        if not api_key:
            self.send_error_response(500, "API key not configured")
            return

        game_name = "polar"
        tag_line = "971"
        account_region = "europe"
        platform_region = "me1"

        headers = {"X-Riot-Token": api_key}

        # Step 1: Get PUUID
        account_url = f"https://{account_region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
        account_response = requests.get(account_url, headers=headers)

        if account_response.status_code != 200:
            self.send_error_response(account_response.status_code, "Account lookup failed")
            return

        puuid = account_response.json()["puuid"]

        # Step 2: Get ranked stats
        league_url = f"https://{platform_region}.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}"
        league_response = requests.get(league_url, headers=headers)

        if league_response.status_code != 200:
            self.send_error_response(league_response.status_code, "League lookup failed")
            return

        league_data = league_response.json()

        # Format response
        result = {
            "summoner": f"{game_name}#{tag_line}",
            "queues": []
        }

        for queue in league_data:
            wins = queue["wins"]
            losses = queue["losses"]
            total = wins + losses
            wr = round((wins / total) * 100) if total > 0 else 0

            result["queues"].append({
                "type": queue["queueType"],
                "tier": queue["tier"],
                "rank": queue["rank"],
                "lp": queue["leaguePoints"],
                "wins": wins,
                "losses": losses,
                "winrate": wr
            })

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())

    def send_error_response(self, code, message):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({"error": message}).encode())