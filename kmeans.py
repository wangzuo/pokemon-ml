import json
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans

# TODO: move to notebook
pokemon = pd.read_csv('./pokedex/pokemon.csv').sort_values(by=['number'])
types = set.union(set(pokemon['type1'].value_counts().keys()), set(
    pokemon['type2'].value_counts().keys()))
egg_groups = set.union(set(pokemon['egg_group1'].value_counts().keys()), set(
    pokemon['egg_group2'].value_counts().keys()))
new_types = {k: v+1 for v, k in enumerate(types)}
new_egg_groups = {k: v+1 for v, k in enumerate(egg_groups)}
tf = {True: 1, False: 0}

data = pokemon.drop(columns=['number', 'name', 'image']) \
    .fillna(value=0) \
    .replace({"type1": new_types, "type2": new_types}) \
    .replace({"egg_group1": new_egg_groups, "egg_group2": new_egg_groups}) \
    .replace({"has_gender": tf, "is_legendary": tf})

k = 3
kmeans = KMeans(init="k-means++", n_clusters=k)
reduced_data = PCA(n_components=2).fit_transform(data)
kmeans.fit(reduced_data)

h = 10
x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

with open('./map/pokemons.json', 'w') as f:
    f.write(pokemon[['number', 'name', 'image', 'generation']
                    ].to_json(orient="records"))

with open('./map/points.json', 'w') as f:
    json.dump(reduced_data.tolist(), f)
