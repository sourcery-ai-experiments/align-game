from unittest import mock

import pytest

from coloredRect import ColoredRect
from constants import BLACK
from game import AlignIt
from game import normalize_cords


@pytest.mark.parametrize(
    'x_pix_cords, y_pix_cords, expected_x, expected_y', [
        pytest.param(176, 234, 150, 200),
        pytest.param(100, 150, 100, 150),
        pytest.param(105, 200, 100, 200),
        pytest.param(200, 155, 200, 150),
        pytest.param(50, 50, 50, 50),
        pytest.param(0, 0, 0, 0),
        pytest.param(199, 234, 150, 200),
    ],
)
def test_normalize_cords(x_pix_cords, y_pix_cords, expected_x, expected_y):
    x, y = normalize_cords(x_pix_cords, y_pix_cords)
    assert x == expected_x
    assert y == expected_y


@pytest.mark.skip
@mock.patch('coloredRect.ColoredRect.draw_colored_rect')
@mock.patch('pygame.display.update')
def test_handle_sqr_movement(mock_rect, mock_video):
    game = AlignIt()
    path = [(0, 0), (0, 1), (0, 2)]
    game.handle_sqr_movement(path)
    first = path[0]
    last = path[-1]
    assert game.space[first[0]][first[1]] == 0
    assert game.space[last[0]][last[1]] == 1


@pytest.mark.parametrize(
    'x_sqr_crd, y_sqr_crd, spc_x_cords, spc_y_cords', [
        pytest.param(150, 150, 0, 0),
        pytest.param(200, 200, 1, 1),
        pytest.param(300, 350, 3, 4),
    ],
)
def test_select_square(
        x_sqr_crd, y_sqr_crd, spc_x_cords, spc_y_cords,
):
    game = AlignIt()
    x, y = game.get_square_cords(x_sqr_crd, y_sqr_crd)
    assert x == spc_x_cords
    assert y == spc_y_cords


@pytest.mark.parametrize(
    'directions, x, y',
    [
        pytest.param(
            {
                0: [(0, 0), (1, 0), (2, 0)],
                1: [(0, 0), (0, 1), (0, 2)],
                2: [(0, 0), (1, 1), (2, 2)],
                3: [(0, 0)],
            }, 0, 0,
        ),
        pytest.param(
            {
                0: [(1, 1), (2, 1), (0, 1)],
                1: [(1, 1), (1, 2), (1, 0)],
                2: [(1, 1), (2, 2), (0, 0)],
                3: [(1, 1), (2, 0), (0, 2)],
            }, 1, 1,
        ),
    ],
)
def test_find_adjacent_color(directions, x, y):
    game = AlignIt()
    game.space = [[1 for _ in range(3)] for _ in range(3)]
    game.sqr_grid = [
        [ColoredRect(BLACK, x, y)for x in range(3)] for y in range(3)
    ]
    lines = game.find_adjacent_color(x, y)
    assert lines[0] == directions[0]
    assert lines[1] == directions[1]
    assert lines[2] == directions[2]
    assert lines[3] == directions[3]


@mock.patch('coloredRect.ColoredRect.draw_colored_rect')
def test_check_length_remove_square(mock_rect):
    game = AlignIt()
    game.space = [[1 for _ in range(5)] for _ in range(5)]
    game.sqr_grid = [
        [ColoredRect(BLACK, x, y)for x in range(5)] for y in range(5)
    ]
    lines = {0: [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]}
    game.check_length_remove_square(lines)
    for line in lines.values():
        for x, y in line:
            assert game.sqr_grid[x][y].draw_colored_rect(BLACK)
            assert game.space[x][y] == 0
    assert game.spawn is False
    assert game.scoreall == 5
