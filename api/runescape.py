
from http.server import BaseHTTPRequestHandler
import requests
import json


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # CHANGE this to your RS3 username
        username = "IReal7MD"

        url = f"https://secure.runescape.com/m=hiscore/index_lite.ws?player={username}"

        response = requests.get(url)

        if response.status_code != 200:
            self.send_error_response(response.status_code, "Hiscores lookup failed")
            return

        lines = response.text.strip().split("\n")

        # First line is overall
        overall_rank, total_level, total_xp = lines[0].split(",")

        skills_list = [
            "Overall", "Attack", "Defence", "Strength", "Constitution", "Ranged",
            "Prayer", "Magic", "Cooking", "Woodcutting", "Fletching", "Fishing",
            "Firemaking", "Crafting", "Smithing", "Mining", "Herblore", "Agility",
            "Thieving", "Slayer", "Farming", "Runecrafting", "Hunter", "Construction",
            "Summoning", "Dungeoneering", "Divination", "Invention", "Archaeology",
            "Necromancy"
        ]

        skills = []
        for i, line in enumerate(lines[1:len(skills_list)], start=1):
            parts = line.split(",")
            if len(parts) >= 3:
                rank, level, xp = parts
                skills.append({
                    "name": skills_list[i],
                    "level": int(level),
                    "xp": int(xp),
                    "rank": int(rank)
                })

        result = {
            "username": username,
            "total_level": int(total_level),
            "total_xp": int(total_xp),
            "overall_rank": int(overall_rank),
            "skills": skills
        }

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