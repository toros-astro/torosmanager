# -*- coding: utf-8 -*-
"""
Preprocessor Module

(c) TOROS Dev Team
"""
import logging
from . import config
import xmlrpc.client
from pony import orm


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
def load_night_build(url):
    from . import models
    from .models import EXP_TYPE_CODES
    from datetime import datetime
    import os
    from astropy.io import fits
    nb = models.NightBuild(datetime=datetime.now(), directory_path=url)
    fits_files = [f for f in os.listdir(url) if ".fit" in f]

    for afile in fits_files:
        hdulist = fits.open(afile)
        head = hdulist[0].header
        t = models.Exposure(
            night_build=nb,
            filename=os.path.basename(afile),
            exposure_type=EXP_TYPE_CODES[head["IMAGETYP"]],
            naxis=head["NAXIS"],
            naxis1=head["NAXIS1"],
            naxis2=head["NAXIS2"],
            exptime=head["EXPTIME"],
        )


if __name__ == "__main__":
    serve()
