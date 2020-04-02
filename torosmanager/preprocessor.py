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
    wotype = work_order.get("WOType")
    if wotype is None:
        logger.error("Missing key: WOType.")
        return
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


def init_preprocessing(url):
    # Assume it will start from scratch
    # This will be done for a specific `night_bundle_id` that uniquely identifies an observation night.
    load_night_bundle(url)
    make_dark_master()
    make_flat_master()
    make_flatdark_correction()


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
    dark_hdu.header["IMAGETYP"] = "DARK_M"
    dark_hdu.header["EXPTIME"] = 60.0
    dark_hdu.writeto(os.path.join(nb_dir, "dark_master.fits"))

    # Add entry to database
    dark_comb = models.ExposureCombination(
        filename="dark_master.fits",
        combination_type=models.COMB_TYPE_CODES["DARKM"],
        exposures=dark_list_q,
    )


if __name__ == "__main__":
    serve()
