from pony import orm
from datetime import datetime

db = orm.Database()

EXP_TYPE_CODES = {
    "LIGHT": 0,
    "FLAT": 1,
    "DARK": 2,
    "BIAS": 3,
}

COMB_TYPE_CODES = {
    "CALIB_LIGHT": 0,
    "FLATM": 1,
    "DARKM": 2,
    "BIASM": 3,
    "STACK_LIGHT": 4,
}


class NightBundle(db.Entity):
    telescope_night_bundle_id = orm.Required(int)
    datetime = orm.Required(datetime)
    directory_path = orm.Required(str)
    exposures = orm.Set("Exposure")


class Exposure(db.Entity):
    night_bundle = orm.Required(NightBundle)
    filename = orm.Required(str)
    exposure_type = orm.Required(int, size=8)
    # observation_date = orm.Required(datetime)
    naxis = orm.Optional(int)
    naxis1 = orm.Optional(int)
    naxis2 = orm.Optional(int)
    exptime = orm.Optional(float)
    stacks = orm.Set("ExposureCombination")


class ExposureCombination(db.Entity):
    filename = orm.Required(str)
    combination_type = orm.Required(int, size=8)
    exposures = orm.Set("Exposure")
