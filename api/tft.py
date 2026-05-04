from http.server import BaseHTTPRequestHandler
import requests
import os
import json


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        api_key = os.environ.get("RIOT_API_KEY_2")

        if not api_key:
            self.send_error_response(500, "API key not configured")
            return

        # CHANGE these two lines to your TFT account
        game_name = "Bolar"
        tag_line = "TFT"
        account_region = "americas"
        platform_region = "na1"

        headers = {"X-Riot-Token": api_key}

        # Step 1: Get PUUID
        account_url = f"https://{account_region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
        account_response = requests.get(account_url, headers=headers)

        if account_response.status_code != 200:
            self.send_error_response(account_response.status_code, "Account lookup failed")
            return

        puuid = account_response.json()["puuid"]

        # Step 2: Get TFT ranked stats
        tft_url = f"https://{platform_region}.api.riotgames.com/tft/league/v1/by-puuid/{puuid}"
        tft_response = requests.get(tft_url, headers=headers)

        if tft_response.status_code != 200:
            self.send_error_response(tft_response.status_code, "TFT lookup failed")
            return

        tft_data = tft_response.json()

        # Format response
        result = {
            "summoner": f"{game_name}#{tag_line}",
            "queues": []
        }

        for queue in tft_data:
            top4 = queue["wins"]    # In TFT: wins = top 4 finishes
            bot4 = queue["losses"]  # losses = bottom 4 finishes
            total = top4 + bot4
            top4_rate = round((top4 / total) * 100) if total > 0 else 0

            result["queues"].append({
                "type": queue["queueType"],
                "tier": queue["tier"],
                "rank": queue["rank"],
                "lp": queue["leaguePoints"],
                "top4": top4,
                "bot4": bot4,
                "top4_rate": top4_rate
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