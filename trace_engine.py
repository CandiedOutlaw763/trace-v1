import aiohttp
import asyncio
import json
import os
import random
import random

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
]

def load_local_data():
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "data.json")
    if not os.path.exists(file_path): return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except: return {}

async def check_site(semaphore, session, site_name, site_data, username, callback):
    async with semaphore:
        if not isinstance(site_data, dict) or "url" not in site_data: return

        url = site_data["url"].replace("{}", username)
        error_type = site_data.get("errorType", "status_code")
        
        # Retry Loop (Max 2 Attempts)
        for attempt in range(2):
            try:
                # Randomize Header for every request
                headers = {
                    "User-Agent": random.choice(USER_AGENTS),
                    "Accept-Language": "en-US,en;q=0.9"
                }
                
                async with session.get(url, headers=headers, timeout=15) as response:
                    found = False

                    if error_type == "status_code":
                        if response.status == 200: found = True

                    elif error_type == "message":
                        text = await response.text()
                        error_msg = site_data.get("errorMsg")
                        is_error = False
                        if isinstance(error_msg, list):
                            if any(msg in text for msg in error_msg): is_error = True
                        else:
                            if error_msg in text: is_error = True
                        if not is_error and response.status == 200: found = True

                    elif error_type == "response_url":
                        if str(response.url) == url: found = True

                    if found:
                        # FIRE THE CALLBACK IMMEDIATELY!
                        callback({"type": "found", "site": site_name, "url": url})
                    
                    # If successful (no exception raised), break the retry loop
                    break

            except:
                # If it's the first failure, wait random time and retry
                if attempt == 0:
                    await asyncio.sleep(1)
                    continue
                else:
                    pass # Failed twice, give up

        # Emit progress event regardless of success/failure
        callback({"type": "scanned"})

async def run_trace_async(username, callback):
    data = load_local_data()
    if not data: return

    valid_sites = {k: v for k, v in data.items() if isinstance(v, dict)}
    semaphore = asyncio.Semaphore(15) # Keep traffic control

    async with aiohttp.ClientSession() as session:
        tasks = []
        for site_name, site_data in valid_sites.items():
            task = asyncio.create_task(check_site(semaphore, session, site_name, site_data, username, callback))
            tasks.append(task)
        
        # Wait for all to finish
        await asyncio.gather(*tasks)

# Wrapper to run async code from sync context
def run_trace(username, callback):
    asyncio.run(run_trace_async(username, callback))