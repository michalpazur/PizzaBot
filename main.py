import facebook, os, makePizza

os.environ["PYTHONIOENCODING"] = "utf-8"

loc = '<YOUR_PROJECT_LOCATION>'

#this is a test API KEY (not required)
apiKey = '<YOUR_TEST_API_KEY>'
#this is a real API KEY
apiKey = '<YOUR_API_KEY>'

facebook = facebook.GraphAPI(apiKey)
message = makePizza.makePizza(loc)

response = facebook.put_photo(image=open(os.path.join(loc, 'pizza2.png'), 'rb'), message=message)
postId = response['post_id']
print("Photo posted with id: " + postId)