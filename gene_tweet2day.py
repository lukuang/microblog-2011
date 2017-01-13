"""
generate tweet2day file
"""

import os
import json
import sys
import re
import argparse
import codecs

def get_start_time(data_dir):
    start_times = {}

    all_files = os.walk(data_dir).next()[2]
    all_files.sort()

    for file_name in all_files:
        m = re.search("^(2011\d+)-",file_name)
        if not m:
            print "Wrong file name %s" %(file_name)
            sys.exit(-1)
        else:
            day = m.group(1)
            if day not in start_times:
                with open( os.path.join(data_dir,file_name) ) as f:
                    for line in f:
                        parts = line.split('\t')
                        tid = int(parts[0])
                        start_times[day] = tid
                        break
    return start_times


def get_tweet_ids(qrel_file):
    tweetids = []
    with open(qrel_file) as f:
        for line in f:
            parts = line.split()
            tid = int(parts[2])
            tweetids.append(tid)

    return tweetids

def gene_tweet2day(start_times,tweetids):
    tweet2day = {}
    increasing_days = sorted(start_times.keys())

    #use the starting tid of each day to determine the
    #day of a tweet. If found the "first" starting tid
    #of a day that is bigger than a tweet's id, the 
    #previous day of the day is the tweet's generation
    #day

    for tid in tweetids:
        previous_day = increasing_days[0]
        #skip the first day 
        for day in increasing_days[1:]:
            if tid - start_times[day] < 0:
                break
            else:
                previous_day = day
        tweet2day[tid] = previous_day
        
    return tweet2day

def write_tweet2day(tweet2day,dest_file):
    with open(dest_file,"w") as f:
        for tid in tweet2day:
            day = tweet2day[tid]
            f.write("%d\t%s\n" %(tid,day))





def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data_dir","-dr",default="/lustre/scratch/lukuang/microblog/data/raw/2011")
    parser.add_argument("--qrel_file","-qf",default="/lustre/scratch/lukuang/microblog/data/raw/official_eval/qrels")
    parser.add_argument("dest_file")
    args=parser.parse_args()

    start_times = get_start_time(args.data_dir)
    tweetids = get_tweet_ids(args.qrel_file)
    tweet2day = gene_tweet2day(start_times,tweetids)
    write_tweet2day(tweet2day,args.dest_file)


if __name__=="__main__":
    main()

