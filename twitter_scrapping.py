# Importing libraries
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
# importing dataset
lk = pd.read_csv("C:/Users/arjun/Downloads/twitter_links.csv")
urls = lk.iloc[:, -1].values

# creating lists
bios = []
follower_follower_list = []
locations = []
websites = []

#fetching data from each url 
for url in urls:
    # using selenium to load url 
    driver = webdriver.Chrome()
    driver.get(url)
    # waiting for 5 sec to load url
    driver.implicitly_wait(5)
    # Getting the html content of page in string 
    html = driver.execute_script("return document.documentElement.outerHTML")
    # using beautiful soup for fetching data 
    soup = BeautifulSoup(html, "html.parser")
    
    #fetching the required data from selected tags
    bio_div = soup.find("div", {"class" : "css-901oao r-1nao33i r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0"})
    follow_count = soup.find("div", {"class" : "css-1dbjc4n r-13awgt0 r-18u37iz r-1w6e6rj"})
    location = soup.find("span", {"class" : "css-901oao css-16my406 r-1bwzh9t r-4qtqp9 r-poiln3 r-1b7u577 r-bcqeeo r-qvutc0"})
    web = soup.find("a", {"data-testid" : "UserUrl"})

    #adding bio to list
    if bio_div is not None:
        bio = bio_div.text
        bios.append(bio)
    else:
        bios.append("Not found")

    #adding follower and following counts in list
    if follow_count is not None:
        cn = follow_count.text
        follower_follower_list.append(cn)
    else:
        follower_follower_list.append("not found")

    #adding location to list
    if location is not None:
        loc = location.text
        locations.append(loc)
    else:
        locations.append("not found")
    
    #adding websites to list
    if web is not None:
        w = web.text
        websites.append(w)
    else:
        websites.append("not found")

#splitting the follower and following count
followers = []
following = []

for item in follower_follower_list:
    # Split the string on the "Following" and "Followers" text
    parts = item.split("Following")
    # Check if there is at least one "Following" in the string
    if len(parts) > 1:
        # The number before "Following" is the number of people they are following
        following.append(parts[0].strip())
        # The number after "Following" and before "Followers" is the number of followers
        followers.append(parts[1].split("Followers")[0].strip())
    else:
        # If there is no "Following" in the string, add "not found" to the following list
        following.append("not found")
        # The number before "Followers" is the number of followers
        followers.append(parts[0].split("Followers")[0].strip())


# creating a dataframe
op = {
    "Bio" : bios,
    "Follower Count" : followers,
    "Following count" : following,
    "Location" : locations,
    "Websites" : websites
}

df = pd.DataFrame(op, columns=['Bio', 'Follower Count', 'Following count', 'Location', 'Websites'])

# Generating output in csv format 

df.to_csv('output1.csv', index=False)
