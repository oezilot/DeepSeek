

story1 = open("/home/zoe/Projects/deepseek/datasets/story1.txt", "r")
story2 = open("/home/zoe/Projects/deepseek/datasets/story2.txt", "r")
story_files = [story1, story2]

print(story1.readline())

stories = [
    {"title":story.readline(), "text":} for story in story_files for i in range(len(story_files))
]
print(stories)