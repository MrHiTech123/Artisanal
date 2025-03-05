from typing import Any


def mod_loaded(mod: str) -> dict[str, str]:
    return {'type': 'forge:mod_loaded', 'modid': mod}


def mod_not_loaded(mod: str) -> dict[str, str]:
    return not_(mod_loaded(mod))


def not_(cond: dict[str, Any]) -> dict[str, Any]:
    return {'type': 'forge:not', 'value': cond}


def and_(cond1: dict[str, Any], cond2: dict[str, Any]) -> dict[str, Any]:
    return {'type': 'forge:and', 'values': [cond1, cond2]}


def or_(cond1: dict[str, Any], cond2: dict[str, Any]) -> dict[str, Any]:
    return {'type': 'forge:or', 'values': [cond1, cond2]}
