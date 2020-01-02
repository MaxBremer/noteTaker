from datetime import datetime as dt
import os
import shutil
class Meeting:
    def __init__(self, title, initialNotes):
        self.title = title
        self.initialNotes = initialNotes
        self.startTime = dt.now()
        self.concluded = False
        self.noteSet = []
        self.tags = []

    def endMeeting(self):
        self.endTime = dt.now()
        #self.duration = self.endTime - self.startTime
        self.concluded = True
        
    def addNote(self, note):
        self.noteSet.append(note)

    def addTag(self, tag):
        self.tags.append(tag)

    def addTags(self):
        print("Add any tags you'd like to attach to this meeting one at a time, or enter \e to end.")
        inp = input()
        while not inp == "\e":
            if not "|" in inp:
                self.tags.append(inp)
                inp = input()
            else:
                print("'|' is a reserved character")
                inp = input()

        
    def __str__(self):
        output = "_______________________\n" + self.title + "\n_______________________\n"
        if len(self.initialNotes) > 0:
            output = output + "\nInitial note: " + self.initialNotes + "\n\n"
        if len(self.tags) > 0:
            tagStr = "Note is tagged as follows: "
            for t in self.tags:
                tagStr += "'" + t + "', "
            #NOTE ODD ERROR: if the following is - 1, the comma appears on a new line.
            #No idea why.
            output += tagStr[:len(tagStr)-2] + "\n\n"
        for n in self.noteSet:
            output = output + "o " + n + "\n"
        return output
        

def runNewMeeting():
    print("Meeting name/title?")
    mName = input()
    print("Enter any initial notes, e.g. notes on topic, relevance, etc.")
    mNo = input()
    curMeet = Meeting(mName, mNo)
    curMeet.addTags()
    print("Enter bullet points one at a time, or '\q' to quit")
    uinput = input()
    while not uinput == "\q":
        curMeet.addNote(uinput + "\n")
        #print("Enter a bullet point, or '\q' to quit")
        uinput = input()
    curMeet.endMeeting()
    return curMeet

def saveMeeting(m):
    if m in os.listdir("saves"):
        print("OVERWRITE")
    file = open(os.path.join("saves", m.title.strip() + ".txt"), "w+")
    file.write(m.title + "|||" + m.initialNotes + "\n")
    tagStr = ""
    for t in m.tags:
        tagStr = tagStr + "|" + t
    tagStr = tagStr[1:]
    file.write(tagStr + "\n")
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
    tags = lines[1].split("|")
    for t in tags:
        m.addTag(t)
    for i in range(2, len(lines)):
        m.addNote(lines[i])
    return m

def loadAllMeetings(saveDir):
    if not os.path.exists(saveDir):
        print("ERROR: nothing saved in " + saveDir + " yet")
        return []
    meetings = []
    for filename in os.listdir(saveDir):
        fileNP = os.path.join(saveDir, filename)
        meetings.append(loadMeeting(fileNP))
    return meetings

def resetMeetings():
    if not os.path.exists("saves"):
        print("saves folder not yet created, nothing to remove.")
        return
    for filename in os.listdir("saves"):
        os.remove(os.path.join("saves", filename))

def listInput(startMessage, quitCommand):
    print(startMessage)
    print("Quit with " + quitCommand)
    inp = input()
    items = []
    while not inp == quitCommand:
        items.append(inp)
        inp = input()
    return items

def main():
    inp = "q"
    while inp == "q":
        print("\n_______________________\nWELCOME TO MAX'S NOTES ORGANIZER INC\n_______________________\n")
        print("loading saved meetings...")
        if not os.path.exists("saves"):
            os.mkdir("saves")
        ms = loadAllMeetings("saves")
        newMs = []
        print("Welcome Max. \n(m)ake a new note,  (r)eference old ones, or (q)uit?\nWARNING: (t) to reset all notes.")
        inp = input()
        if inp=="m":
            meet = runNewMeeting()
            newMs.append(meet)
            print("(a)nother note or (q)uit to menu?")
            inp = input()
            while inp=="a":
                meet = runNewMeeting()
                newMs.append(meet)
                print("(a)nother note or (q)uit to menu?")
                inp = input()
            saveMeetings(newMs)
        elif inp=="r":
            while inp=="r":
                saves = os.listdir("saves")
                i = 0
                print("View by (t)ag or view (a)ll?")
                inpt = input()
                if inpt == "a":
                    print("Which note would you like to reference?")
                    for s in saves:
                        print(str(i) + ": " + s)
                        i += 1
                    choice = int(input())
                    if not choice in range(len(saves)):
                        print("ERROR: Invalid File Choice")
                        return
                    print(loadMeeting(os.path.join("saves", saves[choice])))
                elif inpt == "t":
                    print("Require (a)ll entered tags or an(y)?")
                    logic = input()
                    tags = listInput("Enter tags in question.", "\e")
                    applicable = []
                    if logic == "a":
                        for s in saves:
                            m = loadMeeting(os.path.join("saves", s))
                            acceptable = True
                            for t in tags:
                                if not t in m.tags:
                                    acceptable = False
                                    break
                            if acceptable:
                                applicable.append(m)
                    elif logic == "y":
                        for s in saves:
                            m = loadMeeting(os.path.join("saves", s))
                            acceptable = False
                            for t in tags:
                                if t in m.tags:
                                    acceptable = True
                                    break
                            if acceptable:
                                applicable.append(m)
                    if len(applicable) < 1:
                        print("No applicable notes found for those tags.")
                    else:
                        inp = "a"
                        while inp == "a":
                            print("The following notes were found: ")
                            for m in applicable:
                                print(str(applicable.index(m)) + ": " + m.title)
                            print("Select one to explore by its index, or enter anything else to quit out.")
                            temp = input()
                            if int(temp) in range(len(applicable)):
                                print(applicable[int(temp)])
                                print("(a)nother note of this set or (q)uit to menu?")
                                inp = input()
                            else:
                                inp = "q"
                            
                            
                        
                    
                print("(r)eference another or (q)uit to menu?")
                inp = input()
        elif inp=="t":
            print("Are you sure you want to delete all notes? y/n")
            if input() == "y":
                resetMeetings()
                print("Notes have been reset.")
        elif inp=="lt":
            print("DEBUG COMAND: loading and saving basic test notes.")
            testNotes = loadAllMeetings("tests")
            saveMeetings(testNotes)
            print("Successful.")
            print("(q)uit to menu?")
            inp = input()   
        elif inp=="q":
            return
        
if __name__ == "__main__":
    main()
        
    
