# encoding: utf-8

from __future__ import absolute_import
import logging, platform

__all__ = ["ColorFormatter"]

class ColorFormatter(logging.Formatter):
    """
    .. TODO::
        
        * 支持 Windows 控制台
    """
    
    FORMAT = ("[%(asctime)s][$BOLD%(name)-20s$RESET][%(levelname)-18s]  "
              "%(message)s "
              "($BOLD%(filename)s$RESET:%(lineno)d)")

    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
    
    RESET_SEQ = "\033[0m"
    COLOR_SEQ = "\033[1;%dm"
    BOLD_SEQ = "\033[1m"
    
    COLORS = {
        'WARNING': YELLOW,
        'INFO': WHITE,
        'DEBUG': BLUE,
        'CRITICAL': YELLOW,
        'ERROR': RED
    }
    
    def formatter_msg(self, msg, use_color=True):
        if use_color:
            msg = msg.replace("$RESET", self.RESET_SEQ).replace("$BOLD", self.BOLD_SEQ)
        else:
            msg = msg.replace("$RESET", "").replace("$BOLD", "")
        return msg
    
    def __init__(self, fmt = None, datefmt = None):
        msg = self.formatter_msg(fmt or self.FORMAT, True)
        logging.Formatter.__init__(self, msg)
        if platform.system() != "Windows":
            self.use_color = True
        else:
            self.use_color = False
            
    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in self.COLORS:
            fore_color = 30 + self.COLORS[levelname]
            levelname_color = self.COLOR_SEQ % fore_color + levelname + self.RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)

