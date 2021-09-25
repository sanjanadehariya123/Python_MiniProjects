import os
import json 
from pprint import pprint
import pafy

directory = '/path/to/your/directory/'
videoCounter=0

with open('activity_net.v1-3.min.json') as data_file:    
    data = json.load(data_file)

videos = data ['databse']

for key in videos:
    video=videos[key]
    subset=video['subset']
    annotations=video['annotations']

    label=''
    if len(annotations)!=0
        label=annotations[0]['label']
        label = '/' + label.replace(' ', '_')

    label_dir = directory + subset + label

    if not os.path.exists(label_dir):
        os.makedirs(label_dir)

    url = video['url']

    try:
        video = pafy.new(url)
        best = video.getbest(preftype="flv")
		filename = best.download(filepath=label_dir + '/' + key)
		print ('Downloading... ' )+ str(videoCounter) + '\n'
		videoCounter += 1
    except Exception as inst:
		print ("Error!")


