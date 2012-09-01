import facebook 
import urllib
import urllib2

# This is the hard coded url for my classifier for Facebook post moods on Klassif.io
klassify_url = "http://klassif.io/api/classifiers/5/examples"
klassify_valid_classifiers = ["happy", "sad", "angry", "in_love", "none"]

def main():
    print "Please note that this program will not fail gracefully if you enter the wrong Facebook app information."

    klassif_username = raw_input("Enter your username for Klassif.io: \n")
    klassif_password = raw_input("Enter your password for Klassif.io: \n")
    add_authentication(klassif_username, klassif_password)

    mode = raw_input("Do you want to enter posts manually or pull them from public Facebook posts? Enter manual or auto: \n")

    if mode == "auto":
        app_id = raw_input("Enter the app id of your Facebook app: \n")
        app_secret = raw_input("Enter the app secret of your Facebook app: \n")
        print "Getting Facebook access token"
        access_token = facebook.get_app_access_token(app_id, app_secret)
        print "Done."
        search_term = raw_input("Enter a search term to use to find public Facebook posts: \n")
        run_post_classifying_loop(access_token, search_term)
    elif mode == "manual":
        run_manual_classify_loop()
    else:
       print "Invalid mode. Goodbye."

def run_post_classifying_loop(access_token, search_term):
    """ This method will fetch public facebook posts using the search term provided and ask the user to classify the mood of each post. """
    graph = facebook.GraphAPI(access_token)
    response = graph.request("search", {'q': search_term, 'type': "post"})
    posts = response['data']
    for post in posts:
        post_text = post['message']
        print post_text
        classification = raw_input("Please classify this post (happy, sad, angry, in_love, or none): \n") 
        classify_post(post_text, classification)
    print "You've reached the end of the posts! Goodbye." 

def classify_post(post_text, classification):
    """ Classifies a single post by posting to Klassif.io. This method will prompt the user if the classification entered was not a valid input. """
    while not classification in klassify_valid_classifiers:
        classification = raw_input("Invalid classifier. Please enter one of: happy, sad, angry, in_love, or none: \n")
    
    if classification == "none":
        return

    values = {'text': post_text, 'category': classification}
    data = urllib.urlencode(values)
    req = urllib2.Request(klassify_url, data)

    try:
        response = urllib2.urlopen(req)
        print "Success! The classifier has learned."
        return True
    except urllib2.HTTPError, err:
        if err.code == 401:
            print "Classification failure. You are unauthorized to use this classifier. Please check your login credentials."
            return False
        else:
            print "Classification failure. Ensure your data is correct and try again or check the status of klassif.io"
            return False
    except urllib2.URLError, err:
        print "The classification failed. Ensure your data is correct and try again or check the status of klassif.io"
        return False

def run_manual_classify_loop():
    print "Entering manual post classification loop. Type quit at any time to exit."
    while True:
        post_text = raw_input("Please enter the text for a Facebook post: \n")
        if post_text == "quit":
            break

        classification = raw_input("Please classify this post (happy, sad, angry, or in_love): \n")
        if classification == "quit":
            break
             
        if not classify_post(post_text, classification):
            break

    
def add_authentication(klassif_username, klassif_password):
    """ Uses the given username and password to set up authentication in urllib2 for any Klassif.io API calls."""
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()

    top_level_url = "http://klassif.io/api/"
    password_mgr.add_password(None, top_level_url, klassif_username, klassif_password)

    handler = urllib2.HTTPBasicAuthHandler(password_mgr)

    opener = urllib2.build_opener(handler)

    urllib2.install_opener(opener)

    

if __name__ == '__main__':
    main()
