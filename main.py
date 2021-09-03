import os
import argparse
import arxiv
from random import randint
from time import sleep
from datetime import datetime

# Just log something into the file "log.txt"
def log(txt):
    with open("log.txt", "a") as myfile:
        myfile.write(txt+'\n')

# Request the arxiv API via arxiv lib for a id list
def getPapers(ids):
    data = arxiv.Search(id_list=ids)
    return [el for el in data.results()]

# Build an arxiv id(YYMM.NNNNN) following 
# this instructinos https://arxiv.org/help/arxiv_identifier   
currentYear = datetime.today().year - 2000

for yy in range(7,currentYear):
    for mm in range(1,12):
        yymm = f"{yy:02d}{mm:02d}"
        formatID = lambda id: f"{yymm}.{i:04d}"
        idLimit = 9999

        """
        As decribed into link above:
            - articles before 2014 has YYMM.NNNN(x4N) id format format
            - articles after 2014 has YYMM.NNNNN(x5N) id format format
        """
        if yy > 14:
            idLimit = 99999
            formatID = lambda id: f"{yymm}.{i:05d}" 
        
        ids = []
        for i in range(1, idLimit):
            try:
                # group 500 ids to order at once for arxiv api
                ids.append(str(formatID(id)))
                if len(ids) < 500: continue

                papers = getPapers(ids)
                print(f'found {len(papers)} papers at batch {yymm}')
                # Some months the arxiv didn't receice yymm.99999 articles, 
                # because this some bacthes has only unexistent ids
                if(len(papers) == 0): break

                for paper in papers:
                    log(paper.entry_id)
                ids = []
                sleep(randint(1,3))
            except Exception as e:
                print(e)
                print('Waiting 5 minutes to try again')
                sleep(300)

