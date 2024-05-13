import pytest

from squareGrid import SquareGrid


@pytest.fixture(params=[3])
def empty_grid(request):
    return SquareGrid(request.param)


@pytest.mark.parametrize('start', [(0, 0)])
@pytest.mark.parametrize('end', [(2, 2)])
@pytest.mark.parametrize(
    'impossible_walls', [
        [(0, 1), (1, 1), (1, 0)], [
            (0, 1), (1, 0),
        ], [(2, 1), (1, 2)],
    ],
)
@pytest.mark.parametrize(
    'expected', [
        None,
    ],
)
def test_astar_no_path(empty_grid, start, end, impossible_walls, expected):
    # arrange
    for wall in impossible_walls:
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
