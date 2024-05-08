import urllib
import csv
import os

def Download_images(urls: list, save_dir: str, file_name: str, data_size: int):
    print("-----------画像のダウンロード開始----------")
    print("ダウンロード予定枚数:", len(urls))
    try:
        img_count = 0
        for i in range(len(urls)):
            img_bin_data = urllib.request.urlopen(urls[i]).read()
            file_num = i + data_size
            file_path = os.path.join(save_dir, f"{file_name}{file_num}.png")

            with open(file_path, mode="wb") as file:
                file.write(img_bin_data)
            print(f"Downloaded {file_path}")
            img_count += 1
        return img_count
    except:
        print("something accident is happend!")
        pass
