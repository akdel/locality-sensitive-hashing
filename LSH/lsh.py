from LSH.numba_helpers import *


class Vectors:
    def __init__(self, list_of_signals):
        length = self._check_lengths(list_of_signals)
        self.vectors = np.zeros((len(list_of_signals), length))
        self._load_signals(list_of_signals)

    def _check_lengths(self, list_of_signals):
        try:
            assert len(set([len(signal) for signal in list_of_signals])) == 1
        except AssertionError:
            raise AssertionError("Signal lengths are unequal. Consider padding, trimming or/and aligning.")
        return len(list_of_signals[0])

    def _load_signals(self, list_of_signals):
        for i in range(len(list_of_signals)):
            self.vectors[i] = np.array(list_of_signals[i])


class LSH:
    def __init__(self, length, dimensions, custom_table=None):
        self.length = length
        self.dim = dimensions
        if custom_table is None:
            self.table = create_random_vectors(length, dimensions)
        else:
            self.table = None
            self.create_custom_table(custom_table)

    def create_custom_table(self, custom_table):
        try:
            assert custom_table.shape[1] == self.dim
            assert custom_table.shape[0] == self.length
        except AssertionError:
            raise AssertionError("Either the dimensions or the length does not match the given table shape.")
        self.table = np.zeros((self.length, self.dim), dtype=np.float64)
        for i in range(custom_table.shape[0]):
            self.table[i] = custom_table[i] - np.mean(custom_table[i])

    def search_signal(self, signal):
        return np.packbits(vector_score(signal, self.table).astype(np.bool)).view("uint8")

    def search_signals(self, signals):
        res = np.zeros((signals.shape[0], self.table.shape[0]), dtype=np.int8)
        vector_scores(self.table, signals, res)
        return np.packbits(res.astype(np.bool)).reshape((signals.shape[0], -1)).view("uint8")


class VectorsInLSH(Vectors, LSH):
    def __init__(self, length, signals, custom_table=None):
        try:
            assert np.log2(length) % 1 == 0.0
        except AssertionError:
            raise AssertionError("Bits shifted due to bad length. Use powers of 2.")
        Vectors.__init__(self, signals)
        LSH.__init__(self, length, self.vectors.shape[1], custom_table=custom_table)
        self.search_results = self.search_signals(self.vectors)
        self.search_results = self.search_results.view("|S%s" % self.search_results.shape[1]).flatten()
        self.bin_ids_used, self.bin_counts = np.unique(self.search_results, return_counts=True)

    def return_hashbin_of_signal_id(self, signal_id):
        return self.search_results[signal_id]

    def return_signals_for_bin(self, bin_id):
        return self.vectors[self.search_results == bin_id]

    def return_signal_ids_for_bin(self, bin_id):
        return np.where(self.search_results == bin_id)[0]


if __name__ == "__main__":
    list_of_signals = np.arange(200000).reshape(200, -1).astype(float)
    list_of_signals[:100] = np.sin(np.deg2rad(list_of_signals[:100]))
    list_of_signals[100:120] *= -1
    list_of_signals[120:170] *= 0.0001
    lsh = VectorsInLSH(32, list_of_signals)

    print(len(list_of_signals))
    print("search results: ", lsh.search_results, "\nbin counts: ", lsh.bin_counts)
    print("hashbin signal %s is in this bin: " % 1, lsh.return_hashbin_of_signal_id(150),
          "\nthis bin (%s) contains these signal/s: " % lsh.return_hashbin_of_signal_id(150),
          lsh.return_signal_ids_for_bin(lsh.return_hashbin_of_signal_id(150)),
          "\nbin ids used: ", lsh.bin_ids_used,
          "\nsignals in bin: ", lsh.return_signals_for_bin(lsh.bin_ids_used[0]))
