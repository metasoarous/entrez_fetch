#!/home/csmall/pythedge-clstr/bin/python

import argparse
import re
import os
from itertools import islice
from Bio import Entrez


def chunked(iterable, n):
    "Chunk the iterable into chunks of at max size n"
    it = iter(iterable)
    while True:
        chunk = list(islice(it, n))
        if not chunk: 
            break
        yield chunk


accession_re = re.compile("^([a-zA-Z]+)(\d+)$")


def accession_range(start, end):
    "Generator producing all accessions between start and end"
    (start_base, start_int), (end_base, end_int) = map(lambda x: accession_re.match(x).groups(),
            [start, end])
    assert(start_base == end_base)#, "Accession range %s-%s does not have a matching string part" % (start, end))
    base = start_base
    for i in xrange(int(start_int), int(end_int) + 1):
        yield base + str(i)


def parse_accessions_string(acc_string):
    "Parses a string of comma separated accession numbers and/or accession number ranges (separated by hyphens)"
    accs = acc_string.split(',')
    for a in accs:
        dash_split = a.split('-')
        if len(dash_split) == 1:
            yield a
        else:
            for a_ in accession_range(dash_split[0], dash_split[1]):
                yield a_


def get_args():
    parser = argparse.ArgumentParser(prog="fetch_entrez.py")
    parser.add_argument('-e', '--email',
        help="""If you don't specify this and get greedy, you may get cut off from entrez. Will look for the
        environment variable ENTREZ_EMAIL if this flag is not specified.""")
    parser.add_argument('-f', '--format', default='gb')
    parser.add_argument('-b', '--batch-size', type=int, default=100)
    parser.add_argument('-d', '--db', default='nucleotide')
    parser.add_argument('-s', '--accessions-string', action="store_true", default=False,
        help="""If specified, accession_list is interpretted as a string representation of a list of accession
        numbers, first separated by commas, and then by '-' for ranges. For example, 'EU1234,XY3456-3460'.
        Default interprets accession list as a raw list of accessions numbers.""")
    parser.add_argument('accession_list')
    parser.add_argument('output', type=argparse.FileType('w'))
    return parser.parse_args()


def main():
    args = get_args()
    Entrez.email = args.email or os.environ.get('ENTREZ_EMAIL')

    if args.accessions_string:
        accession_list = parse_accessions_string(args.accession_list)
    else:
        accession_list = file(args.accession_list, "r")

    for accessions in chunked(accession_list, args.batch_size):
        result = Entrez.efetch(db=args.db, id=accessions, rettype=args.format, remode="text")
        for line in result:
            args.output.write(line)

    args.output.close()
    if (not args.accessions_string):
        args.accession_list.close()


if __name__ == '__main__':
    main()


