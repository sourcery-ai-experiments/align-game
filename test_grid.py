import pytest

import squareGrid


@pytest.fixture(params=[3])
def empty_grid(request):
    return squareGrid(request.param)


impossible_wall = [
    (0, 1), (1, 1), (1, 0),
]


@pytest.mark.parametrize('start', [(0, 0)])
@pytest.mark.parametrize('end', [(0, 2), (2, 0), (2, 2)])
@pytest.mark.parametrize(
    'walls, expected', [
        pytest.param(impossible_wall, None),
    ],
)
def test_astar_no_path(empty_grid, start, end, walls, expected):
    # arrange
    for wall in walls:
        empty_grid.grid[wall[0]][wall[1]] = 1
    # act
    path = empty_grid.find_path(start, end)
    # assert
    assert path == expected


@pytest.mark.parametrize('start', [(0, 0)])
@pytest.mark.parametrize(
    'end, walls, expected', [
        pytest.param((0, 2), [(0, 1), (1, 1), (2, 1)], None),
        pytest.param(
            (2, 0),
            [(0, 1), (1, 1), (2, 1)],
            [(0, 0), (1, 0), (2, 0)],
        ),
        pytest.param((2, 2), [(0, 1), (1, 1), (2, 1)], None),
        pytest.param(
            (0, 2),
            [(1, 0), (1, 1), (1, 2)],
            [(0, 0), (0, 1), (0, 2)],
        ),
        pytest.param((2, 0), [(1, 0), (1, 1), (1, 2)], None),
        pytest.param((2, 2), [(1, 0), (1, 1), (1, 2)], None),
        pytest.param((0, 2), [(2, 0), (1, 1), (0, 2)], None),
        pytest.param((2, 0), [(2, 0), (1, 1), (0, 2)], None),
        pytest.param((1, 2), [(2, 0), (1, 1), (0, 2)], None),
    ],
)
def test_astar_path_found(empty_grid, start, end, walls, expected):
    # arrange
    for wall in walls:
        empty_grid.grid[wall[0]][wall[1]] = 1
    # act
    path = empty_grid.find_path(start, end)
    # assert
    assert path == expected


@pytest.mark.parametrize('x_y', [(0, 0), (1, 1), (2, 2)])
@pytest.mark.parametrize('fill', [[(0, 0), (0, 1), (0, 2)]])
def test_find_adjacent(empty_grid, x_y, fill):
    # arrange
    for loc in fill:
        empty_grid.grid[loc[0]][loc[1]] = 1
    # act
    lines = empty_grid.find_adjacent(x_y)
    assert lines is not {0: [], 1: [], 2: [], 3: []}
