#!/usr/bin/env python3
#Auto AI wallpaper 2
#S.D.G.

from tkinter import *
from PIL import ImageTk, Image
import shelve
import ksetwallpaper
import os
import glob
import shutil
import threading
import socket
import weather_retrieval
import openai

openai.api_key = open("openai_api_key.txt").read().strip()
DEEPAI_API_KEY = open("deepai_api_key.txt").read().strip()

IMG_WIDTH = 640
IMG_HEIGHT = 360

WEATHER_LOCATION = open("weather_location.txt").read().strip()

WALLPAPER_FOLDER=os.getcwd()+os.sep+"generated_wallpapers"
DATABASE_FN="./images_and_prompts.db"

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

SOCKET_PORT=3353 #Port for contacting an existing copy of the program
SOCKET_RAISEMESSAGE="Raise the GUI!"
SOCKET_CONFIRMMESSAGE="Ok, I'll raise it."
SOCKET_BYTELIMIT=1024
SERVER_TICK=0.2


class MainWindow(Tk):
    def __init__(self, backend):
        super(MainWindow, self).__init__()
        self.title("Auto AI Wallpaper")
        self.backend=backend
        self.build()
        self.reevaluate_list_nav(startup=True)
        self.mainloop()

    def build(self):
        """Construct the window"""
        self.columnconfigure(0, weight=1)

        #--Prompt manager
        self.prompt_frame=Frame(self)

        #Create widgets
        self.prompt_counter=Label(self.prompt_frame, text="Prompt 0 / 0")
        self.prompt_field=Entry(self.prompt_frame)
        
        self.prompt_del_bttn=Button(self.prompt_frame, text="-", command=self.del_prompt)
        self.prompt_last_bttn=Button(self.prompt_frame, text="<", command=self.last_prompt)
        self.prompt_use_bttn=Button(self.prompt_frame, text="use", command=self.use_prompt)
        self.prompt_next_bttn=Button(self.prompt_frame, text=">", command=self.next_prompt)
        self.prompt_gen_bttn=Button(self.prompt_frame, text="+", command=self.gen_prompt)

        #Set up geometry
        self.prompt_frame.grid(row=0, sticky=N+S+E+W)
        self.rowconfigure(0, weight=1)
        
        self.prompt_counter.grid(row=0, columnspan=5, sticky=N+S+E+W)
        self.prompt_frame.rowconfigure(0, weight=1)
        
        self.prompt_field.grid(row=1, columnspan=5, sticky=N+S+E+W)
        self.prompt_del_bttn.grid(row=2, column=0, sticky=N+S+E+W)
        self.prompt_last_bttn.grid(row=2, column=1, sticky=N+S+E+W)
        self.prompt_use_bttn.grid(row=2, column=2, sticky=N+S+E+W)
        self.prompt_next_bttn.grid(row=2, column=3, sticky=N+S+E+W)
        self.prompt_gen_bttn.grid(row=2, column=4, sticky=N+S+E+W)
        self.prompt_frame.rowconfigure(2, weight=1)
        for column in range(5):
            self.prompt_frame.columnconfigure(column, weight=1)

        #--Image manager
        self.img_frame=Frame(self)

        #Create widgets
        self.img_counter=Label(self.img_frame, text="Image 0 / 0")
        img = Image.open("/home/wilbur/Pictures/Desktop Backgrounds/Auto wallpaper/generated_wallpapers/04_09_23_15-38-22.jpg")
        #img = img.resize((img.width//2, img.height//2))
        self.tkimg = ImageTk.PhotoImage(img)
        self.img_field = Canvas(self.img_frame, background="WHITE", width=img.width, height=img.height)
        self.img_field.create_image((0, 0), image=self.tkimg, anchor=N+W)
        
        self.img_del_bttn=Button(self.img_frame, text="-", command=self.del_img)
        self.img_last_bttn=Button(self.img_frame, text="<", command=self.last_img)
        self.img_use_bttn=Button(self.img_frame, text="use", command=self.use_img)
        self.img_next_bttn=Button(self.img_frame, text=">", command=self.next_img)
        self.img_gen_bttn=Button(self.img_frame, text="+", command=self.gen_img)

        #Set up geometry
        self.img_frame.grid(row=1, sticky=N+S+E+W)
        self.rowconfigure(1, weight=1)
        
        self.img_counter.grid(row=0, columnspan=5, sticky=N+S+E+W)
        self.img_frame.rowconfigure(0, weight=1)
        
        self.img_field.grid(row=1, columnspan=5, sticky=N+S)
        self.img_del_bttn.grid(row=2, column=0, sticky=N+S+E+W)
        self.img_last_bttn.grid(row=2, column=1, sticky=N+S+E+W)
        self.img_use_bttn.grid(row=2, column=2, sticky=N+S+E+W)
        self.img_next_bttn.grid(row=2, column=3, sticky=N+S+E+W)
        self.img_gen_bttn.grid(row=2, column=4, sticky=N+S+E+W)
        self.img_frame.rowconfigure(2, weight=1)
        for column in range(5):
            self.img_frame.columnconfigure(column, weight=1)

    #Prompt management commands
    def del_prompt(self):
        if self.prompt_del_bttn["state"]=="disabled":
            return
        #code
        self.reevaluate_list_nav()
        
    def last_prompt(self):
        if self.prompt_last_bttn["state"]=="disabled":
            return
        #code
        self.reevaluate_list_nav()

    def use_prompt(self):
        if self.prompt_use_bttn["state"]=="disabled":
            return
        #code
        self.reevaluate_list_nav()

    def next_prompt(self):
        if self.prompt_next_bttn["state"]=="disabled":
            return
        #code
        self.reevaluate_list_nav()

    def gen_prompt(self):
        pass

    #Image management commands
    def del_img(self):
        if self.img_del_bttn["state"]=="disabled":
            return
        #code
        self.reevaluate_list_nav()

    def last_img(self):
        if self.img_last_bttn["state"]=="disabled":
            return
        #code
        self.reevaluate_list_nav()

    def use_img(self):
        if self.img_use_bttn["state"]=="disabled":
            return
        #code
        self.reevaluate_list_nav()

    def next_img(self):
        if self.img_next_bttn["state"]=="disabled":
            return
        #code
        self.reevaluate_list_nav()

    def gen_img(self):
        if self.img_gen_bttn["state"]=="disabled":
            return
        #code
        self.reevaluate_list_nav()

    def reevaluate_list_nav(self, startup=False):
        """Re-evaluates if buttons should be enabled or not, and where we are in the lists"""
        pass

class ImagePrompt(object):
    def __init__(self, text, images=[]):
        self.text=text
        if type(images)==list:
            self.images=images
        else:
            raise TypeError("Must be a list of image filenames.")
    def delete_image(self, image):
        """Delete an image from this prompt"""
        #Image ID is a string filename
        if type(image)==str and image in self.images:
            self.images.delete(image)
            try:
                shutil.remove(image)
            except FileNotFoundError:
                return True, "image did not exist on filesystem, was removed from database"
            except PermissionError:
                return True, "image permissions locked on filesystem, was removed from database"

        #Image ID is an integer index
        elif type(image)==int:
            try:
                image=self.images[image]
            except IndexError:
                return False, "image index invalid"
            self.delete_image(image)
        else:
            return False, "image ID invalid"
        return True, "image deleted"

    def add_image(self, image_fn):
        """Add an image by filename, MUST already exist"""
        if not os.path.exists(image_fn):
            return False, "image does not exist on filesystem"
        if image in self.images:
            return False, "image with same name already under this prompt"
        self.images.append(image)
        return True, "image added"

    @property
    def is_used(self):
        """Determine wether or not this prompt has been used for still-existing images"""
        return bool(self.images)

    def has_image(self, image):
        return image in self.images

    def __eq__(self, prompt):
        """Comparison method"""
        if type(prompt)==str:
            return self.text==prompt
        elif type(prompt)==type(self):
            return self.text==prompt.text, self.images==prompt.images
        else:
            raise TypeError

    def __str__(self):
        return self.text[:]

class Server(threading.Thread):
    def run(self):
        self.connection=None
        self.signal_raise=False
        self.keep_running=True
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind(('localhost', SOCKET_PORT))
        self.serversocket.listen(1)
        while self.keep_running:
            self.connection, address = serversocket.accept()
            m = self.connection.recv(SOCKET_BYTELIMIT)
            if m.decode().strip()!=SOCKET_RAISEMESSAGE:
                raise NotImplementedError("No way to deal with getting the wrong message back.")
            else:
                self.connection.send(SOCKET_CONFIRMMESSAGE)
                self.signal_raise=True #This will be set back to false when the backend reads it and the GUI is raised
                self.connection.close()
                self.connection=None
            time.sleep(SERVER_TICK)
            
class Backend(object):
    def __init__(self, start_gui=True):
        self.signal_existing_backend() #Can kill this program
        self.start_backend_server()
        self.get_database()
        if start_gui:
            self.start_gui()
        self.mainloop()

    def signal_existing_backend(self):
        """Try to contact existing backend server and tell them to raise the GUI"""
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            clientsocket.connect(('localhost', SOCKET_PORT))
        except ConnectionRefusedError:
            return False #There is no existing instance
        
        clientsocket.send(SOCKET_RAISEMESSAGE)
        m = connection.recv(SOCKET_BYTELIMIT)
        if m.decode().strip()!=SOCKET_CONFIRMMESSAGE:
            raise NotImplementedError("No way to deal with getting the wrong message back.")
        else:
            #Our mission is complete, abort this process.
            clientsocket.close()
            quit()

    def start_backend_server(self):
        """Set up a server to receive backend messages"""
        self.server=Server()
        self.server.start()
    
    def start_gui(self):
        """Runs GUI, halting loop until GUI closes"""
        self.gui=MainWindow(self)

    def get_database(self):
        """Reads the database"""
        self.database=shelve.open(DATABASE_FN)
        if sum([x in self.database.keys() for x in ("prompts", "last_time")])!=2:
            self.database["prompts"]={}
            self.prompts=self.database["prompts"]
            self.mark_last_time()

    def get_prompt_object(self, prompt=None, image=None):
        """retrieve a prompt object given any kind of info about it"""

        #Require info
        if not prompt and not image:
            raise TypeError("must provide prompt or image")

        #If there is no prompt listed, find the prompt that has the image listed for it
        if not prompt:
            for p in self.prompts.values():
                if p.has_image(image):
                    prompt=p
                    break

        #If the prompt listing is an index
        elif type(prompt)==int:
            try:
                prompt=tuple(self.prompts.values())[prompt]
            except IndexError:
                return False, "invalid prompt index"

        #If the prompt is a string
        elif type(prompt)==str:
            try:
                prompt=self.prompts[prompt]
            except KeyError:
                return False, "invalid prompt"

        #If the prompt is provided as an ImagePrompt object, confirm it is in the database
        elif type(prompt)==ImagePrompt:
            if not prompt in self.prompts.values():
                if prompt.text in self.prompts.keys():
                    return False, "prompt exists, but images do not match"
                return False, "invalid prompt"

        #If we searched for the image in prompts but couldn't find it, report faliure'
        if not prompt:
            return False, "invalid image, could not find in database"

        #if the prompt and image were found but do not coincide, report error
        if image and not prompt.has_image(image):
            return False, "prompt did not list image"

        return prompt, "found prompt"

    def delete_image(self, image, prompt=None, del_empty_prompt=True):
        """Delete an image"""
        prompt, debug = self.get_prompt_object(prompt=prompt, image=image)
        if not prompt:
            return False, debug

        prompt.delete_image(image)
        if del_empty_prompt and not prompt.in_use:
            self.delete_prompt(prompt)
            return True, "Image and prompt deleted because that was the last image on the prompt"
        return True, "Image deleted"

    def delete_prompt(self, prompt):
        """Delete a prompt and all its images"""
        prompt, debug = self.get_prompt_object(prompt=prompt)
        if not prompt:
            return False, debug

        for image in prompt.images:
            success, debug = prompt.delete_image(image)
            if not success:
                return False, debug
        del self.prompts[prompt.text]
        return True, "prompt and all sub-images deleted"

    def add_prompt(self, text):
        """Add a new prompt to the database, or retrieve it if it already exists"""
        existing=self.get_prompt_object(prompt=text)
        if existing:
            return existing, "prompt already exists"
        new=ImagePrompt(text)
        self.prompts[text]=new
        return new, "prompt created and added to database"

    def generate_prompt(self, t=None, weather=None, add=True):
        """Generate a new text prompt"""
        if not t:
            t=time.localtime()
        if not weather:
            weather=self.get_current_weather()

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
        if add:
            self.add_prompt(image_prompt)

        return image_prompt

    def add_image(self, image, prompt):
        """Add an image to the database under the given prompt"""
        prompt, debug=self.get_prompt_object(prompt)
        if not prompt:
            return False, debug
        return prompt.add_image(image)

    def gen_image(self, prompt, image_fn=None, confirm_prompt=True, add=True):
        """Generate a new image from the prompt"""
        if confirm_prompt or add:
            prompt, debug=self.get_prompt_object(prompt)
            if not prompt:
                return False, debug
        text=str(prompt)
        if not image_fn:
            image_fn=self.get_new_image_fn()
        r = requests.post(
            "https://api.deepai.org/api/stable-diffusion",
            data={
                'text': text,
                'width': IMG_WIDTH,
                'height': IMG_HEIGHT,
                'grid_size': 1
            },
            headers={'api-key': DEEPAI_API_KEY}
        )

        response = urllib.request.urlopen(r.json()["output_url"])
        data = response.read()
        f = open(image_fn, "wb")
        f.write(data)
        f.close()

        if add:
            return self.add_image(image, prompt)
        return True, "image generated"

    def get_new_image_fn(self, t=None):
        """Make up a new image fn"""
        if not t:
            t=time.localtime()
        day_path=WALLPAPER_FOLDER+os.sep+time.strftime("%D_", t).replace("/", "_")
        return day_path+time.strftime("%H-%M-%S", t)+".jpg"

    def get_current_weather(self, location=WEATHER_LOCATION):
        """Get today's weather forecast"""
        return weather_retrieval.todays_weather(location)

    def mark_last_time(self):
        self.database["last_time"]=int(time.time())

    def mainloop(self):
        """Main loop of the backend. Change wallpapers on schedule, and listen for a GUI raise signal."""
        raise NotImplemented
