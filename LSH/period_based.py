from LSH.LSH.numba_helpers import *



class Periods:
    def __init__(self, list_of_periods, bin_size):
        pass





def coordinates_to_periods(coordinates):
    c1 = np.array(coordinates[:1])
    c2 = np.array(coordinates[1:])
    return c2 - c1

def multiple_coordinates_to_periods(multiple_coordinates, max_len=100):
    res = np.zeros((len(multiple_coordinates), max_len))
    for i in range(res.shape[0]):
        periods = coordinates_to_periods(multiple_coordinates[i])
        shape = periods.shape[0]
        res[i,:shape] = periods
    return res


if __name__ == "__main__":
    coords = [[1,5,20,30,35,37,100],[2,4,20,25,30,35,50]]
    res = multiple_coordinates_to_periods(coords, max_len=7)

