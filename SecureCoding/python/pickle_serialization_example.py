import pickle

data = {'course_id': 'CSE-60770', 'course_name': 'SW Sec Engineering', 'instructor': 'Dr. Santos'}
# Serialization
with open('data.pickle', 'wb') as f:
    pickle.dump(data, f)
print("Data serialized and saved to data.pickle")

# You can use pickle tools to analyze the content of the pickle file
# python3 -m pickletools data.pickle