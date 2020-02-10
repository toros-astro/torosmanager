from pony import orm
from datetime import datetime

db = orm.Database()

EXP_TYPE_CODES = {
    "LIGHT": 0,
    "FLAT": 1,
    "DARK": 2,
    "BIAS": 3,
}


class Exposure(db.Entity):
    exposure_type = orm.Required(int, size=8, default=EXP_TYPE_CODES["LIGHT"])
    observation_date = orm.Required(datetime)
    naxis = orm.Optional(int)
    naxis1 = orm.Optional(int)
    naxis2 = orm.Optional(int)
    bscale = orm.Optional(float)
    bzero = orm.Optional(float)
    gain = orm.Optional(float)
    exptime = orm.Optional(float)
