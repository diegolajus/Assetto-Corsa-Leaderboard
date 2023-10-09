# main.py
import config
from scraper import LeaderboardScraper
import subprocess

url = config.URL

scraper = LeaderboardScraper(url)
scraper.scrape_leaderboard()
subprocess.run(["bash", "automate_git.sh"])
