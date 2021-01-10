import math
import curses
class progressClassic:
    def __init__(self, title, total = 0):
        self.title = title
        self.total = total
        self.progress = 0
    
    def updateProgress(self, progress):
        self.progress = progress
        return self.progress

    def addProgress(self, add):
        self.progress += (add, self.total-self.progress)[self.progress+add > self.total]
        self.progress += (add, -self.progress)[self.progress+add < 0]
        return self.progress

    def updateTotal(self, total):
        self.total = total
        return self.total

    def draw(self, window, width, ystart=0, xstart=0):
        percent = math.floor((self.progress/self.total)*100)
        strbeg = self.title + " ["
        strmid = ""
        strend = "] " + str(percent) + "% | " + str(self.progress) + "/" + str(self.total) + " "
        w = len(strbeg)+len(strend)
        barlen = width - w
        fill = barlen * (percent/100)
        fill = math.floor(fill)
        for i in range(0, barlen):
            ch = (".", "#")[i<fill]
            strmid += ch
        string = strbeg+strmid+strend
        window.addstr(ystart, xstart, string)

class progressClassicColor(progressClassic):
    def __init__(self, title, total = 0, colors = (1, 2, 3)):
        super().__init__(title, total)
        self.colors = colors
    def draw(self, window, width, ystart=0, xstart=0):
        percent = math.floor((self.progress/self.total)*100)
        strbeg = self.title + " ["
        strend = "] " + str(percent) + "% | " + str(self.progress) + "/" + str(self.total) + " "
        w = len(strbeg)+len(strend)
        barlen = width - w
        fill = barlen * (percent/100)
        fill = math.floor(fill)
        window.addstr(ystart, xstart, strbeg)
        for i in range(0, barlen):
            if(i < fill):
                if(i/barlen < .33):
                    window.addstr('#', curses.color_pair(1))
                elif(i/barlen < .66):
                    window.addstr('#', curses.color_pair(2))
                else:
                    window.addstr('#', curses.color_pair(3))
            else:
                window.addstr('.', curses.color_pair(0))
        window.addstr(strend, curses.color_pair(0))

class progressChasing(progressClassic):
    def __init__(self, title, total = 0):
        super().__init__(title, total)

    def draw(self, window, width, ystart=0, xstart=0):
        percent = math.floor((self.progress/self.total)*100)
        strbeg = self.title + " | " + str(self.progress) + "/" + str(self.total) + " ["
        strend = "] "
        w = len(strbeg)+len(strend)
        barlen = width - w
        pos = barlen * (percent/100)
        pos = math.floor(pos)
        pos = (1, pos)[pos != 0]
        pos = (barlen - 2, pos)[pos < barlen]
        window.addstr(ystart, xstart, strbeg)
        for i in range(0, barlen):
            if(i == pos-1):
                window.addstr('<')
            elif(i == pos):
                window.addstr('=')
            elif(i == pos+1):
                window.addstr('>')
            else:
                window.addstr(' ')
        window.addstr(strend)