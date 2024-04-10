import argparse
from rotate import rotate_image

def get_args():
    psr = argparse.ArgumentParser()
    psr.add_argument('-input_images_dir', '--input_images_dir', help='write input images dir')
    psr.add_argument('-input_image', '--input_image', help='write input image file')
    psr.add_argument('-output_dir', '--output_dir', help='write output dir')

    return psr.parse_args()

if __name__ == "__main__":
    args = get_args()

    rotate_image(args.input_images_dir)

    print(args.input_images_dir)
    print(args.input_image)
    print(args.output_dir)
