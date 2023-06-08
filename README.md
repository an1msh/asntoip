# ASN CIDR Extractor

Had an idea and asked chatGPT(4) to execute it ¯\_(ツ)_/¯

This script allows you to extract unique CIDRs associated with given ASNs.

## Usage

Run the script with one of the following flags:

- `-a` followed by an ASN number or a comma-separated list of ASN numbers. E.g. `python3 updated-asn.py -a 12345,67890`
- `-f` followed by a path to a file containing a list of ASN numbers. E.g. `python3 updated-asn.py -f asns.txt`
- `-o` followed by a path to the output file to write the CIDRs. If not provided, CIDRs will be printed to the console. E.g. `python3 updated-asn.py -a 12345 -o output.txt`

Note that you must provide either `-a` or `-f` argument. 

If `-a` and `-f` are both provided, the ASN numbers will be extracted from both the comma-separated list and the file.

## Example

`python3 updated-asn.py -a 12345,67890 -o output.txt`

This will extract the CIDRs for ASNs 12345 and 67890 and write them to `output.txt`.

## Requirements

- Python 3
- requests library
- BeautifulSoup4 library
- argparse library
