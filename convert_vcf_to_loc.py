#!/usr/bin/env python3
# Converts a vcf file to a Relpair .loc file

# ---VCF File Format---
# Ref: https://samtools.github.io/hts-specs/VCFv4.2.pdf
#
# --Meta-information lines-- 
# ##fileformat=VCFv4.2
# ##fileDate=<some_date>
# ##source=<some_source>
# ##reference=<some_ref>
# ##phasing=partial <-- ???
# ##contig=<
# ##arbitrary number of contig lines...
# ##INFO=<
# ##arbitrary number of INFO lines...
# ##FORMAT=<
# ##arbitrary number of FORMAT lines...
#
# --Header line--
# #CHROM    POS ID  REF ALT QUAL    FILTER  INFO    FORMAT  SAMPLE_ID_1  SAMPLE_ID_2  ... SAMPLE_ID_X
#
# --Data line-- (from left to right)
# -Fixed fields-
# CHROM = chromosome identifier
# POS = reference position (1st base = position 1)
# ID = unique identifier of variant if available
# REF = reference base
# ALT = alternate base (can be symbolic - eg. length of allele for STRs)
# QUAL = quality score for ALT
# FILTER = PASS if all filters are passed, otherwise list of codes for filters that failed (only applicable if filters are applied in meta-info section)
# INFO = additional info (eg. AF=0.02,0.04,...;AN=1188)
# -Genotype fields-
# FORMAT = genotype format (specified in meta-info section)
# SAMPLE_FIELDS = genotype information for each sample (eg. 1/2 - i.e. this sample is heterozygous at this locus for alleles 1 and 2)

# ---Relpair .loc format---
# --Header line--
# MARKER1   AUTOSOME    <no. of alleles>   <chr. no.>   <position from start of chr. in Morgans>
# --Allele lines--
# <allele1 name> <allele1 freq.>
# <allele2 name> <allele2 freq.>
# and so on...

import argparse

def main():
    parser = argparse.ArgumentParser(description="Converts a vcf file to a Relpair .loc file")
    parser.add_argument("-i", "--input", required = True, help = "specify input vcf file")
    parser.add_argument("-o", "--output", default = "output.loc", help = "specify filename of output .loc file")
    args = parser.parse_args()

    # Read in data lines
    with open(args.input, "r") as r:
        vcf_lines = []
        for line in r:
            if not line.startswith("#"):
                vcf_lines.append(line)

    # Prepare .loc lines
    loc_lines = []
    marker_type = "AUTOSOME" # hardcoded for now - does a vcf file specify marker type? (i.e. autosome/x-linked)
    position = "0.00" # hardcoded for now - how to convert physical to genetic distance?
    for line in vcf_lines:
        fields = line.split("\t")
        # -header line-
        marker_id = fields[2]
        alleles = fields[4].split(",")
        chr_no = fields[0]
        header_line = f"{marker_id} {marker_type} {len(alleles)} {chr_no} {position}\n"
        loc_lines.append(header_line)
        # -allele lines-
        # obtain allele frequencies
        allele_freqs = [item for item in fields[7].split(";") if item.startswith("AF")]
        allele_freqs = allele_freqs[0].strip("AF=").split(",")
        # write allele lines
        for i in range(len(alleles)):
            allele_line = f"{alleles[i]} {allele_freqs[i]}\n"
            loc_lines.append(allele_line)

    # Write .loc file
    with open(args.output, "w") as w:
        w.writelines(loc_lines)

    print("Done!")

if __name__ == "__main__":
    main()
