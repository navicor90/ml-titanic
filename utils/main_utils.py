# -*- coding: utf-8 -*-

import pandas as pd

def group_by_with_main_metrics(df, gbcolumn, index, target):
    gbdf = (df.groupby(gbcolumn)
            .agg({index:'count',target:'sum'})
            .rename_axis(gbcolumn)
            .reset_index())
    gbdf['share'] = gbdf[index]/gbdf[index].sum()
    gbdf['target_rate'] = gbdf[target]/gbdf[index]
    return gbdf

def bin_rate(var, target, bins_number=5, bins = None):
    bsize = (var.max() - var.min())/bins_number
    
    if bins==None:
        bins = np.arange(var.min(), var.max()+1, bsize)
    
    total_bins = pd.cut(var, bins=bins)
    total_bins_count = total_bins.groupby(total_bins).count().to_frame()
    total_bins_count.index.name = None
    total_bins_count.columns = ['total_bins_count']

    true_bins = pd.cut(var[target], bins=bins)
    true_bins_count = true_bins.groupby(true_bins).count().to_frame()
    true_bins_count.index.name = None
    true_bins_count.columns = ['true_bins_count']
    
    table = total_bins_count.join(true_bins_count, how='left')
    table['rate'] = 1.0 * table.true_bins_count/table.total_bins_count
    return table

def categorical_rate(var, target):
    total_cat_count = var.groupby(var).count().to_frame()
    total_cat_count.index.name = None
    total_cat_count.columns = ['total_cat_count']
    true_cat_count = var[target].groupby(var[target]).count().to_frame()
    true_cat_count.index.name = None
    true_cat_count.columns = ['true_cat_count']
    
    table = total_cat_count.join(true_cat_count, how='left')
    table['rate'] = 1.0 * table.true_cat_count/table.total_cat_count
    return table


############### Matplot lib helpers ################

def autolabel_bar(ax, rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')