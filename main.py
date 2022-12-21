from dataclasses import dataclass

orientation_value = {
    "N": {"L": "W", "R": "E", 'value': 1},
    "E": {"L": "N", "R": "S", 'value': 1},
    "S": {"L": "E", "R": "W", 'value': -1},
    "W": {"L": "S", "R": "N", 'value': -1}
}


@dataclass
class state:
    x_pos: int
    y_pos: int
    direction: str


@dataclass
class Bot:
    state: dict
    movement: str
    grid: list[list[any]]
    previous_position: tuple
    output: str

    def __init__(self, coords: tuple, direction: str, movement: str, grid) -> None:
        x, y = coords
        self.state: state = state(x, y, direction.strip().capitalize())
        self.movement = movement.upper().strip()
        self.grid = grid
        self.place()
        self.move_robot()

    @property
    def grid_x_max(self) -> int:
        return len(self.grid) + 1

    @property
    def grid_y_max(self) -> int:
        return len(self.grid[0]) + 1

    def __repr__(self) -> str:
        return f"{self.arrow()}"

    def arrow(self) -> str:
        arrow = {
            "N": "⬆️",
            "E": "➡️",
            "S": "⬇️",
            "W": "⬅️"
        }
        return arrow.get(self.state.direction)

    def move_robot(self) -> None:
        for move in self.movement:
            if self.movement != "LOST":
                self.turn_left_or_right(move)
                self.set_previous_position()
                # save position
                x, y = self.previous_position
                self.move_bot_along_x_axis(move, x, y)
                self.move_bot_along_y_axis(move, x, y)
        result = lost(self) if (
                self.movement == "LOST") else f"({self.state.x_pos}, {self.state.y_pos}, {self.state.direction})"
        self.set_output(result)

    def move_bot_along_x_axis(self, move, x, y) -> None:
        if move == "F" and self.state.direction in "WE":
            val = orientation_value[self.state.direction]['value']
            self.move_bot((val + x), y)

    def move_bot_along_y_axis(self, move, x, y) -> None:
        if move == "F" and self.state.direction in "NS":
            val = orientation_value[self.state.direction]['value']
            self.move_bot(x, (val + y))

    def turn_left_or_right(self, move) -> None:
        if move == "L" or move == "R":
            self.state.direction = orientation_value[self.state.direction].get(move)

    def place(self) -> None:
        try:
            self.grid[self.state.x_pos][self.state.y_pos] = self
        except IndexError:
            self.set_previous_position()
            lost(self)

    def move_bot(self, new_x, new_y) -> None:
        try:
            if new_x >= self.grid_x_max or new_x < 0:
                raise IndexError
            if new_y >= self.grid_y_max or new_y < 0:
                raise IndexError
            self.state.x_pos = new_x
            self.state.y_pos = new_y
        except IndexError:
            x_value = self.previous_position[0]
            y_value = self.previous_position[1]
            self.grid[x_value][y_value] = self
            self.movement = "LOST"

    def set_previous_position(self) -> None:
        self.previous_position = self.state.x_pos, self.state.y_pos

    def set_output(self, string: str) -> None:
        self.output = string


def generate_grid(horizontal_value, vertical_value) -> list[list]:
    return [[''] * vertical_value for _ in range(horizontal_value)]


def lost(bot: Bot) -> str:
    return f"({bot.previous_position[0]}, {bot.previous_position[1]}, {bot.state.direction}) {bot.movement}"


# def print_grid(grid: list, user_grid):
#     grid.reverse()
#     print(*user_grid, sep='\n')


def start_bot(movements: str, user_grid, x, y, direction: str) -> Bot:
    return Bot((int(x), int(y)), direction, movements, user_grid)


def inputs_and_setup(usr_input) -> tuple:
    __coords, __movements = parse(usr_input.replace(" ",""))
    return __coords, __movements


def parse(usr_input) -> str:
    return usr_input.strip().lstrip("(").rsplit(")")


if __name__ == "__main__":
    horizontal_value, vertical_value = map(int, input("input for grid:").split())
    usr_grid = generate_grid(horizontal_value, vertical_value)

    usr_coords, usr_movements = inputs_and_setup(input("input for robot 1:"))
    bot_1 = start_bot(usr_movements, usr_grid, *usr_coords.split(','))

    usr_coords, usr_movements = inputs_and_setup(input("input for robot 2:"))
    bot_2 = start_bot(usr_movements, usr_grid, *usr_coords.split(','))
    print(bot_1.output)
    print(bot_2.output)
