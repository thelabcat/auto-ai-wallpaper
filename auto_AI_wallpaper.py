#!/usr/bin/env python3
#Auto AI wallpaper setter
#S.D.G.

import requests
import urllib.request
import weather_retrieval
import openai
import time
import argparse
import os
import glob
import ksetwallpaper

openai.api_key = open("openai_api_key.txt").read().strip()
DEEPAI_API_KEY = open("deepai_api_key.txt").read().strip()
IMG_WIDTH = 640
IMG_HEIGHT =360

LOCATION = open("weather_location.txt").read().strip()

WALLPAPER_PATH=os.getcwd()+os.sep+"generated wallpapers"

LAST_PROMPT_LOG=os.getcwd()+os.sep+"last_prompt.txt"

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def generate_image_prompt(t, weather):
    print("Calling davinci-003 for prompt...")
    strdate=WEEKDAYS[t.tm_wday]+", "+MONTHS[t.tm_mon]+" "+str(t.tm_mday)
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt="Today is "+strdate+". The forecast for today is as follows: "+weather+\
      "\n\nWrite a text prompt for Stable Diffusion text-to-image that you think will generate an appropriate desktop wallpaper for today:",
      max_tokens=64
    )

    image_prompt = response["choices"][0]["text"].strip()
    print("New prompt:", image_prompt)
    return image_prompt

def generate_image(prompt, out_fn):
    r = requests.post(
        "https://api.deepai.org/api/stable-diffusion",
        data={
            'text': prompt,
            'width': IMG_WIDTH,
            'height': IMG_HEIGHT,
            'grid_size': 1
        },
        headers={'api-key': DEEPAI_API_KEY}
    )

    response = urllib.request.urlopen(r.json()["output_url"])
    data = response.read()
    f = open(out_fn, "wb")
    f.write(data)
    f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Auto AI Wallpaper Setter')
    parser.add_argument("--prompt", "-p", type=str, help="Provide manual prompt for Stable Diffusion.", default=None)
    parser.add_argument("--last-prompt", "-l", action="store_true", help="Use last generated prompt.")
    parser.add_argument("--no-img", "-n", action="store_true", help="Generate/set last prompt only, do not generate new image.")
    parser.add_argument("--daily-only", "-d", action="store_true", help="Only generate a new image if one has not already been generated today.")
    args=parser.parse_args()

    t=time.localtime()
    day_path=WALLPAPER_PATH+os.sep+time.strftime("%D_", t).replace("/", "_")
    out_fn=day_path+time.strftime("%H-%M-%S", t)+".jpg"

    if args.daily_only and glob.glob(day_path+"*"):
        print("Already a wallpaper generated today. Abort.")
        quit()

    print("Getting weather...")
    weather=weather_retrieval.todays_weather(LOCATION)

    if not args.last_prompt and not args.prompt:
        prompt=generate_image_prompt(t, weather)
    elif args.prompt and not args.last_prompt:
        prompt=args.prompt
    elif args.last_prompt and not args.prompt:
        f=open(LAST_PROMPT_LOG)
        prompt=f.read().strip()
        f.close()
    else:
        print("You specified manual prompt and last used prompt. Abort.")
        quit()

    if not args.no_img:
        print("Generating image...")
        generate_image(prompt, out_fn)
        print("Setting wallpaper...")
        ksetwallpaper.setwallpaper(out_fn)
    else:
        print("No image generated.")

    if not args.last_prompt:
        f=open(LAST_PROMPT_LOG, "w")
        f.write(prompt)
        f.close()
        print("Prompt saved.")
    elif args.no_img:
        print("Nothing to do.")
