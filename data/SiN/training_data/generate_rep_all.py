#!/usr/bin/env python
# coding: utf-8

from concurrent.futures import ProcessPoolExecutor
import numpy as np

from uf3.data import composition
from uf3.representation import bspline
from uf3.representation import process

import pandas as pd


element_list = ["Si", "N"]
n_cores = 32
filename = "df_features_all.h5"
table_template = "features_{}"

chemical_system = composition.ChemicalSystem(element_list=element_list, degree=3)

r_min_map = {}
r_max_map = {}
resolution_map = {}

for i in chemical_system.get_interactions_list():
    if isinstance(i, str):
        pass
    else:
        if len(i) == 2:
            r_min_map[i] = 0.001
            r_max_map[i] = 5.5
            resolution_map[i] = 15
        if len(i) == 3:
            r_min_map[i] = [0.75] * 3
            r_max_map[i] = [3.5, 3.5, 7.0]
            resolution_map[i] = [6, 6, 12]

bspline_config = bspline.BSplineBasis(
    chemical_system,
    r_min_map=r_min_map,
    r_max_map=r_max_map,
    resolution_map=resolution_map,
    leading_trim=0,
    trailing_trim=3,
)

df_data = pd.read_pickle("all.pkl")


print("Number of energies:", len(df_data))
print("Number of forces:", int(np.sum(df_data["size"]) * 3))


representation = process.BasisFeaturizer(bspline_config)
client = ProcessPoolExecutor(max_workers=n_cores)

representation.batched_to_hdf(
    filename,
    df_data,
    client,
    n_jobs=n_cores,
    batch_size=500,
    progress="bar",
    table_template=table_template,
)
