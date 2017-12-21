import logging
import sys
import types
from typing import Union, Any, Callable
from tqdm import tqdm

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(name)s: %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S%z')


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger

LOGGER = get_logger(__name__)



class TqdmLog(tqdm):

    class PreserveLastOutputStreamInterceptor():
        def __init__(self, output_stream: Any, last_output_initial_value: str = "(no output yet)") -> None:
            self.output_stream = output_stream
            if hasattr(output_stream, 'encoding'):
                self.encoding = output_stream.encoding
            self.last_output = last_output_initial_value
        def write(self, string: str) -> None:
            if string != '\n' and string != '':   # don't store or print the end of line after the last iteration
                self.last_output = string
                self.output_stream.write(string)
            else:
                # get rid of the status bar line so that it is
                # effectively replaced by the log of the last output
                self.output_stream.write('\r')
        def flush(self) -> None:
            self.output_stream.flush()


    def __init__(self, *args, **kwargs) -> None:
        if 'file' not in kwargs:
            kwargs['file'] = TqdmLog.PreserveLastOutputStreamInterceptor(sys.stderr)
        super(tqdm, self).__init__(*args, **kwargs)
    def __iter__(self) -> types.GeneratorType:
        iterable = super(tqdm, self).__iter__()
        def iter_logging_wrapper():
            count = 0
            item = None
            try:
                for count, item in enumerate(iterable):
                    yield item
            finally:
                if self.n != count + 1:
                    print('')  # kinda dirty but ensures that the next log line is not appended to the last output line
                    LOGGER.info(f'failed on item: {item}')
                    self.n = count
                self.refresh()
                LOGGER.info(self.fp.last_output[1:])
        return iter_logging_wrapper()
    @classmethod
    def pandas(tclass: type, *targs, **tkwargs) -> None: # pylint: disable=C0202
                                                         # adhering to tqdm's definition
        if 'file' in tkwargs:
            super(tqdm, tclass).pandas(*targs, **tkwargs)
        else:
            tkwargs['file']=TqdmLog.PreserveLastOutputStreamInterceptor(sys.stderr)

            from pandas.core.frame import DataFrame
            from pandas.core.series import Series
            from pandas.core.groupby import DataFrameGroupBy
            from pandas.core.groupby import SeriesGroupBy
            from pandas.core.groupby import GroupBy
            from pandas.core.groupby import PanelGroupBy
            from pandas import Panel

            tqdm.pandas(tclass, *targs, **tkwargs)
            def wrap_progress_apply(original_progress_apply) -> Callable[[Any, Callable, Any, Any], Any]:
                def progress_apply(df: Union[DataFrame, Series, DataFrameGroupBy,
                                             SeriesGroupBy, GroupBy, PanelGroupBy, Panel],
                                   func: Callable, *args, **kwargs
                                  ) -> Union[DataFrame, Series, DataFrameGroupBy,
                                             SeriesGroupBy, GroupBy, PanelGroupBy, Panel]:
                    # error handling in progress_apply is difficult because
                    # the instance of the tqdm object only exists within
                    # the tqdm progress_apply classmethod
                    # we can still keep track of the invocations by wrapping
                    # the apply function but we won't be able to produce an
                    # updated version of the status bar in the case of
                    # failure because at that point the tqdm object
                    # does not exist anymore (this can only be changed
                    # inside the tqdm code itself which we leave untouched)

                    count = 1
                    def counter_wrapped_func(item, *args, **kwargs):
                        nonlocal count
                        try:
                            res = func(item, *args, **kwargs)
                        except Exception: # pylint: disable=W0703
                                          # needs to be general
                            print('')  # kinda dirty but ensures that the next log line 
                                       # is not appended to the last output line
                            LOGGER.info(f'Failed on pandas apply during the {count}. invocation of the ' +
                                        f'provided apply function processing item: \n{item}')
                        count+=1
                        return res

                    progress_apply_res = original_progress_apply(df, counter_wrapped_func, *args, **kwargs)
                    LOGGER.info(tkwargs['file'].last_output[1:])
                    return progress_apply_res
                return progress_apply

            for datatype in [DataFrame, Series, DataFrameGroupBy, SeriesGroupBy, GroupBy, PanelGroupBy, Panel]:
                datatype.progress_apply = wrap_progress_apply(datatype.progress_apply)


tqdm = TqdmLog # pylint: disable=C0103
               # we want users to be able to use logging.tqdm just like tqdm.tqdm
