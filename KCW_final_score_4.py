# SANKARANARAYANAN Swathi
# THAVARASA Sanujan
# ALHOUSSAMY Alaa
from tabulate import tabulate
import score_checker as checkScore
from KCW_Team_4 import main as T4
import time
import ntpath
import glob
import os


if __name__ == "__main__":
    directoryPath = input("Enter folder path for data set: ")
    table = [["file", "time (s)", "score"]]
    total = 0
    startTotal = time.time()
    totalTime = 0
    for file in glob.glob(os.path.join(directoryPath, '*.txt')):
        row = []
        head, tail = ntpath.split(file)
        filename = tail or ntpath.basename(head)
        row.append(filename.replace(".txt", ""))
        startTime = time.time()
        T4(file)
        outputFile = "KCW_Team4_" + filename
        row.append("{:.2f}".format(time.time() - startTime))
        scorer = checkScore.Scorer(file, outputFile)
        scorer.exhibition_walk()
        scr = scorer.score
        row.append(scr)
        table.append(row)
        row = []
        total += scr

    table.append(["TOTAL", "{:.2f}".format(time.time() - startTotal), total])
    print(tabulate(table))