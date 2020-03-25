import csv
import re
import subprocess


with open("samples-ncbi.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")

    csv_file = [row for row in reader]

samples = []
not_downloaded = []

for row in csv_file:
    name = re.sub("&|\(|\)|\,", "", row[0])
    f = name.index("_")
    name = name[: name.index("_", f + 1)] + f"_{row[1]}"
    samples.append([name, row[1]])

for sample in samples:
    out = subprocess.run(
        f"prefetch -O SRA/ {sample[1]}", shell=True, capture_output=True
    )
    print(out.stdout.decode("utf-8"))

    out = subprocess.run(
        f"mv {sample[1]}/*R1_001.fastq.gz raw-fastq/{sample[0]}_1.fastq.gz", shell=True, capture_output=True
    )
    out = subprocess.run(
        f"mv {sample[1]}/*R2_001.fastq.gz raw-fastq/{sample[0]}_2.fastq.gz", shell=True, capture_output=True
    )
    print(out.stdout.decode("utf-8"))



#if not "has 0 unresolved dependencies" in str(out.stdout):
#    not_downloaded.append(sample)
#
#for sample in not_downloaded:
#    print(sample)
