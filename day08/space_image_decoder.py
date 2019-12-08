"""
Space Image Decoder

Images are sent as a series of digits that each represent the color of a single pixel.
The digits fill each row of the image left-to-right, then move downward to the next row,
filling rows top-to-bottom until every pixel of the image is filled.

Each image actually consists of a series of identically-sized layers that are filled in this way.
So, the first digit corresponds to the top-left pixel of the first layer,
the second digit corresponds to the pixel to the right of that on the same layer, and so on until the last digit,
which corresponds to the bottom-right pixel of the last layer.

For example, given an image 3 pixels wide and 2 pixels tall, the image data 123456789012 corresponds to the following image layers:

Layer 1: 123
         456

Layer 2: 789
         012

The image you received is 25 pixels wide and 6 pixels tall.
"""
import sys

def read_image_input(image_file, width, height):
    layers = []
    with open(image_file) as image_f:
        layers = image_layers(image_f.read(), width, height)

    return layers


def image_layers(image_data, width, height):
    layer_size = width * height
    layers = [image_data[i:i+layer_size] for i in range(0, len(image_data), layer_size)]
    return layers

def compute_checksum(layers):
    """
    The layer that contains the fewest 0 digits.
    Determine the number of 1 digits multiplied by the number of 2 digits?
    """
    min_zero = None
    min_layer = None
    for layer in layers:
        zeroes = layer.count('0')
        if not min_zero or zeroes < min_zero:
            min_zero = zeroes
            min_layer = layer

    return min_layer.count('1') * min_layer.count('2')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(f"usage: {sys.argv[0]} <input file>")
    input_file = sys.argv[1]
    layers = read_image_input(input_file, 25, 6)

    print(compute_checksum(layers))