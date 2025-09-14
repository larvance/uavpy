from src.uavpy import mavlink
from src.uavpy.utils.log import debug


def handle_link_node_status(self: "mavlink.Mavlink", msg):
    self.since_boot = msg.timestamp / 1e3
    self.link_status.transmit_buffer = msg.tx_buf / 1e2
    self.link_status.receive_buffer = msg.rx_buf / 1e2
    self.link_status.transmit_speed = msg.tx_rate
    self.link_status.receive_speed = msg.rx_rate
    self.link_status.received_invalid = msg.rx_parse_err
    self.link_status.transmit_overflows = msg.tx_overflows
    self.link_status.receive_overflows = msg.rx_overflows
    self.link_status.messages_sent = msg.messages_sent
    self.link_status.messages_received = msg.messages_received
    self.link_status.messages_lost = msg.messages_lost
    debug(f"Link status: {self.link_status}")
