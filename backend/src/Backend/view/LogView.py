import FixRaidenBoss2 as FRB

from .BaseView import BaseView


class LogView(FRB.Logger, BaseView):
    def __init__(self, prefix: str = "", logTxt: bool = False, verbose: bool = True):
        FRB.Logger.__init__(self, prefix = prefix, logTxt = logTxt, verbose = verbose)

    def print(self, txt: str, *args, prefix: str = "", **kwargs):
        oldIncludePrefix = self.includePrefix
        self.includePrefix = prefix != ""
        
        if (self.includePrefix):
            self.prefix = prefix

        #self.log(txt, *args, **kwargs)

        if (self.includePrefix != oldIncludePrefix):
            self.includePrefix = oldIncludePrefix