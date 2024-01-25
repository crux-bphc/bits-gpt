import os
import re

input_dir = "./data\\jc_posts"
output_dir = "./data\\jc_posts_cleaned"

files = os.listdir(input_dir)

for doc in files:

    input_path = os.path.join(input_dir, doc)

    with open(input_path, 'r', encoding="utf-8") as handle:
        content = handle.read()
        target = re.compile("<.*?>")
        cleaned = re.sub(target, '', content)
        
        output_path = os.path.join(output_dir, doc)
        with open(output_path, "w+", encoding="utf-8") as newfile:
            newfile.write(cleaned)
            print("Completed document", doc)