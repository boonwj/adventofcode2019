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


def obtain_coloured_layer(layers, height, width):
    colour_layer = [2] * height * width
    for i, _ in enumerate(colour_layer):
        for j, layer in enumerate(layers):
            if layer[i] != "2":
                colour_layer[i] = ' ' if layer[i] == "0" else "X"
                break

    return colour_layer


def decode_image(image_file, height, width):
    layers = read_image_input(image_file, height, width)
    color_layer = obtain_coloured_layer(layers, height, width)
    return [color_layer[i: i + width] for i in range(0, len(color_layer), width)]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(f"usage: {sys.argv[0]} <image file>")
    image_file = sys.argv[1]
    layers = read_image_input(image_file, 6, 25)

    print(compute_checksum(layers))

    for row in decode_image(image_file, 6, 25):
        print(''.join(row))
