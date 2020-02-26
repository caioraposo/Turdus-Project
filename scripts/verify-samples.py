import csv
import collections
import re
import subprocess


with open("samples-ncbi.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=",")

    csv_file = [row for row in reader]

data = []
samples = []
samples_sra = []
not_downloaded = []

out = subprocess.run("ls SRA", capture_output=True, shell=True)
sra = out.stdout.decode("utf-8").splitlines()

for sample in sra:
    samples_sra.append(sample[:-4])

for row in csv_file:
    data.append([re.sub("&|\(|\)|\,", "", row[0]), row[1]])
    samples.append(re.sub("&|\(|\)|\,", "", row[0]))


print(len([item for item, count in collections.Counter(samples).items() if count > 1]))
