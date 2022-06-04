import imageio
import os
import argparse
import numpy as np
import torchvision.utils as vutils
import torchvision.transforms as transforms
from PIL import Image
import re

def save_images(image, fname, col=8):
    #open image here
    transform = transforms.Compose([
        transforms.PILToTensor()
    ])
    image = transform(Image.open(image))
    #image = image/2

    image = vutils.make_grid(image, nrow=col)  # (C, H, W)
    image = image.numpy().transpose([1, 2, 0])
    image = np.clip(255 * image, 0, 255).astype(np.uint8)

    if fname is not None:
        os.makedirs(os.path.dirname(fname), exist_ok=True)
        imageio.imwrite(fname + '.png', image)
    return image


def save_gifs(image_list, fname, col=1):
    """
    :param image_list: [(N, C, H, W), ] in scale [-1, 1]
    """
    image_list = [save_images(each, None, col) for each in image_list]
    os.makedirs(os.path.dirname(fname), exist_ok=True)
    imageio.mimsave(fname + '.gif', image_list)


def parse_arg():
    """Creates a parser for command-line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputDir', type=str, default='~/Desktop/registration_16725/aligned', help="path to the input image")
    parser.add_argument("--name", type=str, default="registration")
    return parser.parse_args()


#logic from https://www.tutorialspoint.com/How-to-correctly-sort-a-string-with-a-number-inside-in-Python
def atoi(text):
    return int(text) if text.isdigit() else text
def naturalKeys(text):
    return [ atoi(c) for c in re.split('(\d+)',text) ]


if __name__ == '__main__':
    args = parse_arg()
    # save gif of depth, rgb, and semantic information
    imagesPath = os.path.expanduser(args.inputDir) + "/"
    imagePathsList = os.listdir(imagesPath)
    imagePathsList.sort(key=naturalKeys)
    # before opening the image skip ds stores
    imagePathsList = imagePathsList[1:]
    print(imagePathsList)
    image_list = [imagesPath + s for s in imagePathsList]
    print(image_list)
    outputDir = '%s/assets/%s' % (os.path.expanduser("~/Desktop"), args.name)
    print(outputDir)
    save_gifs(image_list, outputDir)
