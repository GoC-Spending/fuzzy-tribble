import logging
from tqdm import tqdm
from io import IOBase
import sys

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(name)s: %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S%z')


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger

LOGGER = get_logger(__name__)



class tqdmLog(tqdm):

    class PreserveLastOutputStreamInterceptor():
        def __init__(self,outputStream : IOBase,lastOutputInitialValue: str = "(no output yet)"):
            self.outputStream = outputStream
            if hasattr(outputStream,'encoding'):
                self.encoding = outputStream.encoding
            self.lastOutput = lastOutputInitialValue
        def write(self,st):
            if len(st) > 3:   # we want the last sentence (avoids storing of formatting output like '\n')
                self.lastOutput = st
                self.outputStream.write(st)
            else:
                sys.stderr.write('\r')
        def flush(self):
            self.outputStream.flush()


    def __init__(self,*args,**kwargs):
        if not 'file' in kwargs:
            kwargs['file'] = tqdmLog.PreserveLastOutputStreamInterceptor(sys.stderr)
        super(tqdm,self).__init__(*args,**kwargs)
    def __iter__(self,*args,**kwargs):
        iterable = super(tqdm,self).__iter__(*args,**kwargs)
        def it():
            try:
                for i in iterable:
                    yield i
            finally:
                LOGGER.info(self.fp.lastOutput[1:])
        return it()
    @classmethod
    def pandas(tclass,*targs,**tkwargs):

        if 'file' in tkwargs:
            super(tqdm,tclass).pandas(*targs,**tkwargs)
        else:
            tkwargs['file']=tqdmLog.PreserveLastOutputStreamInterceptor(sys.stderr)
 
            from pandas.core.frame import DataFrame
            from pandas.core.series import Series
            from pandas.core.groupby import DataFrameGroupBy
            from pandas.core.groupby import SeriesGroupBy
            from pandas.core.groupby import GroupBy
            from pandas.core.groupby import PanelGroupBy
            from pandas import Panel

            super(tqdm,tclass).pandas(*targs,**tkwargs)
            def wrap_progress_apply(original_progress_apply):
                def progress_apply(df, func, *args, **kwargs):
                    try:
                        res = original_progress_apply(df, func, *args, **kwargs)
                    finally:
                        LOGGER.info(tkwargs['file'].lastOutput[1:])
                    return res
                return progress_apply

            for dt in [DataFrame, Series, DataFrameGroupBy, SeriesGroupBy, GroupBy, PanelGroupBy, Panel]:
                dt.progress_apply = wrap_progress_apply(dt.progress_apply)
        

tqdm = tqdmLog

