from papermill.engines import Engine
from papermill.utils import merge_kwargs, remove_args
from papermill.log import logger

from ploomber_engine.client import PapermillPloomberNotebookClient


class DebugEngine(Engine):
    """An engine that starts a debugging session once the notebook fails
    """

    @classmethod
    def execute_managed_notebook(
        cls,
        nb_man,
        kernel_name,
        log_output=False,
        stdout_file=None,
        stderr_file=None,
        start_timeout=60,
        execution_timeout=None,
        **kwargs,
    ):
        # Exclude parameters that named differently downstream
        safe_kwargs = remove_args(['timeout', 'startup_timeout'], **kwargs)

        # Nicely handle preprocessor arguments prioritizing values set by
        # engine
        final_kwargs = merge_kwargs(
            safe_kwargs,
            timeout=execution_timeout
            if execution_timeout else kwargs.get('timeout'),
            startup_timeout=start_timeout,
            kernel_name=kernel_name,
            log=logger,
            log_output=log_output,
            stdout_file=stdout_file,
            stderr_file=stderr_file,
        )

        #  use our Papermill client
        return PapermillPloomberNotebookClient(nb_man,
                                               **final_kwargs).execute()


class DebugLaterEngine(Engine):
    """An engine that stores the traceback object for later debugging
    """

    @classmethod
    def execute_managed_notebook(
        cls,
        nb_man,
        kernel_name,
        log_output=False,
        stdout_file=None,
        stderr_file=None,
        start_timeout=60,
        execution_timeout=None,
        **kwargs,
    ):
        # Exclude parameters that named differently downstream
        safe_kwargs = remove_args(['timeout', 'startup_timeout'], **kwargs)

        # Nicely handle preprocessor arguments prioritizing values set by engine
        final_kwargs = merge_kwargs(
            safe_kwargs,
            timeout=execution_timeout
            if execution_timeout else kwargs.get('timeout'),
            startup_timeout=start_timeout,
            kernel_name=kernel_name,
            log=logger,
            log_output=log_output,
            stdout_file=stdout_file,
            stderr_file=stderr_file,
        )
        return PapermillNotebookClient(nb_man, **final_kwargs).execute()
