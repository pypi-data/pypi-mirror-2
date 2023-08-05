ui='submod.overweb'
import spam
import os
status = spam.system("cd" if os.name == 'nt' else "pwd")
ui=status

