import csv
import re

def Check_image_url(url: str, csv_file_path: str):
    normalized_url = normalize_image_url(url)
    if normalized_url == None:
        print("画像ファイルの形式がjpg, jpeg, pngではないため、排除します:::", url)
        return 
    else:
        try:
            with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                existing_urls = set(row[0] for row in reader if row)

            if url not in existing_urls:
                with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([url])
                    print(f"Added new URL to CSV: {url}")
                    return normalized_url
        except FileNotFoundError:
            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([url])
                print(f"Created new CSV and added URL: {url}")
                return
        except Exception as e:
            print(f"An error occurred: {e}")
            return

def normalize_image_url(url):
    # 正規表現を使って、.jpg, .jpeg, .png の後に続く文字列を削除する
    pattern = re.compile(r'(\.jpg|\.jpeg|\.png)[^\s]*', re.IGNORECASE)
    match = pattern.search(url)
    if match:
        # 拡張子の直後の余計な文字を削除し、正規化されたURLを返す
        return url[:match.start()] + match.group(1)
    else:
        return