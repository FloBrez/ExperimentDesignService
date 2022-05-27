def calc_affordable_principle(zins_bps: int, annuitaet_mtl_eur: float, laufzeit_monate: int) -> float:
    r = zins_bps / 100 / 100 / 12.0
    return annuitaet_mtl_eur / (r * (1+r)**laufzeit_monate / ((1+r)**laufzeit_monate-1))

# calc_affordable_principle(interest_rate=0.02, annuity=982., periods=12*30)
# calc_affordable_principle(zins_bps=200, annuitaet_mtl_eur=982., laufzeit_monate=12*30)