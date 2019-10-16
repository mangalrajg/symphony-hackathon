from mybot2.python.listeners.simple_message_processor import FlagDealsProcessor
from .elements_listener import ElementsActionListener
import logging
import config
import time
# A sample implementation of Abstract imListener class
# The listener can respond to incoming events if the respective event
# handler has been implemented

class ElementsListenerTestImp(ElementsActionListener):
    """Example implementation of ElementsActionListener

        sym_bot_client: contains clients which respond to incoming events

    """
    global_stream_id = ""

    def __init__(self, sym_bot_client):
        self.bot_client = sym_bot_client

    def on_elements_action(self, action):
        logging.debug('element submitted :')
        logging.debug(action)
        form_values = action["payload"]["symphonyElementsAction"]["formValues"]
        if form_values["action"] == "update-button":
            msg_to_send = dict(
                message='<messageML><h2>Updating prices for OJX20</h2></messageML>'
            )
            stream_id=config.global_stream_id
            self.bot_client.get_message_client(). \
                send_msg(stream_id,  msg_to_send)
            time.sleep(5)
            msg_to_send2 = dict(
                message="""<messageML>Update Successful. Starting NAV Process in 10 minutes
                <form id="hold_id"><button name="hold-button" type="action">Hold</button></form></messageML>"""
            )
            self.bot_client.get_message_client(). \
                send_msg(stream_id,  msg_to_send2)
        elif form_values["action"] == "hold-button":
            msg_to_send = dict(
                message='<messageML>Holding NAV</messageML>'
            )
            stream_id = config.global_stream_id
            self.bot_client.get_message_client(). \
                send_msg(stream_id, msg_to_send)
        #self.bot_client.get_message_client(). \
        #    send_msg(action_stream_id,  msg_to_send)

