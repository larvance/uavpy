from src.uavpy import mavlink


def handle_home_position(self: "mavlink.Mavlink", msg):
    t = msg.time_usec / 1e6
    if t > 1.7e9:
        self.time_unix = t
    else:
        self.since_boot = t
    self.home.lat = msg.latitude / 1e7
    self.home.lon = msg.longitude / 1e7
    self.home.alt = msg.altitude / 1e3
    self.home.north = msg.x
    self.home.east = msg.y
    self.home.up = -msg.z
    # ignoring .q for now.
    self.home.approach.north = msg.approach_x
    self.home.approach.east = msg.approach_y
    self.home.approach.up = -msg.approach_z
