import OpenEXR
import Imath
import glob
import os

if __name__ == '__main__':

    for path in glob.glob('/foo/bar/*.exr'):
        print(path)
        dir_name = os.path.dirname(path)
        base_name = os.path.basename(path)

        ret = OpenEXR.InputFile(path)  # Read EXR file
        header = ret.header()  # Get OpenEXR header info
        print(header)
        # Change Compression Type
        header['compression'] = Imath.Compression(Imath.Compression.ZIP_COMPRESSION)
        print(header)

        pix = {}
        for ch in header['channels']:   # Get channel name from header
            pix[ch] = ret.channel(ch)   # Get channel image data
        ret.close()  # Close Read File handler

        # Open write file and Set header info
        exr = OpenEXR.OutputFile(dir_name + '/' + base_name, header)
        exr.writePixels(pix)    # Write Pixel Data
        exr.close()  # Close Write File handler
