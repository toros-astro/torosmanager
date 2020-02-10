# -*- coding: utf-8 -*-
"""
Preprocessor Module

(c) TOROS Dev Team
"""
import logging
from . import config
import xmlrpc.client


def front_desk(work_order):
    """Front Desk will receive your Work Order and perform the requested operations.
    Make sure all your services are running."""
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


if __name__ == "__main__":
    serve()
