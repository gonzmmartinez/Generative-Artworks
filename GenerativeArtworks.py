import os
import random

from mutagen.easyid3 import EasyID3
import csv
from Drawing import generate_art
from PIL import Image, ImageEnhance

# set the directory path
path = 'E:\Musika' # here's where I save my music

# create an empty list to store the artist names
artist_names = []

# iterate over each file in the directory
for filename in os.listdir(path):
    # get the full path of the file
    full_path = os.path.join(path, filename)

    # check if the file is an audio file
    if filename.endswith('.mp3') or filename.endswith('.flac'):
        # read the artist name using mutagen
        audio = EasyID3(full_path)
        artist_name = audio['artist'][0] if 'artist' in audio else 'Unknown'
        if artist_name in artist_names:
            pass
        else:
            artist_names.append(artist_name)

# set the file name
filename = 'artists.csv'

# open the file in write mode
with open(filename, 'w', newline='') as file:
    # create a CSV writer object
    writer = csv.writer(file)

    # write the row of data to the CSV file
    writer.writerow(artist_names)

used_nums = [] # create a list to save all the used numbers to avoid repetition

# generate artworks
for artist in artist_names:
    generate_art(f"E:\Code\Projects\Generative_Artworks\Drawings\{artist}_drawing.png",artist)

    # generate a random number and add it to a list with used numbers
    while True:
        random_num = random.randint(1, 25)  # generate a random number between 1 and 25
        if random_num not in used_nums:  # check if the number has not been used
            used_nums.append(random_num)  # add the number to the list of used numbers
            break  # exit the while loop if a valid number is found

    print(f"{artist}: {random_num}")

    # load the two images
    background_image = Image.open(f"E:\Code\Projects\Generative_Artworks\Screenshots\Batch\{random_num}.png")
    foreground_image = Image.open(f"E:\Code\Projects\Generative_Artworks\Drawings\{artist}_drawing.png")

    # Create an enhancer object and darken the background image by a factor of 0.5
    enhancer = ImageEnhance.Brightness(background_image)
    darkened_image = enhancer.enhance(0.25)

    # convert the mode of the foreground image to match the mode of the background image
    if foreground_image.mode != background_image.mode:
        background_image = background_image.convert(foreground_image.mode)

    # resize the foreground image to match the size of the background image
    if foreground_image.size != background_image.size:
        foreground_image = foreground_image.resize(background_image.size)

    # composite the foreground image onto the background image
    result_image = Image.alpha_composite(background_image, foreground_image)

    # save the result image
    result_image.save(f"E:\Code\Projects\Generative_Artworks\Outputs\{artist}_result.png")