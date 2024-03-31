import logging
import sys
from typing import Any, List, Optional


# check min. python version
if sys.version_info < (3, 9):  # pragma: no cover
    sys.exit("sonworld requires Python version >= 3.9")

from sonworld import __version__

from sonworld.exceptions import SonWorldException, OperationalException
from sonworld.utils.gc_setup import gc_set_threshold
from sonworld.commands import Arguments
from sonworld.loggers import setup_logging_pre


logger = logging.getLogger('sonworld')


def main(sysargv: Optional[List[str]] = None) -> None:
    """
    This function will initiate the bot and start the trading loop.
    :return: None
    """

    return_code: Any = 1
    try:
        setup_logging_pre()
        arguments = Arguments(sysargv)
        args = arguments.get_parsed_arg()

        # Call subcommand.
        if 'func' in args:
            logger.info(f'sonworld {__version__}')
            gc_set_threshold()
            return_code = args['func'](args)
        else:
            # No subcommand was issued.
            raise OperationalException(
                "Usage of sonworld requires a subcommand to be specified.\n"
                "To see the full list of options available, please use "
                "`sonworld --help` or `sonworld <command> --help`."
            )

    except SystemExit as e:  # pragma: no cover
        return_code = e
    except KeyboardInterrupt:
        logger.info('SIGINT received, aborting ...')
        return_code = 0
    except SonWorldException as e:
        logger.error(str(e))
        return_code = 2
    except Exception:
        logger.exception('Fatal exception!')
    finally:
        sys.exit(return_code)


if __name__ == '__main__':  # pragma: no cover
    main()