# Install biopython
!pip install biopython

from google.colab import drive
drive.mount('/content/drive')

# Import Entrez, Seq input/output, Sequence, and bio.alphabet modules
from Bio import Entrez
from Bio import SeqIO
from Bio import Seq

# Can put any email address below
Entrez.email = "ugwupaschal@gmail.com"

handle = Entrez.esearch(db="nucleotide", term="16S rRNA[gene] AND streptococcus[ORGN] AND Manfredo AND genome")  # search sequences by a combination of keywords
records = Entrez.read(handle)  #store records from search
print(records['Count'])  #This prints how many results there are from your search

#This retrieves the Genbank record for the top result
handle = Entrez.efetch(db="nucleotide", id=records['IdList'][0], rettype="gb", retmode="text")
record = SeqIO.read(handle, "genbank")
handle.close()

#Initialize variables
sixteen_s=[]
seqs=[]
locations=[]

print(record); print("-----------")
print(record.annotations["taxonomy"])

#This goes through each feature of a genbank record (features are listed on the left of a Genbank record)
for feature in record.features:
	if feature.type=='gene' or feature.type == 'rRNA':  #If the feature is a Gene or rRNA then
		if 'gene' in feature.qualifiers:  #This looks to see if /gene= exists in the second column
			if feature.qualifiers['gene'][0]=='16S rRNA':  #If the first occurrence of gene is /gene="16S rRNA"
				if str(feature.location) not in locations:  #If the feature location is not already in the locations list
					print(feature.location)
					locations.append(str(feature.location))  #append the location to the locations list
					print(locations)
					sixteen_s.append(feature)  # append the feature itself to a list of 16S features
					seqs.append(feature.extract(record.seq))  #We can also extract just the sequences

print(len(sixteen_s))

#output_handle=open("/workshop/rRNAs.fa","w")
output_handle=open("rRNAs.fa","w")

#SeqIO.write(final, output_handle, "fasta")
for i in range(len(seqs)):
	output_handle.write(">%s %s %s\n%s\n" % (record.id,record.description,sixteen_s[i].location,str(seqs[i])))  #This outputs the record ID, description, location of the sequence and sequence itself to a file
output_handle.close()
