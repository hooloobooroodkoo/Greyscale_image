"""
This module contains class for compressing, decompressing and turninig into black-white of the picture.
"""
import numpy as np
from arrays import Array2D, Array
from PIL import Image, ImageOps
import sys


class GrayscaleImage:
    """
    This class includes methods for turning picture into black and white,
    compressing and decompressing"""

    def __init__(self, nrows: int, ncols: int):
        """
        Represents the future image as 2D Array.
        """
        self.image_array = Array2D(nrows, ncols)
        self.clear(0)

    def height(self) -> int:
        """
        Returns the height of the picture.
        """
        return self.image_array.num_rows()

    def width(self) -> int:
        """
        Returns the width of the picture.
        """
        return self.image_array.num_cols()

    def clear(self, value: int):
        """
        Changes all value in the array to given value.
        """
        if 0 <= value <= 255:
            for row in range(self.height()):
                for col in range(self.width()):
                    self.image_array[row, col] = value
        else:
            raise ValueError("The value should be between 0 and 255.")

    def __getitem__(self, row_col: tuple) -> [int, str, list, tuple, object]:
        """
        Returns the value of the array in the given coordinates.
        """
        return self.image_array[row_col[0], row_col[1]]

    def __setitem__(self, row_col: tuple, value: [int, str, list, tuple, object]):
        """
        Sets the value to the given coordinates of the array.
        """
        if 0 <= value <= 255:
            self.image_array[row_col[0], row_col[1]] == value
        else:
            raise ValueError("The value should be between 0 and 255.")


    def from_file(self, path: str):
        """
        Creates the grey-version copy of the picture.
        """
        img = Image.open(path)
        image_grayscale = ImageOps.grayscale(img)
        img_array = np.array(image_grayscale)
        pixels = image_grayscale.load()
        for row in range(self.height()):
            for col in range(self.width()):
                self.image_array[row, col] = pixels[row, col]

    def lzw_compression(self) -> list:
        """
        Compress an image array to a list of output symbols.
        """
        uncompressed = ''
        dict_size = 256

        for row in range(self.height()):
            for col in range(self.width()):
                uncompressed += str(chr(self.image_array[row, col]))

        dictionary = {chr(i): i for i in range(dict_size)}
        
        w = ""
        result = []
        for c in uncompressed:
            wc = w + c
            if wc in dictionary:
                w = wc
            else:        
                result.append(dictionary[w])
                # Add wc to the dictionary.
                dictionary[wc] = dict_size
                dict_size += 1
                w = c
       
        if w:
            result.append(dictionary[w])
        return result


    def lzw_decompression(self, compressed: list) -> str:
        """
        Decompress a list of output ks to a string.
        """
        from io import StringIO
    
        dict_size = 256
        dictionary = {i: chr(i) for i in range(dict_size)}
    
        # use StringIO, otherwise this becomes O(N^2)
        # due to string concatenation in a loop
        result = StringIO()
        w = chr(compressed.pop(0))
        result.write(w)
        for k in compressed:
            if k in dictionary:
                entry = dictionary[k]
            elif k == dict_size:
                entry = w + w[0]
            else:
                raise ValueError('Bad compressed k: %s' % k)
            result.write(entry)
    
            # Add w+entry[0] to the dictionary.
            dictionary[dict_size] = w + entry[0]
            dict_size += 1
    
            w = entry
        return result.getvalue()
        
    def test_compression_decompression(self, symbols: str):
        """
        Tests the compression and decompression methods.
        """
        idx = 0
        rows = []
        for row in range(self.height()):
            nrow = []
            for col in range(self.width()):
                pixel = ord(symbols[idx])
                nrow.append(pixel)
                idx += 1
            rows.append(nrow)
        image_array = np.array(rows)
        new_img = Image.fromarray(image_array)
        img_rotate = new_img.rotate(-90, expand=1)
        img_rotate.show()


def main():
    path = input("Enter the path to the picture: ")
    img = Image.open(path)
    width, height = img.size
    image_grayscale = GrayscaleImage(width, height)
    image_grayscale.from_file(path)
    compressed_image = image_grayscale.lzw_compression()
    print(f"After compressing: {len(compressed_image)}")
    decompressed_image = image_grayscale.lzw_decompression(compressed_image)
    print(f"After decompressing: {len(decompressed_image)}")
    image_grayscale.test_compression_decompression(decompressed_image)

if __name__ == "__main__":
    main()