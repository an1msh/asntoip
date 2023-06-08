import argparse
import concurrent.futures
import re
import requests
import random

def get_asn_numbers_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def extract_cidrs(asn):
    url = f"https://ipinfo.io/AS{asn}"
    
    user_agents = [
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0'
    ]
    
    headers = {
        'User-Agent': random.choice(user_agents)
    }
    
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
    except requests.HTTPError as http_err:
        raise Exception(f'HTTP error occurred: {http_err}')  
    except Exception as err:
        raise Exception(f'Other error occurred: {err}')
    else:
        return re.findall(r'\d+\.\d+\.\d+\.\d+/\d+', resp.text)


def cidr_validator(cidr):
    try:
        ip, mask = cidr.split('/')
        return len(ip.split('.')) == 4 and all(0<=int(num)<256 for num in ip.split('.')) and (0 <= int(mask) <= 32)
    except ValueError:
        return False

def main(asn_input, file_input, output_file):
    asns = []
    if file_input:
        asns = get_asn_numbers_from_file(file_input)
    else:
        asns = asn_input.split(',')
    
    # Use a ThreadPoolExecutor to send the HTTP requests in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_asn = {executor.submit(extract_cidrs, asn): asn for asn in asns}
        for future in concurrent.futures.as_completed(future_to_asn):
            asn = future_to_asn[future]
            try:
                cidrs = future.result()
                if cidrs:
                    valid_cidrs = [cidr for cidr in cidrs if cidr_validator(cidr)]
                    valid_cidrs.sort()
                    if output_file is None:
                        print('\033[92m' + f'ASN {asn}:' + '\033[0m')  
                        for cidr in valid_cidrs:
                            print(cidr)
                    else:
                        with open(output_file, 'a') as f:
                            for cidr in valid_cidrs:
                                f.write(f"{cidr}\n")
                else:
                    print(f'No CIDRs found for ASN {asn}.')
            except Exception as exc:
                print('\033[91m' + f'Error while processing ASN {asn}: {exc}' + '\033[0m')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract unique CIDRs for given ASNs.')
    parser.add_argument('-a', help='ASN number or comma-separated list of ASN numbers')
    parser.add_argument('-f', help='File containing a list of ASN numbers')
    parser.add_argument('-o', help='Path to the output file to write the CIDRs')
    args = parser.parse_args()

    if args.a is None and args.f is None:
        parser.print_help()
        parser.exit()
    
    main(args.a, args.f, args.o)
