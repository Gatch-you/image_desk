import cv2
import pathlib

def rotate_image(input_dir_name: str):

    input_dir = 'data/images/input/'+input_dir_name
    input_list = list(pathlib.Path(input_dir).glob('**/*.png'))
    print(input_list)

    for i in range(len(input_list)):
        image_file_path = str(input_list[i])
        image_file_name = str(image_file_path.replace(input_dir+'/', '')) 
        print(image_file_path)
        img = cv2.imread(image_file_path)
        print(type(img))

        print(img.shape)

        img_rotate_90_clockwise = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        print('data/images/output/rotate/270rad/rotate_270_'+image_file_name)
        cv2.imwrite('data/images/output/rotate/270rad/rotate_270_'+image_file_name, img_rotate_90_clockwise)

        img_rotate_90_counterclockwise = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        print('data/images/output/rotate/90rad/rotate_90_'+image_file_name)
        cv2.imwrite('data/images/output/rotate/90rad/rotate_90_'+image_file_name, img_rotate_90_counterclockwise)

        img_rotate_180 = cv2.rotate(img, cv2.ROTATE_180)
        print('data/images/output/rotate/180rad/rotate_180_'+image_file_name)
        cv2.imwrite('data/images/output/rotate/180rad/rotate_180'+image_file_name, img_rotate_180)
