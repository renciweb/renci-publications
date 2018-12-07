import json
import re
import sys
import getopt
from pprint import pprint

def read_pubs(filenames):
    publications = []
    for filename in filenames:
        print(f'Reading "{filename}"... ', end='')
        try:
            with open(filename, encoding='utf-8') as f:
                year_regex = '.+(\d{4})\.json$'
                match = re.match(year_regex, filename)
                if match:
                    year = match.groups()[0]
                    pubs = json.load(f)
                    publications += pubs[year]
            print(f'Success! ({len(pubs[year])})')
        except FileNotFoundError:
            print(f'Not found')
        except IOError:
            print(f'Read error')
    return publications

def write_pubs(publications, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(publications, f, indent=4)
    except:
        print('A write error occurred')

def main(argv):
    dois_only = False
    outputfile = default_outputfile
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ofile="])
    except getopt.GetoptError:
        print('collect.py -o <outputfile> [dois]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('collect.py -o <outputfile> [dois]')
            sys.exit()
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    if 'dois' in argv:
        print('dois only')
        dois_only = True
    publications = read_pubs(filenames)
    if dois_only == True:
        items = [pub.get('doi', '').strip() for pub in publications if 'doi' in pub and pub['doi'].strip() != '']
    else:
        items = read_pubs(filenames)
    item_type = 'DOIs' if dois_only == True else 'publications'
    print(f' > Imported {len(items)} {item_type}.\n')
    write_pubs(items, outputfile)
    print(f' > Successfully wrote to {outputfile}.\n')

###

json_path = '../library'
filenames = [f'{json_path}/{i}.json' for i in range(2005, 2019)]
default_outputfile = './library.json'

if __name__ == "__main__":
    print()
    main(sys.argv[1:])