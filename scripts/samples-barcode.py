import csv
import re
import subprocess


with open("Table S1.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")

    next(reader)
    next(reader)
    next(reader)

    samples_csv = [row for row in reader]

with open("lib_AB.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")

    next(reader)

    lib_AB_csv = [row for row in reader]

with open("lib_C.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")

    lib_C_csv = [row for row in reader]


samples = {}
barcodes = {}
not_found = ["U4342", "U4330", "U3572", "GNM1291"]

for row in samples_csv:
    sample_name = row[1].replace(" ", "_")
    name = re.sub("&|\(|\)|\,", "", sample_name)
    f = name.index("_")
    name = name[: name.index("_", f + 1)] + f"_{row[11]}"
    # Parse strange id name
    if "(" in row[0]:
        space = row[0].index(" ")
        row[0] = row[0][:space]
    if "-" in row[0]:
        row[0] = row[0][:3] + row[0][10:]
    samples[row[0]] = name

for row in lib_AB_csv:
    dash = row[1].index("-")
    barcodes[row[1][:dash]] = row[3]

for row in lib_C_csv:
    barcodes[row[2]] = row[7]

for k, v in samples.items():
    print(k, v)

with open("uceasy-conf.csv", "w") as f:
    fieldnames = ["Customer_Code", "i7_Barcode_Seq"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    writer.writeheader()
    for k, v in samples.items():
        if k in not_found:
            k = "U4345"
        writer.writerow({"Customer_Code": v, "i7_Barcode_Seq": barcodes[k]})
