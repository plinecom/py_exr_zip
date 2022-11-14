# py_exr_zip

# Self Introduction
I am Masataka @plinecom, a pipeline engineer at digitalbigmo, Inc.

# What is this?
I was given tens of thousands of large uncompressed OpenEXR files at work, and since OpenEXR has a lossless compression option, I want to convert this large number of uncompressed OpenEXR files to lossless compressed ZIP OpenEXR.
I will record how to batch process them using Python.

# For now, the code
```python:main.py
import OpenEXR
import Imath
import glob
import os

if __name__ == '__main__':

    for path in glob.glob('/foo/bar/*.exr'):
        print(path)
        dir_name = os.path.dirname(path)
        base_name = os.path.basename(path)

        InputFile(path) # Read EXR file
        header = ret.header() # Get OpenEXR header info
        print(header)
        # Change Compression Type
        header['compression'] = Imath.Compression(Imath.Compression.ZIP_COMPRESSION)
        print(header)

        pix = {}
        for ch in header['channels']: # Get channel name from header
            pix[ch] = ret.channel(ch) # Get channel image data
        ret.close() # Close Read File handler

        # Open write file and Set header info
        OutputFile(dir_name + '/' + base_name, header)
        exr.writePixels(pix) # Write Pixel Data
        exr.close() # Close Write File handler
````

# Required Python external modules
* OpenEXR
```terminal:terminal
pip install OpenEXR
```
Download from PyPI using pip, and the Imath module will be installed with it.
However, you will need to install Python's own header file for the build process. If you cannot prepare it, it is easier to build it from Python.

## Explanation of code
### Load EXR file
```python:
        InputFile(path) # Read EXR file
```

### Specify compression method

```python:
        header = ret.header()
        # Change Compression Type
        header['compression'] = Imath.Compression(Imath.Compression.ZIP_COMPRESSION)
```
If you write the compression method directly in text and assign it, it will fail; you must pass an Imath.Compression object initialized with the Imath.Compression.* enumerator. In this case, we want to compress ZIP, so we pass Imath.Compression.ZIP_COMPRESSION. Since we do not change anything other than the compression method, we use the header information of the original file for the rest of the header information.


### Writing files
````python:
        ## Open write file and Set header info
        OutputFile(dir_name + '/' + base_name, header)
        exr.writePixels(pix) # Write Pixel Data
        exr.close() # Close Write File handler
````
Create a file based on the diverted header, specifying the destination to write to, write pixel data, and close the file.

# Explanation of OpenEXR compression options
## Lossless compression options.
### RLE
Run-length compression. It is a simple compression process, but it is very fast because it takes only one pass and requires very little computation. It is very fast because it is a simple compression process that takes only one pass and requires very little computation. Since this alone reduces the size of the file by about 90%, there is no reason to choose uncompressed. ~~~ so don't send me uncompressed OpenEXR files. ~~~
### ZIP
You all know ZIP compression. It compresses an image by dividing it into 16 lines. It can reduce the size to about half of the uncompressed size.
### ZIPS
ZIP compresses images by 16 lines, but ZIPS compresses by 1 line. S is for scan lines, not plural S. I heard a rumor that ZIPS compresses images faster with compositing software such as Nuke, but I have not felt any difference. Compression efficiency is lower than ZIP.
### PIZ
PIZ compresses image data in the frequency domain using a wavelet transform, which is upward compatible with the Fourier transform. While it offers the best compression ratio, it is also very computationally intensive, and the sacrifice in computation time is too great for a compression that is a few percent smaller than ZIP compression.

## Compression that can be lossless or lossy.
### PXR24
PXR24 compresses data with quantization reduced to 24 bits. 16-bit half-precision floating-point data and 16-bit integer data below 24 bits are lossless lossy lossy lossy compression, but 32-bit single-precision floating-point data, etc. are lossy lossy lossy compression. This point should be handled with caution, so if you are not sure, do not select this option.

## Lossy lossy compression option
Other lossy compression options are as follows.
* B44
* B44A
* DWAA
* DWAB

However, I think that most of us use OpenEXR for high quality, and I don't think we will use lossy lossy lossy compression, which may cause an accident due to different decompression results at the delivery destination. If you are a large studio that produces your own masters, it may be an option in terms of storage efficiency.

# advertisement
digitalbigmo Inc. sells beautiful skin plug-ins and provides video VFX production services. If you are interested, please come visit our web page. Let's work together.

https://digitalbigmo.com

# References
About [Python's OpenEXR module (English)](https://excamera.com/sphinx/articles-openexr.html)

[OpenEXR main house (English)](https://www.openexr.com/)

[Wikipedia's OpenEXR page](https://en.wikipedia.org/wiki/OpenEXR)

[Wikipedia's OpenEXR page (Japanese)](https://ja.wikipedia.org/wiki/OpenEXR)

http://yamagishi-2bit.blogspot.com/2020/05/vfxexr.html
