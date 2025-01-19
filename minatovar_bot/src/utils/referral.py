from ctypes import Union
import logging


def pars_arg(mes: str) -> Union[str]:
    mes_split = mes.split()
    logging.info(mes_split)
    return mes_split[-1] if len(mes_split) > 1 else None
