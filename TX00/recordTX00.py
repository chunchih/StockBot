from connectCapitalAPI import loginCapitalAccount
from tkTool import recordWindow

if __name__ == '__main__':
    loginCapitalAccount()
    root = recordWindow()
    root.mainloop()