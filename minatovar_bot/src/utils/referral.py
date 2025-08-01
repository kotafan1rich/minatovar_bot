from typing import Optional


def pars_arg(mes: str) -> Optional[str]:
    mes_split = mes.split()
    return mes_split[-1] if len(mes_split) > 1 else None
