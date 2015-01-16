
# Entrez Fetch!

A simple python command line utility for fetching results from GenBank Entrez based on a set of accession numbers.
Batches downloads so that you can download as many as _thousands_ of records.
Based on Biopython.

## How it works

Installing gives you a command line utility -- `entrez_fetch.py` -- that let's you fetch Entrez results either via a list of accession numbers in a file, or via accession ranges presented at the command line. (e.g. `LZ1234-LZ1249,ZY9988`).
You will need to specify an email address for the download, so big brother can track you.
This can be done either via env variable or a command line flag, as you choose (if you use this tool a lot, the former might be a better bet).

The script will download in chunks of size you specify, and after each is done, will start the next batch download.
This has been used to successfully download _thousands_ of sequences, so rest assured the job _will_ get done.
(Should look into multiprocessing in the future, but they might start throttling you if you get too smart... also concurrency sucks in python).

After installing run `entrez_fetch.py -h` from the command line to get full usage.

## Requirements

Really just biopython.
If you're here, you probably won't have trouble setting that up.
If you're on Ubuntu though, you can pretty easily just `apt-get install python-biopython`.
Other OSs... you're on your own.

Once you're there, just `python setup.py install`, and you're done.

Enjoy your entrez.

