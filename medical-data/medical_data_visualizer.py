import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv('medical_examination.csv')

# 2
df['bmi'] = df['weight'] / (df['height']/ 100)**2 
df['overweight'] = [1 if bmi > 25 else 0 for bmi in df['bmi']]
df = df.drop(['bmi'], axis=1)
# 3
df['cholesterol'] = df['cholesterol'].apply(lambda x: 0 if x == 1 else 1)
df['gluc'] = df['gluc'].apply(lambda x: 0 if x == 1 else 1)

# 4
def draw_cat_plot():
    # 5
    features = ['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke']
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=features)
    #6, 7, 8
    fig = sns.catplot(
    data=df_cat,
    kind='count',
    x='variable',
    col='cardio',
    hue='value',
    )
    # Customize the plot
    fig.set_ylabels("total") 
    # 9
    fig.savefig('catplot.png')
    return fig.figure


# 10
def draw_heat_map():
    # 11
    # Define masks for weight and height
    weight_mask = (df['weight'] >= df['weight'].quantile(0.025)) & (df['weight'] <= df['weight'].quantile(0.975))
    height_mask = (df['height'] >= df['height'].quantile(0.025)) & (df['height'] <= df['height'].quantile(0.975))

    # Apply masks to create df_heat
    df_heat = df[weight_mask & height_mask]

    # 12
    # creation of correlation matrix
    corr = df_heat.corr(method='pearson')

    # 13
    # Create a mask
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 14
    plt.figure(figsize=(16, 12))
    cmap = sns.diverging_palette(200, 15, l=40, n=9, center="dark", as_cmap=True)
    
    # 15
    svm = sns.heatmap(corr, mask=mask, center=0, annot=True,
            fmt='.1f', square=True, cmap=cmap)
    fig = svm.get_figure()
    # 16
    fig.savefig('heatmap.png')
    return fig.figure
