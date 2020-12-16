from py621.public import Pool

# Get a list of not safe for work posts from the pool 6527
pooltest = Pool(False, 6527)
SamplePosts = pooltest.getPoolPosts()

SamplePost = SamplePosts[0] # Select the first post from the pool

print("Post ID:")
print(SamplePost["id"]) # Print the post's ID

print("Post URL:")
print(SamplePost["file"]["url"]) # Print the post's media URL