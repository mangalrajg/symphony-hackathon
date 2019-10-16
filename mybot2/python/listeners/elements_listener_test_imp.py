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
        #form_stream_id=action["payload"]["symphonyElementsAction"]["formStream"]["streamId"]
        #action_stream_id=action["payload"]["symphonyElementsAction"]["actionStream"]["streamId"]
        form_values = action["payload"]["symphonyElementsAction"]["formValues"]
        if form_values["action"] == "select-options":
            selected_deals = []
            for entry in form_values :
                if(entry.startswith("tables") and form_values[entry] == "on"):
                    selected_deals.append(entry[13:])

                logging.debug('entry' + entry)


            msg_to_send = dict(
                message='<messageML>Flagging trades #{} to be removed from DUT</messageML>'.format(', #'.join(selected_deals))
            )
            stream_id=config.global_stream_id
            self.bot_client.get_message_client(). \
                send_msg(stream_id,  msg_to_send)
            time.sleep(5)
            msg_to_send2 = dict(
                message="""<messageML>Deals flagging successful. Starting NAV Process in 10 minutes
                <form id="hold_id"><button name="hold-button" type="action">Hold</button></form></messageML>"""
            )
            self.bot_client.get_message_client(). \
                send_msg(stream_id,  msg_to_send2)
        elif form_values["action"] == "hold-button":
            msg_to_send = dict(
                message='<messageML><p>Holding NAV</p></messageML>'
            )
            stream_id = config.global_stream_id
            self.bot_client.get_message_client(). \
                send_msg(stream_id, msg_to_send)
        #self.bot_client.get_message_client(). \
        #    send_msg(action_stream_id,  msg_to_send)

