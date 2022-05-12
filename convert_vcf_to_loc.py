#!/usr/bin/env python3
# Converts a vcf file to a Relpair .loc file

import argparse

def main():
    parser = argparse.ArgumentParser(description="Converts a vcf file to a Relpair .loc file")
    parser.add_argument("-i", "--input", required = True, help = "specify input vcf file")
    parser.add_argument("-o", "--output", default = "output.loc", help = "specify filename of output .loc file")
    args = parser.parse_args()

if __name__ == "__main__":
    main()
    