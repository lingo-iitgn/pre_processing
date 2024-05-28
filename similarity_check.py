'''
This script is used to check the similarity between the hash values of the files.
The script reads the hash values from the files and calculates the similarity between the hash values using the simhash algorithm.
The similarity is calculated based on the hamming distance between the hash values.
The script then saves the similarity values to an output file.
'''


import os
import re
from simhash import Simhash, SimhashIndex
from rich.pretty import pprint
import pandas as pd
from tqdm import tqdm


def get_features(s):
    width = 3
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]


def compute_simhash(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    simhash_value = Simhash(get_features(content))
    return simhash_value


def simhash_diff(hash_1, hash_2):
    """calcuate the difference from two simhash values.
    """
    x = (hash_1 ^ hash_2) & ((1 << 64) - 1)
    ans = 0
    while x:
        ans += 1
        x &= x - 1
    return ans


def compare_and_save_results(simhash_objects_1, simhash_objects_2, output_file):

    index_1 = SimhashIndex(simhash_objects_1, k=3)
    index_2 = SimhashIndex(simhash_objects_2, k=3)

    with open(output_file, 'a', encoding='utf-8') as result_file:
        for filename1, simhash1 in simhash_objects_1:
            for filename2, simhash2 in simhash_objects_2:
                distance = simhash1.distance(simhash2)
                similarity = 1 - distance / 64.0
                result_file.write(f"Similarity between {filename1} and {filename2}: {similarity}\n")


output_file = "/path/to/your/output/results.txt"
path = "/opt/lodwalhitesh/pdf_conversion/data/hash/before-deduplication"
files = list(os.listdir(path))
files.sort()
print("Number of files:", len(files), files)
files = [f"{path}/{x}" for x in files]

for file in tqdm(files):
    print(file)
    df = pd.read_csv(file)
    df = df.drop_duplicates(subset='hash', keep="first")

    s = file.split("/")[-1]
    print(s)
    df.to_csv(f"/opt/lodwalhitesh/pdf_conversion/data/hash/after-deduplication/{s}", index=False)
    print("Deduplication done for", file)


           















































