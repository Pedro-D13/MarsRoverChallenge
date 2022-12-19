from dataclasses import dataclass

orientation_value = {
    "N": {"L": "W", "R": "E", 'value': 1},
    "E": {"L": "N", "R": "S", 'value': 1},
    "S": {"L": "E", "R": "W", 'value': -1},
    "W": {"L": "S", "R": "N", 'value': -1}
}


@dataclass
class Bot:
    state: dict
    movement: str
    grid: list
    previous_position: tuple

    def __init__(self, coords: tuple, direction: str, movement: str, grid):
        x, y = coords
        self.state = {'x': x, 'y': y, 'direction': direction.strip().capitalize()}
        self.movement = movement.upper().strip()
        self.grid = grid
        self.place()
        self.move_robot()

    def __repr__(self):
        return f"{self.arrow()}"

    def arrow(self):
        arrow = {
            "N": "⬆️",
            "E": "➡️",
            "S": "⬇️",
            "W": "⬅️"
        }
        return arrow.get(self.state["direction"])

    def move_robot(self):
        try:
            for move in self.movement:
                self.turn_left_or_right(move)
                self.set_previous_position()
                x, y = self.previous_position
                self.grid[x][y] = ""
                self.move_bot_along_y_axis(move, x, y)
                self.move_bot_along_x_axis(move, x, y)
        except IndexError:
            self.movement = "LOST"
            print("cannot place bot here")
        if self.movement == "LOST":
            lost(self)
        else:
            print(self.state["x"], self.state["x"], self.state["direction"])

    def move_bot_along_x_axis(self, move, x, y):
        if move == "F" and self.state["direction"] in "WE":
            val = orientation_value[self.state['direction']]['value']
            self.move_bot(x, (y + val))

    def move_bot_along_y_axis(self, move, x, y):
        if move == "F" and self.state["direction"] in "NS":
            val = orientation_value[self.state['direction']]['value']
            self.move_bot((x + val), y)

    def turn_left_or_right(self, move):
        if move == "L" or move == "R":
            self.state['direction'] = orientation_value[self.state['direction']].get(move)

    def place(self):
        try:
            self.grid[self.state['x']][self.state['y']] = self
        except IndexError:
            self.set_previous_position()
            lost(self)

    def move_bot(self, new_x, new_y):
        try:
            self.state['x'] = new_x
            self.state['y'] = new_y
            self.grid[new_x][new_y] = self
        except IndexError:
            x_value = self.previous_position[0]
            y_value = self.previous_position[1]
            self.move_bot(x_value, y_value)

    def set_previous_position(self):
        self.previous_position = self.state['x'], self.state['y']


def generate_grid(horizontal_value, vertical_value):
    return [[''] * vertical_value for _ in range(horizontal_value)]


def lost(previous_coords: Bot):
    print(*previous_coords.previous_position,previous_coords.movement,"LOST")


def print_grid(grid: list, user_grid):
    grid.reverse()
    print(*user_grid, sep='\n')


def start_bot(movements: str, user_grid, x, y, direction: str):
    return Bot((int(x), int(y)), direction, movements, user_grid)


def starting_position_and_movement():
    __coords, __movements = input("input for robot").strip().lstrip("(").rsplit(")")
    return __coords, __movements


if __name__ == "__main__":
    user_input = list(input("input for grid:").split(" "))
    x, y = int(user_input[1]), int(user_input[0])
    user_grid = generate_grid(x+1, y+1)
    coords, movements = starting_position_and_movement()
    bot_1 = start_bot(movements, user_grid, *coords.split(','))
    print("bot1")
    print_grid(bot_1.grid, user_grid)

