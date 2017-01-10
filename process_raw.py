"""
process 2011 raw data
"""

import os
import json
import sys
import re
import argparse
import codecs
import datetime
import langid
from myUtility.indri import TextFactory


def time_to_string(time_stamp):
    return time_stamp.strftime("%Y%m%d")

def get_day_file_list(data_dir,processing_date):
    """according to processing_date, generate a file list
    of files of that date
    """
    
    prefix = time_to_string(processing_date)

    day_files = []
    for single_file in os.walk(data_dir).next()[2]:
        if single_file.find(prefix) != -1:
            single_file = os.path.join(data_dir,single_file)
            day_files.append(single_file)

    return day_files

def get_dest_file(processed_dir,processing_date):
    dest_file = os.path.join(processed_dir,time_to_string(processing_date))
    return dest_file

def get_processing_date(date_id):
    """according to date id, generate processing_date
    """
    start_date = datetime.date(year=2011,month=1,day=23)
    end_date = datetime.date(year=2011,month=2,day=8)
    time_step = datetime.timedelta(days=1)
    processing_date = start_date + time_step*(date_id-1)
    return processing_date


def process_files(day_files,dest_file):
    """process day files and store them in trec format
    in dest_file
    """
    data = {}
    text_factory = TextFactory(dest_file)
    for sinlge_file in day_files:
        #with codecs.open(sinlge_file,'r',"utf-8") as f:
        with open(sinlge_file,'r') as f:
            for line in f:
                #print line
                #print "-"*20
                parts = line.split('\t')
                tid = parts[0]
                code = parts[2]
                if code == "200":
                    #text = parts[4]
                    text = unicode(parts[4],encoding='utf-8')
                    if langid.classify(text)[0]=='en':
                        text_factory.add_document(tid,text)
        #break
    text_factory.write()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("date_id",type=int,choices=range(1,18))
    parser.add_argument("--data_dir","-dr",default="/lustre/scratch/lukuang/microblog/data/raw/2011")
    parser.add_argument("--processed_dir","-pr",default="/lustre/scratch/lukuang/microblog/data/processed/2011")
    args=parser.parse_args()
    
    processing_date = get_processing_date(args.date_id)
    day_files = get_day_file_list(args.data_dir,processing_date)
    dest_file = get_dest_file(args.processed_dir,processing_date)
    
    process_files(day_files,dest_file)
    # while now_day <= end_date:
    #     print "%s" %( time_to_string(now_day) )
    #     now_day += time_step 

if __name__=="__main__":
    main()

