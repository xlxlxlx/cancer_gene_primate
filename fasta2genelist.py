import csv

id = "id"
name = "name"
transcript_biotype = "transcript_biotype"
length = "length"
desc = "description"
data = []

with open('Homo_sapiens.GRCh38.cds.all.fa', 'r') as file:
    for line in file:
        if line.startswith(">"):
            #print(line)
            data.append([id, name, transcript_biotype, length, desc])
            id = line.split(" ")[3].split(":")[1]
            transcript_biotype = line.split(" ")[5].split(":")[1]
            if "gene_symbol" in line:
                name = line.split(" ")[6].split(":")[1]
            else:
                name = ""
            if "description:" in line:
                desc = line.split("description:")[1]
            else:
                desc = ""
            length = 0
        else:
            # Add the length of the line to the accumulated length
            length += len(line.strip())

with open('Homo_sapiens_GRCh38_cds_list.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)
