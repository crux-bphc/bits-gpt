import json
import requests
import datetime

SUBREDDIT_URL = "https://reddit.com/r/BITSPilani"
EXPORT_PATH = "data/reddit/"


def get_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0"
    }
    data = requests.get(url, headers=headers).json()

    #print(json.dumps(data, indent=4))
    return data

def get_posts(url, exclude=None):
    exclude = [] if exclude is None else exclude
    data = get_data(url)
    posts = []
    c = 0
    for ch in data["data"]["children"]:
        if ch["data"]["id"] in exclude:
            continue
        c += 1
        post_obj = {
                "title": ch["data"]["title"],
                "text": ch["data"]["selftext"],
                "id": ch["data"]["id"],
                "permalink": ch["data"]["permalink"],
                "url": ch["data"]["url"],
                "date": datetime.datetime.fromtimestamp(ch["data"]["created_utc"]).strftime("%d %B %Y"),
                "score": ch["data"]["score"],
                "author": ch["data"]["author"],
                "flair": ch["data"]["link_flair_text"],
            }
        posts.append(post_obj)

    print(f"Got {c} posts from {url}.")
    print("Getting comments for these...")

    for post in posts:
        # Get comments
        post_url = "https://reddit.com" + post["permalink"][:-1] + ".json"
        try:
            comments = get_data(post_url)
            comments = comments[1]["data"]["children"]
        except requests.exceptions.JSONDecodeError:
            print(f"Error getting comments for {post_url}")
            post["comments"] = []
            continue

        comments_list = []
        for comment in comments:
            comment_obj = {
                "author": comment["data"]["author"],
                "text": comment["data"]["body"],
                "score": comment["data"]["score"],
            }
            comments_list.append(comment_obj)
        
        post["comments"] = comments_list

    return posts

def main():
    with open(EXPORT_PATH+"posts.json", "r") as f:
        posts = json.load(f)

    new_posts = get_posts(SUBREDDIT_URL+".json?limit=100",exclude=[post["id"] for post in posts])
    
    posts.extend(new_posts)
    with open(EXPORT_PATH+"posts.json", "w") as f:
        json.dump(posts, f, indent=4)

    print(f"Exported all posts.")

if __name__ == "__main__":
    main()