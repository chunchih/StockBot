from tkTool import TX00Window
from connectCapitalAPI import loginCapitalAccount

if __name__ == '__main__':    
    loginCapitalAccount()
    root = TX00Window()
    root.mainloop()