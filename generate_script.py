import urllib.parse
import urllib.request
import time
import os
import random
import sys

os.makedirs("chunky_soldiers", exist_ok=True)

base_prompts = [
    "funny stock photo of an extremely overweight chunky soldier in green camo, hands up, isolated on white background, photorealistic",
    "obese military general in camo uniform eating a donut, isolated on white background, stock photo style",
    "chunky soldier trying to do a push up, wearing tight camo uniform, exhausted, white background",
    "massively overweight soldier trying to fit into a tiny military jeep, camo, isolated on white background",
    "funny stock photo of a fat soldier crawling under barbed wire, camo uniform, isolated on white background",
    "chunky soldier in tactical gear with camo helmet, surrendering, isolated on solid white background",
    "obese army man running away from a tiny explosion, funny stock photo, white background",
    "chunky soldier stuck in a military tank hatch, camo uniform, absurd, white background",
    "fat soldier saluting very seriously, tight camo uniform, isolated on white background",
    "chunky military soldier holding a tiny rifle, looking confused, camo, white background",
    "obese soldier doing jumping jacks, camo uniform, funny stock photo, white background",
    "chunky soldier eating a giant sandwich in a trench, camo, stock photo, white background",
    "fat army recruit crying during basic training, camo uniform, isolated on white background",
    "chunky soldier trying to climb over a small wall, stuck, camo, white background",
    "extremely round soldier in full camo gear, standing proudly, isolated on white background"
]

# Generate 30 images per run (2x the list)
prompts = base_prompts * 2 

# Force GitHub to print logs instantly
def log(message):
    print(message)
    sys.stdout.flush()

log(f"Starting generation of {len(prompts)} images. Do not close this window!")

for i, prompt in enumerate(prompts):
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
    
    filename = f"chunky_soldiers/soldier_{int(time.time())}_{random.randint(1000, 9999)}.jpg"
    
    log(f"[{i+1}/{len(prompts)}] Fetching image...")
    
    try:
        # 20-second timeout so it doesn't hang forever if the API blocks us
        req = urllib.request.urlopen(url, timeout=20)
        with open(filename, 'wb') as f:
            f.write(req.read())
        log(f"✅ Saved: {filename}")
    except Exception as e:
        log(f"❌ Error on image {i+1}: {e}")
        log("Skipping this one to avoid getting stuck...")
    
    # Wait 30 seconds between images
    if i < len(prompts) - 1:
        log("Waiting 30 seconds to avoid the rate limit...")
        time.sleep(30)

log("Done! Run complete.")
