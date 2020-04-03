# -*- coding: utf-8 -*-
"""
Preprocessor Module

(c) TOROS Dev Team
"""
import logging
from . import config
import xmlrpc.client
from pony import orm
from . import models
from .models import EXP_TYPE_CODES
from astropy.io import fits
import os


def front_desk(work_order):
    """Front Desk will receive your Work Order and perform the requested operations.
    Make sure all your services are running."""
    logger = logging.getLogger()
    logger.info("Work order received.")
    logger.debug("{}".format(work_order))
    for k, v in work_order.items():
        print("{}:\t{}".format(k, v))
    request_type = work_order.get("Request")
    if request_type is None:
        logger.error("Missing key: Request.")
        return
    if request_type == "Exposure Calibration":
        init_preprocessing(work_order)
        logger.info("Initiating exposure calibration request.")
    return "Work order received."


def serve():
    logger = logging.getLogger("preprocessor")
    logger.info("Started serving.")

    from xmlrpc.server import DocXMLRPCServer
    from xmlrpc.server import DocXMLRPCRequestHandler
    from . import config

    # A request handler that responds appropriately for CORS and preflight
    class CORSRequestHandler(DocXMLRPCRequestHandler):
        def do_OPTIONS(self):
            self.send_response(200)
            self.end_headers()

        # Add these headers to all responses
        def end_headers(self):
            self.send_header(
                "Access-Control-Allow-Headers",
                "Origin, X-Requested-With, Content-Type, Accept",
            )
            self.send_header("Access-Control-Allow-Origin", "*")
            super().end_headers()

    net_address = config.get_config_for_key("Preprocessor Address")
    server = DocXMLRPCServer(
        ("0.0.0.0", net_address.get("Port")), requestHandler=CORSRequestHandler
    )
    server.set_server_title("Preprocessor Service Docs")
    server.set_server_name("TOROS Preprocessor Service")
    server.set_server_documentation("The Preprocessor module reduces CCD exposures.")
    server.register_function(front_desk)
    server.serve_forever()


@orm.db_session
def load_night_bundle(url):
    from datetime import datetime

    nb = models.NightBundle(
        telescope_night_bundle_id=1,
        datetime=datetime.now(),
        directory_path=os.path.abspath(url),
    )
    fits_files = [os.path.join(url, f) for f in os.listdir(url) if ".fit" in f]

    for afile in fits_files:
        hdulist = fits.open(afile)
        head = hdulist[0].header
        t = models.Exposure(
            night_bundle=nb,
            filename=os.path.basename(afile),
            exposure_type=EXP_TYPE_CODES[head["IMAGETYP"].upper()],
            naxis=head["NAXIS"],
            naxis1=head["NAXIS1"],
            naxis2=head["NAXIS2"],
            exptime=head["EXPTIME"],
        )
        hdulist.close()


def init_preprocessing(work_order):
    # Assume it will start from scratch
    # This will be done for a specific `night_bundle_id` that uniquely identifies an observation night.
    from urllib.parse import urlparse

    logger = logging.getLogger("init_preprocessing")
    file_url = urlparse(work_order.get("File Location"))
    directory_path = file_url.path
    try:
        load_night_bundle(directory_path)
    except:
        logger.exception("Error loading night bundle.")
    try:
        make_dark_master()
    except:
        logger.exception("Error making dark master.")
    try:
        make_flat_master()
    except:
        logger.exception("Error making flat master.")
    try:
        make_flatdark_correction()
    except:
        logger.exception("Error doing flat-dark reduction.")


@orm.db_session
def make_dark_master():
    """ for each group of (filter, exptime) do:
    stack all dark exposures
    save fits to file
    add entry in database for each file (stack) generated"""
    import ccdproc

    nb = models.NightBundle.get(telescope_night_bundle_id=1)
    nb_dir = nb.directory_path
    dark_list_q = nb.exposures.select(
        lambda d: d.exposure_type == models.EXP_TYPE_CODES["DARK"]
    )
    dark_list = [os.path.join(nb_dir, f.filename) for f in dark_list_q]

    # Create dark master and save to file
    master_dark = ccdproc.combine(dark_list, method="median", unit="adu")
    dark_hdu = fits.PrimaryHDU(master_dark)
    dark_hdu.header["IMAGETYP"] = "DARKM"
    dark_hdu.header["EXPTIME"] = 60.0
    dark_hdu.writeto(os.path.join(nb_dir, "dark_master.fits"))

    # Add entry to database
    dark_comb = models.ExposureCombination(
        night_bundle=nb,
        filename="dark_master.fits",
        combination_type=models.COMB_TYPE_CODES["DARKM"],
        exposures=dark_list_q,
    )


@orm.db_session
def make_flat_master():
    """ for each filter do:
    stack all flat exposures
    save fits to file
    add entry in database for each file (stack) generated"""
    import ccdproc

    nb = models.NightBundle.get(telescope_night_bundle_id=1)
    nb_dir = nb.directory_path
    flat_list_q = nb.exposures.select(
        lambda d: d.exposure_type == models.EXP_TYPE_CODES["FLAT"]
    )
    flat_list = [os.path.join(nb_dir, f.filename) for f in flat_list_q]

    # Create dark master and save to file
    master_flat = ccdproc.combine(flat_list, method="average", unit="adu")
    flat_hdu = fits.PrimaryHDU(master_flat)
    flat_hdu.header["IMAGETYP"] = "FLATM"
    flat_hdu.header["EXPTIME"] = 60.0
    flat_hdu.writeto(os.path.join(nb_dir, "flat_master.fits"))

    # Add entry to database
    flat_comb = models.ExposureCombination(
        night_bundle=nb,
        filename="flat_master.fits",
        combination_type=models.COMB_TYPE_CODES["FLATM"],
        exposures=flat_list_q,
    )


@orm.db_session
def make_flatdark_correction():
    """ for each light exposure do:
    subtract dark from light
    divide by dark-subtracted flat
    save fits to file
    add entry in database for each calibrated file generated"""
    # Eventually should be done as described in:
    # https://ccdproc.readthedocs.io/en/latest/reduction_toolbox.html
    # Or here:
    # https://mwcraig.github.io/ccd-as-book
    import ccdproc
    from astropy.nddata import CCDData
    import astroscrappy
    import numpy as np
    from astropy import units as u

    nb = models.NightBundle.get(telescope_night_bundle_id=1)
    nb_dir = nb.directory_path
    light_list_q = nb.exposures.select(
        lambda d: d.exposure_type == models.EXP_TYPE_CODES["LIGHT"]
    )
    light_list = [os.path.join(nb_dir, f.filename) for f in light_list_q]

    master_dark_q = nb.combinations.select(
        lambda d: d.combination_type == models.COMB_TYPE_CODES["DARKM"]
    ).get()
    master_dark_path = os.path.join(nb_dir, master_dark_q.filename)
    master_flat_q = nb.combinations.select(
        lambda d: d.combination_type == models.COMB_TYPE_CODES["FLATM"]
    ).get()
    master_flat_path = os.path.join(nb_dir, master_flat_q.filename)

    for light_q, light_fname in zip(light_list_q, light_list):
        raw_data = CCDData.read(light_fname, unit="adu")
        master_dark = CCDData.read(master_dark_path, unit="adu")
        master_flat = CCDData.read(master_flat_path, unit="adu")
        # cr_cleaned = ccdproc.cosmicray_lacosmic(
        #     raw_data,
        #     satlevel=np.inf,
        #     sepmed=False,
        #     cleantype="medmask",
        #     fsmode="median",
        # )
        # crmask, cr_cleaned = astroscrappy.detect_cosmics(
        #     raw_data,
        #     inmask=None,
        #     satlevel=np.inf,
        #     sepmed=False,
        #     cleantype="medmask",
        #     fsmode="median",
        # )
        # cr_cleaned.unit = "adu"
        cr_cleaned = raw_data
        dark_subtracted = ccdproc.subtract_dark(
            cr_cleaned,
            master_dark,
            exposure_time="EXPTIME",
            exposure_unit=u.second,
            scale=True,
        )
        reduced_image = ccdproc.flat_correct(
            dark_subtracted, master_flat, min_value=0.9
        )
        reduced_filename = "calib_{}".format(os.path.basename(light_fname))
        reduced_path = os.path.join(nb_dir, reduced_filename)
        reduced_image.write(reduced_path, overwrite=True)
        reduced_comb = models.ExposureCombination(
            night_bundle=nb,
            filename=reduced_filename,
            combination_type=models.COMB_TYPE_CODES["CALIB_LIGHT"],
            exposures=light_q,
            uses_combinations=[master_flat_q, master_dark_q],
        )


if __name__ == "__main__":
    serve()
