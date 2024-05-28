'''
# explain about the code
- This code is used to calculate the similarity between the documents using the simhash algorithm. 
- The simhash algorithm is used to calculate the similarity between the documents based on the hash values of the documents.
- The code reads the content of the documents and calculates the simhash value for each document.
- The simhash value is then used to calculate the similarity between the documents.
- The similarity is calculated based on the hamming distance between the simhash values of the documents.
- The code then saves the similarity values to an output file.

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

parent = "/opt/lodwalhitesh/pdf_conversion/data/corpus_1"
for path, directories, files in os.walk(parent):
    data = []
    s = path.split("/")[-1]
    for file in tqdm(files, leave=False, desc=s):
        file_path = os.path.join(path, file)
        simhash_value = compute_simhash(file_path)
        
        data.append({
            "file": file_path,
            "hash": simhash_value.value
        })


    if len(data) == 0:
        continue
    
    df = pd.DataFrame(data)
    df.to_csv(f"/opt/lodwalhitesh/pdf_conversion/data/hash/before-deduplication/{s}.csv", index=False)

