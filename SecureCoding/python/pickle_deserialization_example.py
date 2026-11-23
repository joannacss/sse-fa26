import pickle

# Deserialization
with open('data.pickle', 'rb') as f:
    deserialized = pickle.load(f)
    print(deserialized)

