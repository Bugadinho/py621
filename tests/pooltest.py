import py621

# Create an unsafe api instance
api = py621.public.api(py621.types.e621)

# Get a Pool object from the pool 6527
pool = api.getPool(6527)

# Get posts from the Pool object
SamplePosts = pool.getPosts()

SamplePost = SamplePosts[0] # Select the first post from the pool

print("Post ID:")
print(SamplePost.id) # Print the post's ID

print("Post URL:")
print(SamplePost.file.url) # Print the post's media URL