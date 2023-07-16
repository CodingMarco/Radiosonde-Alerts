class BBox:
    def __init__(self, west, south, east, north, name="BBox"):
        self.west = west
        self.south = south
        self.east = east
        self.north = north
        self.name = name

    
    def is_inside(self, lat, lon):
        return self.west <= lon <= self.east and self.south <= lat <= self.north
