import httpx
import time
import urllib.parse
import json
from colorama import Fore, Style, init
import asyncio

# Inisialisasi Colorama untuk Windows
init()

url = "https://api3.thevertus.app/users/get-data"

headers = {
    "Authorization": None,  # Token akan di-set nanti setelah diambil dari file key.txt
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.159 Mobile Safari/537.36",
    "Sec-Ch-Ua": '"Not A;Brand";v="99", "Chromium";v="119", "Google Chrome";v="119"',
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Sec-Ch-Ua-Mobile": "?1",
    "Sec-Ch-Ua-Platform": '"Android"',
    "Origin": "https://thevertus.app",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://thevertus.app/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Priority": "u=4, i"
}

payload = {}

async def main(token):
    async with httpx.AsyncClient() as client:
        headers["Authorization"] = f"Bearer {token}"

        decoded_token = urllib.parse.unquote(token)
        user_json = urllib.parse.parse_qs(decoded_token).get('user', [''])[0]
        user_obj = json.loads(user_json)
        full_name = f"{user_obj.get('first_name', 'Not found')} {user_obj.get('last_name', 'Not found')}"
        print(f"{Fore.YELLOW}Full Name: {full_name}{Style.RESET_ALL}\n")

        start_time = time.time()
        response = await client.post(url, headers=headers, json=payload)
        end_time = time.time()

        data = response.json()
        formatted_data = {
            "walletAddress": data.get("user", {}).get("walletAddress", "Not found"),
            "balance": f"{data.get('user', {}).get('balance', 0)/10**18:.4f}",
        }
        print(f"{Fore.GREEN}Data: {json.dumps(formatted_data, indent=2)}{Style.RESET_ALL}\n")

async def claim(token):
    async with httpx.AsyncClient() as client:
        headers["Authorization"] = f"Bearer {token}"

        start_time = time.time()
        response = await client.post("https://api3.thevertus.app/game-service/collect", headers=headers, json={})
        end_time = time.time()

        if response.status_code == 201:
            print(f"{Fore.RED}Claim berhasil!{Style.RESET_ALL}")
            claim_data = response.json()
            new_balance = f"{claim_data.get('newBalance', 0)/10**18:.4f}"
            print(f"{Fore.RED}New Balance: {new_balance}{Style.RESET_ALL}\n")
        else:
            print(f"{Fore.RED}Claim gagal!{Style.RESET_ALL}\n")

       

async def run_tasks():
    with open('key.txt', 'r') as file:
        tokens = [line.strip() for line in file]

    print(f"{Fore.CYAN}Hi Sir, welcome back!{Style.RESET_ALL}\n")
    for token in tokens:
        await main(token)
        await asyncio.sleep(5)  # Menambahkan jeda 5 detik antara setiap permintaan
        await claim(token)
        await asyncio.sleep(5)  # Menambahkan jeda 5 detik antara setiap permintaan

if __name__ == "__main__":
    asyncio.run(run_tasks())
