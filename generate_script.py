import urllib.parse
import urllib.request
import time
import os
import random
import sys
import json

os.makedirs("chunky_soldiers", exist_ok=True)
TRACKER_FILE = "chunky_soldiers/generated_prompts.json"

# Your master list of prompts
base_prompts = [
    "funny stock photo of an extremely obese fat man in a tight green camo military uniform, hands up, isolated on white background",
    "obese fat male military general in camo uniform eating a giant donut, isolated on white background, stock photo",
    "overweight fat male soldier trying to do a push up, exhausted, wearing tight camo uniform, white background",
    "extremely overweight fat male soldier trying to fit into a tiny military jeep, camo, isolated on white background",
    "funny stock photo of a fat male soldier stuck crawling under barbed wire, camo uniform, isolated on white background",
    "chunky fat male soldier in tactical gear with camo helmet, surrendering, isolated on solid white background",
    "obese fat army man running away from a tiny explosion, funny stock photo, white background",
    "fat male soldier stuck in a military tank hatch, camo uniform, absurd, white background",
    "fat male soldier saluting very seriously, tight camo uniform, isolated on white background",
    "chunky fat male soldier holding a tiny rifle, looking confused, camo, white background",
    "obese fat male soldier doing jumping jacks, camo uniform, funny stock photo, white background",
    "fat male soldier eating a giant sandwich in a trench, camo, stock photo, white background",
    "fat male army recruit crying during basic training, camo uniform, isolated on white background",
    "overweight fat male soldier trying to climb over a small wall, stuck, camo, white background",
    "extremely round fat male soldier in full camo gear, standing proudly, isolated on white background",
    # Extra prompts to keep the army growing
    "fat male soldier tangled in a parachute on the ground, camo uniform, funny, white background",
    "overweight male soldier stuck in a narrow doorway, wearing camo, funny stock photo",
    "fat male soldier trying to eat an MRE military ration, spilling it everywhere, white background",
    "chunky male soldier hiding behind a tiny bush, camo uniform, absurd, white background",
    "obese male soldier trying to put on a tiny military helmet, too small, white background"
]

# Shuffle prompts to keep it random
random.shuffle(base_prompts)

def log(message):
    print(message)
    sys.stdout.flush()

# 1. Load already generated prompts
generated_history = []
if os.path.exists(TRACKER_FILE):
    try:
        with open(TRACKER_FILE, 'r') as f:
            generated_history = json.load(f)
    except:
        generated_history = []

# 2. Filter out prompts we've already done
new_prompts = [p for p in base_prompts if p not in generated_history]

if not new_prompts:
    log("All prompts have been generated already! Add more prompts to the script if you want new ones.")
    sys.exit(0)

log(f"Starting generation of {len(new_prompts)} NEW images. Do not close this window!")

for i, prompt in enumerate(new_prompts):
    encoded_prompt = urllib.parse.quote(prompt)
    
    # Negative prompt bans females and vehicles. Random seed stops duplicates.
    negative_prompt = urllib.parse.quote("woman, girl, female, vehicle, car, jeep, duplicate, ugly, deformed")
    seed = random.randint(1, 999999)
    
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&model=flux&negative_prompt={negative_prompt}&seed={seed}"
    
    filename = f"chunky_soldiers/soldier_{int(time.time())}_{random.randint(1000, 9999)}.jpg"
    
    log(f"[{i+1}/{len(new_prompts)}] Fetching image...")
    
    try:
        req = urllib.request.urlopen(url, timeout=25)
        with open(filename, 'wb') as f:
            f.write(req.read())
        log(f"✅ Saved: {filename}")
        
        # Save this prompt to the history file so we never generate it again
        generated_history.append(prompt)
        with open(TRACKER_FILE, 'w') as f:
            json.dump(generated_history, f, indent=2)
            
    except Exception as e:
        log(f"❌ Error on image {i+1}: {e}")
        log("Skipping this one to avoid getting stuck...")
    
    if i < len(new_prompts) - 1:
        log("Waiting 30 seconds to avoid the rate limit...")
        time.sleep(30)

log("Done! Run complete.")
