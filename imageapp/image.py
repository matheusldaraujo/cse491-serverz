# image handling API

images = {}

def add_image(data):
    if images:
        image_num = max(images.keys()) + 1
    else:
        image_num = 0
        
    images[image_num] = data
    return image_num

def get_image(num):
    return images[num]

def get_latest_image():
    image_num = max(images.keys())
    return images[image_num]

def delete_image(num):
	images.pop(num)
	return "Done"

def has_image(num):
	return images.has_key(num)