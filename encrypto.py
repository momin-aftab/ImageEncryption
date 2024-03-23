import cv2
import numpy as np
import hashlib

def GenerateKeys(data = str(np.random.randint(1000,9999))):
    '''
    Generates a set of three 16-bit keys.

    Parameters: 
        data (str): Any string value, which will be hashed to generate the keys.

    Returns:
        keys (list[str]) : Array containing the three keys. \n
        data (str) : Initial value given, which can be used for further decryption.
    '''
    raw = str(int(hashlib.md5(str(data)).hexdigest(), 18))
    keys = [
        raw[:16],
        raw[1:17],
        raw[2:18]
    ]
    return keys,data 

def SplitIntoBlock(image, blockSize: int = 8):
    '''
    Split a cv2 image into an array of blocks. \n
    Image dimensions must be a perfect multiple of blockSize.

    Parameters:
        image : A grayscale cv2 image. \n
        blockSize (int) : The desired dimensions of each block.

    Returns:
        blocks : Array containing cv2 blocks of the image
    '''
    blocks = [image[i*blockSize:(i+1)*blockSize, j*blockSize:(j+1)*blockSize,:] for i in range(image.shape[0] // blockSize) for j in range(image.shape[1] // blockSize)]
    return blocks

def ShuffleBlocks(blocks: np.array, key: str):
    #Seed Key
    np.random.shuffle(blocks)
    return blocks
