import json
import requests
from py621 import objectify

# Custom user agent header for identification within e621
headers = {"User-Agent":"py621/1.1 (by Bugman69 on e621)"}

def handleCodes(StatusCode):
    if StatusCode == 200:
        return
    else:
        Codes = {
            "403": "Forbidden; Access denied",
            "404": "Not found",
            "412": "Precondition failed",
            "420": "Invalid Record; Record could not be saved",
            "421": "User Throttled; User is throttled, try again later",
            "422": "Locked; The resource is locked and cannot be modified",
            "423": "Already Exists; Resource already exists",
            "424": "Invalid Parameters; The given parameters were invalid",
            "500": "Internal Server Error; Some unknown error occurred on the server",
            "502": "Bad Gateway; A gateway server received an invalid response from the e621 servers",
            "503": "Service Unavailable; Server cannot currently handle the request or you have exceeded the request rate limit. Try again later or decrease your rate of requests.",
            "520": "Unknown Error; Unexpected server response which violates protocol",
            "522": "Origin Connection Time-out; CloudFlare's attempt to connect to the e621 servers timed out",
            "524": "Origin Connection Time-out; A connection was established between CloudFlare and the e621 servers, but it timed out before an HTTP response was received",
            "525": "SSL Handshake Failed; The SSL handshake between CloudFlare and the e621 servers failed"}
        raise ConnectionRefusedError(
            "Server connection refused! HTTP Status code: " + str(StatusCode) + " " + Codes[str(StatusCode)])

def isTag(Tag):
    # Since tags can't inherently be NSFW we will always verify tags on e621
    RequestLink = "https://e621.net/tags.json?"
    
    RequestLink += "search[name_matches]="
    RequestLink += Tag

    # Sends the actual request
    eRequest = requests.get(RequestLink, headers=headers)

    # Verify status codes
    handleCodes(eRequest.status_code)

    # Decodes the json into a a list
    eJSON = eRequest.json()

    try:
        # Try to access element name, this throws and error when the tag does not exist or is an alias, check for that in the except
        if eJSON[0]["name"] == Tag:
            return True
        # If the tag's name isn't the tag, assume it's a fluke on e621's servers and return false
        else:
            return False
    except:
        # Redoing the request to check if it's an alias
        RequestLink = "https://e621.net/tag_aliases.json?"
    
        RequestLink += "search[name_matches]="
        RequestLink += Tag

        # Sends the actual request
        eRequest = requests.get(RequestLink, headers=headers)

        # Verify status codes
        handleCodes(eRequest.status_code)

        # Decodes the json into a a list
        eJSON = eRequest.json()

        try:
            # Try to access element name, this WILL throw and exception if it actually does not exist
            if eJSON[0]["antecedent_name"] == Tag:
                # Return the actual tag
                return eJSON[0]["consequent_name"]
            # This shouldn't ever happen, but if it does, consider yourself a special snowflake
            else:
                return False
        except:
            # This tag really does not exist
            return False

# Simple function, gets a single post
def getPost(isSafe, PostID):
    RequestLink = "https://e"

    # Chooses which website to use depending on the isSafe argument
    if isSafe == True:
        RequestLink += "926.net/"
    else:
        RequestLink += "621.net/"
    
    RequestLink += "posts/"

    # Specifies the Post ID
    RequestLink += str(PostID)
    RequestLink += ".json"
    
    # Sends the actual request
    eRequest = requests.get(RequestLink, headers=headers)

    # Verify status codes
    handleCodes(eRequest.status_code)

    # Decodes the json into a a list
    eJSON = eRequest.json()

    # Return posts from the previously defined list
    return objectify.DictProxy(eJSON["post"])

# Simple function, returns a list with posts
def getPosts(isSafe, Tags, Limit, Page, Check):
    RequestLink = "https://e"

    # Chooses which website to use depending on the isSafe argument
    if isSafe == True:
        RequestLink += "926.net/"
    else:
        RequestLink += "621.net/"
    
    RequestLink += "posts.json?"

    # Gives a limit of posts to the api (can be used for per page limits when combined with Page)
    RequestLink += "limit="
    RequestLink += str(Limit)

    # Specifies the page
    RequestLink += "&page="
    RequestLink += str(Page)


    # Handles tag formation
    RequestLink += "&tags="

    for id, Tag in enumerate(Tags):
        if Check == True:
            # Check the tag, it could not exist
            TagCheck = isTag(Tag)

            if TagCheck == False:
                # Tag does not exist, throw an error, this can help devs latter on
                raise NameError("Tag (" + Tag + ") does not exist!")
            elif TagCheck == True:
                # Tag exists and isn't an alias, put it on the request
                RequestLink += Tag
            else:
                # Tag is an alias, use the actual tag on the request
                RequestLink += TagCheck
        else:
            # Don't bother with tag checks
            RequestLink += Tag
        
        if id != (len(Tags) - 1):
            RequestLink += "+"
    
    # Sends the actual request
    eRequest = requests.get(RequestLink, headers=headers)

    # Verify status codes
    handleCodes(eRequest.status_code)

    # Decodes the json into a a list
    eJSON = eRequest.json()

    # Return posts from the previously defined list
    return objectify.DictProxy(eJSON["posts"])

# Simple function, returns a pool from a pool ID
def getPool(isSafe, PoolID):
    RequestLink = "https://e"

    # Chooses which website to use depending on the isSafe argument
    if isSafe == True:
        RequestLink += "926.net/"
    else:
        RequestLink += "621.net/"
    
    RequestLink += "pools.json?"

    # Specifies the pool ID
    RequestLink += "?&search[id]=" + str(PoolID)
    
    # Sends the actual request
    eRequest = requests.get(RequestLink, headers=headers)

    # Verify status codes
    handleCodes(eRequest.status_code)

    # Decodes the json into a a list and selects first element (the pool, if there are more, how?)
    eJSON = eRequest.json()[0]

    # Returns the pool
    return objectify.DictProxy(eJSON)

# Simple function, returns a list of posts from a specific pool ID
def getPoolPosts(isSafe, PoolID):
    # Get ID of all posts in a pool
    poolPosts = getPool(isSafe, PoolID)["post_ids"]

    # Sets posts list
    posts = []

    for postID in poolPosts:
        # For every post id, get a post and append it to the posts list
        posts.append(getPost(isSafe, postID))
    
    # Return the posts list
    return objectify.DictProxy(posts) 
