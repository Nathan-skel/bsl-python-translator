from numpy import imag
import requests, re, sys, imageio, os, shutil
from PIL import Image, ImageSequence
from bs4 import BeautifulSoup




#If we put a word on the end of it it should find the correct page on the site so we can grab video
URL = ("https://www.signbsl.com/sign/")
os.mkdir("toDel")



def main():

    listWord = str(input("Please input what you want to say in sign language: "))
    count = 0
    for word in listWord.split(" "):
        try: 

            r=requests.get(get_video(word), stream=True)
            with open(f"./toDel/word{count}.mp4", 'wb') as f:
                for chunk in r.iter_content(chunk_size = 1024*1024):
                    if chunk:
                        f.write(chunk)
            count += 1

        except:
            print("Couldn't Download Video for Word: " + word) 

    for i in range(count):
        convertVideoToGifFile(f'./toDel/word{i}.mp4')

    frames = []
  
    for i in range(count):
        im = Image.open(f"./toDel/word{i}.gif")
        ImageNew = True

        for frame in ImageSequence.Iterator(im):
            frames.append(frame.copy())
            if ImageNew == True:
                frames.pop()
                ImageNew = False

    
    imageio.mimwrite("./output/words.gif", frames, format=".gif", fps=25, )
    shutil.rmtree("./toDel")





def get_video(word):


    try:
        page = requests.get(URL + word)
    except:
        print(word + "Was not on database")
    
    data = page.text

    try:
        vid_link = re.findall('content="(.*?).mp4"', data)
    except:
        print("Couldn't find word: " + word)

  
    return vid_link[0] + ".mp4"


def convertVideoToGifFile(inputFile, outputFile=None):	
    if not outputFile:
        outputFile = os.path.splitext(inputFile)[0] + ".gif"
		
    print("Converting {0} to {1}".format(inputFile, outputFile))

    reader = imageio.get_reader(inputFile)
    fps = reader.get_meta_data()['fps']

    writer = imageio.get_writer(outputFile, fps=fps)
	
    for i,im in enumerate(reader):
        writer.append_data(im)

    writer.close()
    img = Image.open(outputFile)
    img.resize((500,500))
    img.convert('RGBA')
	
    print("\r\nConversion done.")




if __name__ == "__main__":
    main()