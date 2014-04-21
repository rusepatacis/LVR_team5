__author__ = 'Jaka & Jani'
#coding UTF-8

from time import time


"""
Razred stoparica, namenjen merjenju cas izvajanja razlicnih delov programa.
Ukazi: intermediate(tag), start(tag),restart(tag),stop(tag).
Stoparica se avtomatsko aktivira, ko kreiramo objekt. Z uporabo "intermediate" lahko dodajamo vmesne case.
Tag se uporablja za oznacevanje dogodka, ce ga pustimo prazno se uporabi prednastavljena vrednost.

Case izpisemo z uporabo print(Stopwatch()).
"""
class Stopwatch():
    def __init__(self,name="Tags:"):
        self.timestamps = [time()]
        self.tags = ["Start"]
        self.name = name
        self.dx = len(name)+1

    def intermediate(self,tag=""):
        tag = str(tag)
        if len(self.timestamps) == 0:
            print "Error. Stopwatch not running. Starting it now."
            self.timestamps.append(time())

            if len(tag) == 0:
                self.tags = ["Start"]
            else:
                self.tags = [tag]
        else:
            self.timestamps.append(time())
            if len(tag) == 0:
                self.tags.append("Inter" + str(len(self.timestamps)-1))
            else:
                self.tags.append(tag)

    def start(self,tag=""):
        if len(self.timestamps > 1):
            print "Error. Stopwatch already running."
        else:
            self.timestamps.append(time())
            if len(tag) == 0:
                self.tags.append("Inter" + str(len(self.timestamps)-1))
            else:
                self.tags.append(tag)

    def restart(self,tag=""):
        self.timestamps = [time()]
        if len(tag) == 0:
            self.tags = ["Start"]
        else:
            self.tags = [tag]

    def clear(self):
        self.timestamps = []
        self.tags = []

    def stop(self,tag=""):
        self.timestamps.append(time())
        if len(tag) == 0:
            self.tags.append("Inter" + str(len(self.timestamps)-1))
        else:
            self.tags.append(tag)

    def __repr__(self):
        ind2 = max(self.dx,6)
        x = "Time:"+" "*(ind2-5) + "| "
        y = self.name + " "*(ind2 - len(self.name)) + "| "

        if len(self.timestamps) > 0:
            for t in range(0,len(self.timestamps)-2):
                #x += str(self.timestamps[t+1] - self.timestamps[t])+" "

                tmp = '%.3f ' % (self.timestamps[t+1] - self.timestamps[t])
                indent = max(len(tmp),len(self.tags[t+1]))+1

                x += tmp+" "*(abs(indent-len(tmp)))+"| "
                y += self.tags[t+1] + " "*abs(indent-len(self.tags[t+1]))+"| "

            y += "TOTAL"
            x += "%.3f" % (self.timestamps[len(self.timestamps)-1] - self.timestamps[0]) + " s"
            x += "\n --------------------------"
        else:
            x += "Stopwatch not started."
        y += "\n"
        return y+x