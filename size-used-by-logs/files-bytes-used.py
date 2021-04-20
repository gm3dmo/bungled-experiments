#!/usr/bin/env python3

import pandas as pd

def main():

   before = pd.read_csv('before.csv')
   after = pd.read_csv('after.csv')

   ms = pd.merge(before, after, on=['filename'], how='inner')
   ms['bytesUsed'] = ms['size_bytes_y'] - ms['size_bytes_x']
   sums = ms.select_dtypes(pd.np.number).sum().rename('total')
   ms = ms.append(sums)

   print(ms)


if __name__ == "__main__":
    main(