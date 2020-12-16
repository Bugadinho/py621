import py621

# Get a list of unsafe posts from the pool 6527
SamplePosts = py621.public.getPoolPosts(False, 6527)

SamplePost = SamplePosts[0] # Select the first post from the pool

print("Post ID:")
print(SamplePost.id) # Print the post's ID

print("Post URL:")
print(SamplePost.file.url) # Print the post's media URL