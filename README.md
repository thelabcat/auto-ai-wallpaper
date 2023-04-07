# auto-ai-wallpaper
Automatic AI wallpaper changer

This program uses OpenAI davinci-003 and Stable Diffusion hosted on deepai.org to automatically generate an appropriate wallpaper for the day, based on the date and the weather forecast.

This program requires OpenAI API subscription credits and at least one DeepAI API credit to run. Thankfully, these are not expensive.

Currently, this script only works with KDE Plasma 5. Windows support coming soon!

PYTHON DEPENDENCIES:
https://github.com/pashazz/ksetwallpaper
python_weather (a pip package)
openai (a pip package)

To configure, create these files in the working directory:
openai_api_key.txt (with your OpenAI API key)
deepai_api_key.txt (with your DeepAI API key)
weather_location.txt (with your approximate location in plain english, for example "Springfield NT")
generated_wallpapers (empty folder)

You can set this script to run on login in Settings -> Startup and Shutdown -> Autostart. Add the -d flag as a command line option there to make sure only one wallpaper is generated daily.

Thinking about changing this script to run automatically in the background, maybe with a configuration GUI. That way, wallpaper change frequency and other factors are easily adjustable.
