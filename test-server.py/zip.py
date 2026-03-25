import os
import zipfile
import base64
import argparse
from math import ceil
 
def zip_folder(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, folder_path)
                zipf.write(abs_path, rel_path)
    print(f"[✔] Đã nén {folder_path} thành {zip_path}")
 
def encode_zip_to_base64_split(zip_path, output_folder, split_size):
    os.makedirs(output_folder, exist_ok=True)
    with open(zip_path, "rb") as f:
        encoded = base64.b64encode(f.read())
 
    total_parts = ceil(len(encoded) / split_size)
    for i in range(total_parts):
        part_data = encoded[i*split_size : (i+1)*split_size]
        part_file = os.path.join(output_folder, f"part_{i+1:03}.txt")
        with open(part_file, "wb") as pf:
            pf.write(part_data)
        print(f"[✔] Tạo {part_file}")
 
    print(f"[✔] Đã encode và split thành {total_parts} phần vào {output_folder}")
 
def decode_base64_split_to_zip(input_folder, output_zip):
    part_files = sorted([f for f in os.listdir(input_folder) if f.startswith("part_")])
    combined_data = b""
    for part_file in part_files:
        with open(os.path.join(input_folder, part_file), "rb") as pf:
            combined_data += pf.read()
        print(f"[✔] Nối {part_file}")
 
    with open(output_zip, "wb") as f:
        f.write(base64.b64decode(combined_data))
 
    print(f"[✔] Đã decode và tạo {output_zip}")
 
def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        zipf.extractall(extract_to)
    print(f"[✔] Đã giải nén {zip_path} vào {extract_to}")
 
def main():
    parser = argparse.ArgumentParser(description="Tool nén thư mục và encode base64 vào txt, hỗ trợ split file, hoặc decode ngược lại.")
 
    parser.add_argument("mode", choices=["encode", "decode"], help="Chế độ thực thi: encode hoặc decode")
    parser.add_argument("--input", required=True, help="Thư mục đầu vào (encode) hoặc file txt / thư mục part (decode)")
    parser.add_argument("--output", required=True, help="Thư mục/đường dẫn đầu ra")
    parser.add_argument("--split", action="store_true", help="Bật chế độ split file")
    parser.add_argument("--split-size", type=int, default=5*1024*1024, help="Dung lượng tối đa mỗi part (bytes). Mặc định 5MB")
 
    args = parser.parse_args()
 
    if args.mode == "encode":
        folder_to_zip = args.input
        zip_file = args.output + ".zip"
        zip_folder(folder_to_zip, zip_file)
 
        if args.split:
            output_folder = args.output
            encode_zip_to_base64_split(zip_file, output_folder, args.split_size)
        else:
            encoded_txt = args.output
            with open(zip_file, "rb") as f:
                encoded = base64.b64encode(f.read())
            with open(encoded_txt, "wb") as f:
                f.write(encoded)
            print(f"[✔] Đã encode vào {encoded_txt}")
 
        os.remove(zip_file)
        print("[✔] Hoàn tất ENCODE.")
 
    elif args.mode == "decode":
        if args.split:
            input_folder = args.input
            zip_file = args.output + ".zip"
            decode_base64_split_to_zip(input_folder, zip_file)
        else:
            input_txt = args.input
            zip_file = args.output + ".zip"
            with open(input_txt, "rb") as f:
                encoded = f.read()
            with open(zip_file, "wb") as f:
                f.write(base64.b64decode(encoded))
            print(f"[✔] Đã decode {input_txt} thành {zip_file}")
 
        extract_folder = args.output
        extract_zip(zip_file, extract_folder)
        os.remove(zip_file)
        print("[✔] Hoàn tất DECODE.")
 
if __name__ == "__main__":
    main()
 
