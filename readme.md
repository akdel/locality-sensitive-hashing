## Locality sensitive hashing

* Implements lsh with numba + numpy.

### Example usage:

```py
from LSH.lsh import VectorsInLSH

list_of_signals = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                   [2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                   [5, 4, 3, 2, 1, 0, -1, -2, -3, -4],
                   [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10],
                   [1, 3, 1, 3, 1, 3, 1, 3, 1, 3],
                   [2, 4, 2, 4, 2, 4, 2, 4, 2, 4]]

lsh = VectorsInLSH(8, list_of_signals)
print(lsh.search_results)
```

This gives us, `array([b'+', b'+', b'M', b'\xf4', b'm', b'm'], dtype='|S1')`.
As expected, the first two signals and the last two signals are put in the same bins.
In this example, the maximum number of bin hashes are 512, each using 8 bits.
Number of bits used can be changed to change the specificity of each bin.
For simplicity, the number of bits can only be more than or equal to 8 and powers of 2.
