from tkinter import *
from connectCapitalAPI import requestKL, runTX00

class EntryWithPlaceholder(Entry):
    def __init__(self, master, placeholder, textvariable, color='grey'):
        super(EntryWithPlaceholder, self).__init__(master, textvariable=textvariable)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)
        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

todayString = None
def recordWindow():
    global todayString
    root = Tk()
    root.title('紀錄當天股票')
    root.geometry('300x30')  

    todayDateLabel = Label(root, text = "Today Date")
    todayString = StringVar()
    todayEntry = EntryWithPlaceholder(root, '2000-01-01', textvariable=todayString)
    resultButton = Button(root, text = u"送出", command= lambda: requestKL(todayString))

    todayDateLabel.grid(column=0, row=0, sticky=W)
    todayEntry.grid(column=1, row=0, padx=10)
    resultButton.grid(column=2, row=0, sticky=W)
    return root

def TX00Window():
    root = Tk()
    root.title('策略預估')
    root.geometry('300x50')  

    todayDateLabel = Label(root, text = "Today Date")
    todayString = StringVar()
    todayEntry = EntryWithPlaceholder(root, '2019-08-03', textvariable=todayString)

    resultButton = Button(root, text = u"開始", command= lambda: runTX00(todayString), width=5)

    todayDateLabel.grid(column=0, row=1, sticky=W)
    todayEntry.grid(column=1, row=1, padx=10)
    resultButton.grid(column=2, row=1, sticky=W)

    return root

