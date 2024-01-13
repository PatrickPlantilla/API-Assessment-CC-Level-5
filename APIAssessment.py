import tkinter as tk
from io import BytesIO
from PIL import Image, ImageTk
import praw
import requests
import random

reddit = praw.Reddit(client_id='o_dVy2h_REeg6cVJiGaxEA',
                     client_secret='urt1BzBNt7a3fXhb1rieyNSKpy0i0g',
                     user_agent='Patrick API_Assessment')

subreddits = ["MadeMeSmile", "wholesomememes", "aww", "Eyebleach", "UpliftingNews", "AnimalsBeingBros", "HumansBeingBros", "wholesomepics", "wholesomecomics", "wholesomevandalism", "wholesomejerk"]

def get_random_post():
    subreddit_name = random.choice(subreddits)
    subreddit = reddit.subreddit(subreddit_name)
    post = random.choice(list(subreddit.top(limit=100))) # anything more than 50 and it will load way too long, unfortunately

    title = post.title
    url = post.url
    author = post.author
    subreddit_of_origin = post.subreddit

    if url.endswith((".jpg", ".jpeg", ".png")):
        response = requests.get(url)
        img_data = BytesIO(response.content)
        img = Image.open(img_data)

        # This is to make it fit within 800x600 pixels
        if img.size[0] > 800 or img.size[1] > 800:
            width_percent = 800 / float(img.size[0])
            height_percent = 800 / float(img.size[1])
            min_percent = min(width_percent, height_percent)

            new_width = int(float(img.size[0]) * min_percent)
            new_height = int(float(img.size[1]) * min_percent)
        else:
            new_width = img.size[0]
            new_height = img.size[1]

        img = img.resize((new_width, new_height), Image.BICUBIC)
        photo = ImageTk.PhotoImage(img)

        image_label.config(image=photo)
        image_label.image = photo

        title_label.config(text=title)

        author_label.config(text=f"Posted by: u/{author} in r/{subreddit_of_origin}")

root = tk.Tk()
root.title("Wholesome Reddit")
root.geometry("800x1000")
root.resizable(0,0)
root.configure(background="#1a1a1b")

label1 = tk.Label(root, text="Wholesome Reddit Retriever", bg="#ff4500", font=('Arial', 18), anchor="w", fg="white")
label1.pack(fill='x', side="top")

frame = tk.Frame(root, bg="black", height="800", width="800", highlightbackground="white", highlightthickness=1)
frame.pack(side="top")

title_label = tk.Label(frame, text="", font=("Arial", 16), bg="black", fg="white", wraplength="800")
title_label.pack()

author_label = tk.Label(frame, text="", font=("Arial", 14), bg="black", fg="white", wraplength="800")
author_label.pack()

image_label = tk.Label(frame, bg="black")
image_label.pack()

label2 = tk.Label(root, text="Next post should load within 5 seconds of clicking next. If there's nothing, click it again. It must have chosen a post that was a video which cannot be displayed.", bg="#1a1a1b", fg="white", anchor="w", wraplength="730", font=("Arial", 14))
label2.place(rely=1, anchor="sw")

button = tk.Button(root, text="Next", font=("Arial", 18), command=get_random_post)
get_random_post()
button.pack(side='bottom', anchor="se")

root.mainloop()
