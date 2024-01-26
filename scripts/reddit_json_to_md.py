import json

POSTS_PATH = "data/reddit/posts.json"
EXPORT_PATH = "data/reddit/posts/"

def main():
    with open(POSTS_PATH, "r") as f:
        posts = json.load(f)

    for post in posts:
        fp = EXPORT_PATH+post["id"]+".md"
        with open(fp, "w", encoding="utf-8") as f:
            f.write("# " + post["title"]+"\n")
            f.write(f"## u/{post['author']} (Score: {post['score']}) (Flair: {post['flair']})\n")
            f.write(post["text"]+"\n")
            f.write("\n\n## Comments\n\n")
            for comment in post["comments"]:
                f.write(f"### u/{comment['author']} (Score: {comment['score']})\n")
                f.write(comment["text"]+"\n")
                f.write("\n\n")
            f.write("\n\n")

    print(f"Exported {len(posts)} posts to {EXPORT_PATH}.")

if __name__ == "__main__":
    main()
