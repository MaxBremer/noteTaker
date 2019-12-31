from datetime import datetime as dt
import os
class Meeting:
    def __init__(self, title, initialNotes):
        self.title = title
        self.initialNotes = initialNotes
        self.startTime = dt.now()
        self.concluded = False
        self.noteSet = []

    def endMeeting(self):
        self.endTime = dt.now()
        #self.duration = self.endTime - self.startTime
        self.concluded = True
        
    def addNote(self, note):
        self.noteSet.append(note)
        
    def __str__(self):
        output = "_______________________\n" + self.title + "\n_______________________\n"
        if len(self.initialNotes) > 0:
            output = output + "\nInitial note: " + self.initialNotes + "\n\n"
        for n in self.noteSet:
            output = output + "o " + n + "\n"
        return output
        

def runNewMeeting():
    print("Meeting name/title?")
    mName = input()
    print("Enter any initial notes, e.g. notes on topic, relevance, etc.")
    mNo = input()
    curMeet = Meeting(mName, mNo)
    print("Enter bullet points one at a time, or '\q' to quit")
    uinput = input()
    while not uinput == "\q":
        curMeet.addNote(uinput + "\n")
        #print("Enter a bullet point, or '\q' to quit")
        uinput = input()
    curMeet.endMeeting()
    return curMeet

def saveMeeting(m):
    if not os.path.exists("saves"):
        os.mkdir("saves")
    if m in os.listdir("saves"):
        print("OVERWRITE")
    file = open(os.path.join("saves", m.title.strip() + ".txt"), "w+")
    file.write(m.title + "|||" + m.initialNotes + "\n")
    for n in m.noteSet:
        file.write(n)
    file.close()

def saveMeetings(meetingList):
    for m in meetingList:
        saveMeeting(m)

def loadMeeting(fileNP):
    file = open(fileNP, "r")
    lines = file.readlines()
    indexing = lines[0].split("|||")
    m = Meeting(indexing[0], indexing[1])
    for i in range(1, len(lines)):
        m.addNote(lines[i])
    return m

def loadAllMeetings():
    if not os.path.exists("saves"):
        print("ERROR: nothing saved yet")
        return []
    meetings = []
    for filename in os.listdir("saves"):
        fileNP = os.path.join("saves", filename)
        meetings.append(loadMeeting(fileNP))
    return meetings

def main():
    print("WELCOME TO DUMBASS MEETING ORGANIZER INC")
    print("loading saved meetings...")
    ms = loadAllMeetings()
    newMs = []
    print("Welcome dumbass. (m)ake a new meeting or (r)eference old ones?")
    inp = input()
    if inp=="m":
        meet = runNewMeeting()
        newMs.append(meet)
        print("(a)nother meeting or (q)uit?")
        inp = input()
        while inp=="a":
            meet = runNewMeeting()
            newMs.append(meet)
            print("(a)nother meeting or (q)uit?")
            inp = input()
        saveMeetings(newMs)
    elif inp=="r":
        saves = os.listdir("saves")
        i = 0
        print("Which meeting would you like to reference?")
        for s in saves:
            print(str(i) + ": " + s)
            i += 1
        choice = int(input())
        if not choice in range(len(saves)):
            print("ERROR: Invalid File Choice")
            return
        print(loadMeeting(os.path.join("saves", saves[choice])))
        print("(r)eference another or (q)uit?")
        uinput = input()
        if input=="r":
            print("NOT BUILT YET")
        
if __name__ == "__main__":
    main()
        
    
