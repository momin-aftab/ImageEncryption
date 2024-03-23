'''
Contains functions used for image encryption, decryption and key generation.
'''
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

def SplitIntoBlock(image, blockSize: int = 8) -> list:
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

def ShuffleBlocks(blocks, key: str) -> list:
    '''
    Use a key to randomly shuffle image blocks.

    Parameters:
        blocks ( list ) : Array containing image blocks. \n
        key (str) : 16 bit key value used for shuffling.
    Returns:
        blocks ( list ) : Shuffled array of blocks.
    '''
    np.random.seed(int(key))
    np.random.shuffle(blocks)
    return blocks

'''def PermuteBlocks(blocks, key: str):
    np.random.seed(int(key))
    #indexList = np.random.permutation(blocks.size)
    #pBlocks = np.take(blocks, indexList).reshape(blocks.shape)  #This line could be used for the shuffling function.
    for block in blocks:
        block = 255 - block
        block = cv2.rotate(block , cv2.ROTATE_90_CLOCKWISE)
    return blocks'''
    
def RotateBlocks(blocks, key:str) -> list:
    '''
    Use a key value to rotate each image block in a block-list by a multiple of 90 degrees.

    Parameters:
        blocks ( list ): List of image blocks. 
        key ( str ) : 16 bit key used for rotation.
    Returns:
        blocks: Modified rotated block list.
    '''
    for offset,block in enumerate(blocks):
        np.random.seed( int(key) + offset )
        angle = np.random.randint(0,3)
        while angle:
            block = cv2.rotate(block , cv2.ROTATE_90_CLOCKWISE)
            angle -= 1
    return blocks

def InvertBlocks(blocks, key: str) -> list:
    '''
    Returns:
        blocks ( list ) : Modified list of inverted blocks 
    '''
    np.random.seed(int(key))
    binCode : str = ''.join( map (str , np.random.randint(2, blocks.size)))
    for i, value in enumerate(binCode):
        if value != "1":
            pass
        else:
            blocks[i] = 255 - blocks[i]
    return blocks

def unRotateBlocks(blocks, key: str):
    for offset, blocks in enumerate(blocks):
        np.random.seed( int(key) + offset )
        angle = np.random.randint(0,3)
        while angle:
            block = cv2.rotate(block , cv2.ROTATE_90_COUNTERCLOCKWISE)
            angle -= 1
    return blocks

def unShuffleBlocks(blocks: np.ArrayLike, key: str):
    np.random.seed(int(key))
    index = list(range(blocks.size))
    np.random.shuffle(index)
    return blocks[np.argsort(a = index)]

def encrypt(image, blockSize, code):
    '''
    Parameters:
        image : A grayscale CV2 image
        blockSize ( int ): Desired dimensions of blocks for image to be divided in (in pixels)
        code ( str ) : A keyword to be used for encryption and decryption
    Returns:
        image_ : Encrypted image
    '''
    blocks = SplitIntoBlock(image , blockSize)
    keys = GenerateKeys(code)
    blocks = ShuffleBlocks(blocks, keys[0])
    blocks = RotateBlocks(blocks, keys[1])
    blocks = InvertBlocks(blocks, keys[2])
    rows = [np.hstack(blocks[i:i+(image.shape[1] // 8)]) for i in range(0, len(blocks), image.shape[1] // 8)]
    image_ = cv2.vconcat(rows)
    return image_

def decrypt(image, blockSize, code):
    blocks = SplitIntoBlock(image , blockSize)
    keys = GenerateKeys(code)
    blocks = unShuffleBlocks(blocks, keys[0])
    blocks = unRotateBlocks(blocks, keys[1])
    blocks = InvertBlocks(blocks, keys[2])
    rows = [np.hstack(blocks[i:i+(image.shape[1] // 8)]) for i in range(0, len(blocks), image.shape[1] // 8)]
    image_ = cv2.vconcat(rows)
    return image_
