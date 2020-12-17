import py621

# Create a safe api instance
api = py621.public.api(py621.types.e926)

# Set the tags we want 
tags = ["protogen", "anthro"]

# Get a list of posts with the tags contained in the above list and don't check for tag validity
SamplePosts = api.getPosts(tags, 10, 1, False)

SamplePost = SamplePosts[0] # Select the first post from the list

print("Post ID:")
print(SamplePost.id) # Print the post's ID

print("Post URL:")
print(SamplePost.file.url) # Print the post's media URL