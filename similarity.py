'''
This script is used to calculate the similarity between the hashes of the documents.
The script reads the hashes from the files and calculates the similarity between the hashes using the simhash algorithm.
The similarity is calculated based on the hamming distance between the hashes.
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


path = "/opt/lodwalhitesh/pdf_conversion/data/hash/after-deduplication1"

files = list(os.listdir(path))
files.sort()
print("Number of files:", len(files), files)

files = [os.path.join(path, x) for x in files]

all_hashes = []

for file in files:
    try:
        df = pd.read_csv(file)
        hashes = df['hash'].values

        hashes = [str(h) for h in hashes]
        
        all_hashes.extend(hashes)
    except Exception as e:
        print(f"Error reading {file}: {e}")

removed = []
for i in range(len(all_hashes)):
    if all_hashes[i] in removed:
        continue
    for j in range(i + 1, len(all_hashes)):
        try:
            if Simhash(all_hashes[i]).distance(Simhash(all_hashes[j])) < 3:
                removed.append(all_hashes[j])
        except Exception as e:
            print(f"Error computing Simhash for {all_hashes[i]} and {all_hashes[j]}: {e}")

print(removed)
print("Number of removed hashes:", len(removed))

all_hashes = [h for h in all_hashes if h not in removed]
print("Number of remaining hashes:", len(all_hashes))