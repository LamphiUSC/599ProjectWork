import urllib

image_urls = open('image_urls.txt','r')

#reading the image url text file and downloading the images
for url in image_urls:
	filename = url.replace('\n','').rsplit('/', 1)[-1]
	urllib.urlretrieve(url, 'images/'+filename)
