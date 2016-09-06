import argparse
import logging
import os
import re
import shutil
import sys

from os.path import abspath, isfile, join


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('teamlist', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('--dir', help="Directory for the feedback pdfs (defaults to current dir) ", default=os.getcwd())
    parser.add_argument('-v', '--verbose', action='store_const', const=logging.INFO, dest='loglevel',
                        help='increase output verbosity.')
    parser.add_argument('-d', '--debug', action='store_const', const=logging.DEBUG, dest='loglevel',
                        default=logging.WARNING, help='show debug output (even more than -v).')

    args = parser.parse_args()
    args.dir = abspath(args.dir)

    logging.basicConfig(level=args.loglevel)

    #read in the csv containing the team assignments: 'username','teamnumber'

    #assign the appropriate pdf to each student. one pdf per student named after the students username.
    #pdfs taken from a given input directory with filename: 'XXXX.pdf' where XXXX is the teamnumber
    #student pdfs put in the same directory.

    teams = {}

    for line in args.teamlist:
        username, team = line.strip().split(',')

        if team not in teams:
            teams[team] = []

        teams[team].append(username)

    logging.debug("Teams loaded")
    logging.debug(teams)

    r = re.compile('\d{4}\.pdf')

    files = [f for f in os.listdir(args.dir) if isfile(join(args.dir, f)) and r.match(f)]
    logging.debug(files)

    if len(files) == 0:
        logging.warning("No matching pdfs in directory: %s", args.dir)

    for file in files:
        team = file.split('.')[0]

        if team not in teams:
            logging.warning("Team %s not found in team list." % team)
            continue

        for student in teams[team]:
            logging.debug("Duplicating file %s.pdf for %s" % (team, student))
            shutil.copy(join(args.dir, file), join(args.dir, student + ".pdf"))






if __name__ == '__main__':
    main()