from main import start_bot, inputs_and_setup, generate_grid, Bot

test_input_1 = {
    "input": [
        "4 8",
        "(2, 3, E) LFRFF",
    ],
    "output": [
        "(4, 4, E)",
    ],
}

test_input_2 = {
    "input": [
        "4 8",
        "(1, 0, S) FFRLF",
    ],
    "output": [
        "(1, 0, S) LOST",
    ],

}
test_input_3 = {
    "input": [
        "4 8",
        "(1, 0, S) LLFFF",
    ],
    "output": "(1, 3, N)"

}


def generate_bot(inputs) -> Bot:
    horizontal_value, vertical_value = map(int, inputs['input'][0].split())
    usr_grid = generate_grid(horizontal_value, vertical_value)
    usr_coords, usr_movements = inputs_and_setup(inputs['input'][1])
    return start_bot(usr_movements, usr_grid, *usr_coords.split(','))


def test_inputs_are_valid():
    grid_vals: str
    start_pos_and_moves_1: str
    start_pos_and_moves_2: str
    grid_vals, start_pos_and_moves_1 = test_input_1.get("input")
    vals = grid_vals.split()
    for each in vals:
        assert each.isdigit()
    input_is_two_values = grid_vals.split()
    assert len(input_is_two_values) == 2
    parsed_start_pos, parsed_moves = inputs_and_setup(start_pos_and_moves_1)
    assert parsed_start_pos == "2,3,E"
    assert parsed_moves == "LFRFF"


class TestBot:
    grid_vals: str
    start_pos_and_moves_1: str
    start_pos_and_moves_2: str

    def test_bot_turns_left(self):
        bot = generate_bot(test_input_1)
        bot.movement = "L"
        bot.move_robot()
        assert bot.state.direction == "N"
        bot.movement = "LL"
        bot.move_robot()
        assert bot.state.direction == "S"

    def test_bot_turns_right(self):
        bot = generate_bot(test_input_1)
        bot.movement = "R"
        bot.move_robot()
        assert bot.state.direction == "S"
        bot.movement = "RR"
        bot.move_robot()
        assert bot.state.direction == "N"

    def test_bot_is_lost_and_is_not_lost(self):
        bot = generate_bot(test_input_2)
        assert bot.movement == "LOST"
        bot_2 = generate_bot(test_input_1)
        assert bot_2.movement != "LOST"
        bot_3 = generate_bot(test_input_3)
        assert bot_3.movement != "LOST"
        assert bot_3.output == test_input_3.get("output")
