from pony import orm
from datetime import datetime

db = orm.Database()

EXP_TYPE_CODES = {
    "LIGHT": 0,
    "FLAT": 1,
    "DARK": 2,
    "BIAS": 3,
}


class NightBundle(db.Entity):
    telescope_night_build_id = orm.Required(int)
    datetime = orm.Required(datetime)
    directory_path = orm.Required(str)
    exposures = orm.Set("Exposure")


class Exposure(db.Entity):
    night_build = orm.Required(NightBundle)
    filename = orm.Required(str)
    exposure_type = orm.Required(int, size=8, default=EXP_TYPE_CODES["LIGHT"])
    # observation_date = orm.Required(datetime)
    naxis = orm.Optional(int)
    naxis1 = orm.Optional(int)
    naxis2 = orm.Optional(int)
    exptime = orm.Optional(float)
    stacks = orm.Set("ExposureCombination")


class ExposureCombination(db.Entity):
    combination_type = orm.Required(int, size=8, default=EXP_TYPE_CODES["DARK"])
    exposures = orm.Set("Exposure")
