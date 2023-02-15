# SANKARANARAYANAN Swathi
# THAVARASA Sanujan
# ALHOUSSAMY Alaa
import ntpath

totalPaintings = 0
landscape_flag = 0


class Painting():
    def __init__(self, pID, type, numberOfTags, tags):
        self.pID = pID
        self.type = type
        self.numberOfTags = numberOfTags
        self.tags = tags


# function that reads input file and groups portraits directly (before sorting)
def read_and_group(file):
    global totalPaintings
    global landscape_flag
    final = []
    with open(file, mode="r") as f:
        line = f.readline()
        # list of TOTAL paintings
        totalPaintings = str(line)
        line = f.readline()
        # for portrait pairing
        temp_portrait = []
        ID = 0
        while line:
            # remove \n and split by white space (into array)
            split = line.strip().split(" ")
            # landscape condition, directly append to final list
            if split[0] == "L":
                final.append(Painting(ID, split[0], split[1], set(split[2:])))
            else:
                # portrait condition => array of portrait pairs
                if (len(temp_portrait) == 0):
                    temp_portrait.append(
                        Painting(ID, split[0], split[1], set(split[2:])))
                elif (len(temp_portrait) == 1):
                    temp_portrait.append(
                        Painting(ID, split[0], split[1], set(split[2:])))
                    final.append(temp_portrait)
                    temp_portrait = []
            ID += 1
            line = f.readline()

        if (len(temp_portrait) == 1):
            final.append(temp_portrait)
        # conditional for first input file (all landscapes)
        if(len(final) == int(totalPaintings)):
            landscape_flag = 1
    return final


# function that reads input file and returns list of paintings, portraits not paired
def read_only(file):
    global totalPaintings
    global landscape_flag
    final = []
    with open(file, mode="r") as f:
        line = f.readline()
        # list of LANDSCAPES
        LoL = []
        # list of TOTAL paintings
        totalPaintings = str(line)
        line = f.readline()
        ID = 0
        while line:
            # remove \n and split by white space (into array)
            split = line.strip().split(" ")
            # landscape condition, directly append to final list
            final.append(Painting(ID, split[0], split[1], set(split[2:])))
            ID += 1
            line = f.readline()
    return final


# sorting function based on # of tags in frame
def sort_by_number_of_tags(frames):
    return sorted(frames, key=lambda x: (x[0].numberOfTags+x[1].numberOfTags) if isinstance(x, list) else (x.numberOfTags), reverse=True)


def groupPortraits(ungrouped):
    sortedList = list()
    temp_portrait = []
    for painting in ungrouped:
        # landscape condition, directly append to final list
        if painting.type == "L":
            sortedList.append(painting)
        else:
            # portrait condition => array of portrait pairs
            if (len(temp_portrait) == 0):
                temp_portrait.append(painting)
            elif (len(temp_portrait) == 1):
                temp_portrait.append(painting)
                sortedList.append(temp_portrait)
                temp_portrait = []
    return sortedList


def comparePaintings(frames):
    length = len(frames)
    for index in range(0, length):
        best_object = 0
        score = 0
        if length > 5000:
            maxRange = index + 500 if (index + 500) < length else length
        else:
            maxRange = length
        for nextIndex in range(index+1, maxRange):
            scorepair = local_robotic_satisfaction(
                frames[index], frames[nextIndex])

            if scorepair > score:
                score = scorepair
                best_object = nextIndex

        if best_object != 0 and (index + 1) != len(frames):
            temp = frames[index+1]
            frames[index+1] = frames[best_object]
            frames[best_object] = temp

    return frames


# creates output file
def output(frames, filename):
    with open(filename, "w") as f:
        # write number of frames
        f.write(str(len(frames)) + "\n")
        # condition for 1_binary_landscapes
        if landscape_flag == 1:
            for frame in frames:
                # write only ID of landscape
                f.write(str(frame.pID)+" \n")
        # code block for all other input files
        else:
            for frame in frames:
                if isinstance(frame, list):
                    # single portrait frame conditional
                    if(len(frame) == 1):
                        single_portrait_frame = str(frame[0].pID)+" \n"
                        f.write(single_portrait_frame)
                    # frame with two portrait conditional
                    else:
                        portrait_frame = str(
                            frame[0].pID)+" "+str(frame[1].pID)+"\n"
                        f.write(portrait_frame)
                else:
                    # landscape conditional for mixed type exhibition
                    landscape_frame = str(frame.pID)+" \n"
                    f.write(landscape_frame)
    return 0


# returns minimum out of common tags, tags in P1 but not in P2 and its inverse
def local_robotic_satisfaction(P1, P2):
    P1T = get_tags(P1)
    P2T = get_tags(P2)
    common = len(list(set(P1T).intersection(P2T)))
    # tags in P1 but not in P2
    p1NI2 = len(list(set(P1T).difference(P2T)))
    # tags in P2 but not in P1
    p2NI1 = len(list(set(P2T).difference(P1T)))
    return min(common, p1NI2, p2NI1)


def get_tags(F):
    if isinstance(F, list):
        F1 = F[0]
        F2 = F[1]
        tagsF1 = set(F1.tags)
        tagsF2 = set(F2.tags)
        unionTags = tagsF1.union(tagsF2)
        return unionTags
    else:
        return F.tags

def main(file):
    # read contents of input file
    head, tail = ntpath.split(file)
    filename = tail or ntpath.basename(head)
    print("Processing", filename, "...")
    stream = read_and_group(file)
    sorted_tags = sort_by_number_of_tags(stream)
    arrangedPaintings = comparePaintings(sorted_tags)
    outputFile = "KCW_Team4_" + filename
    output(arrangedPaintings, outputFile)
