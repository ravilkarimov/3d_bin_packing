class Box:
    def __init__(
        self,
        width: int,
        height: int,
        length: int,
        x=0,
        y=0,
        z=0,
    ):
        self.width = width
        self.height = height
        self.length = length
        self.x = x
        self.y = y
        self.z = z

    def get_dimensions(self) -> tuple[int, int, int]:
        return self.width, self.height, self.length

    def get_x_vertices(self) -> list[int]:
        return [
            self.x, self.x,
            self.x + self.width, self.x + self.width,
            self.x, self.x,
            self.x + self.width, self.x + self.width
        ]

    def get_y_vertices(self) -> list[int]:
        return [
            self.y, self.y + self.height,
            self.y + self.height, self.y,
            self.y, self.y + self.height,
            self.y + self.height, self.y
        ]

    def get_z_vertices(self) -> list[int]:
        return [
            self.z, self.z,
            self.z, self.z,
            self.z + self.length, self.z + self.length,
            self.z + self.length, self.z + self.length
        ]

    def set_position(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        s = "[(width, height, length), (x, y, z)]:"
        return s + " [(%s, %s, %s), (%s, %s, %s)]" % (
            self.width, self.height, self.length,
            self.x, self.y, self.z
        )
