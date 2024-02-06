from facebook_scraper import get_posts, set_user_agent

set_user_agent(
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
)

# SMC: 249589865080586
# TODO: Figure out why it keeps getting the same posts
for post in get_posts(group=249589865080586, pages=10, cookies="cookies.txt"):
    print(post['text'][:50])
