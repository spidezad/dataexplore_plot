"""
    Data Explore plotting module.

    module:
    pca 2 component scatter
    multiple subplots box, hist


"""

import sys, re, time, datetime, os, math
import numpy as np
import pandas as pd
import seaborn as sns
from pylab import plt


import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def pca_2component_scatter(data_df, predictors, legend, sav_fig=0 , savefname = r'c:\data\temp\ans.png'):
    """
        outlook of data set by decomposing data to only 2 pca components.
        do: scaling --> either maxmin or stdscaler

    """

    print 'PCA plotting'

    data_df[predictors] =  StandardScaler().fit_transform(data_df[predictors])

    pca_components = ['PCA1','PCA2'] #make this exist then insert the fit transform
    pca = PCA(n_components = 2)
    for n in pca_components: data_df[n] = ''
    data_df[pca_components] = pca.fit_transform(data_df[predictors])

    sns.lmplot('PCA1', 'PCA2',
       data=data_df,
       fit_reg=False,
       hue=legend,  
       scatter_kws={"marker": "D",
                    "s": 100})


    fig = plt.gcf()
    if sav_fig:
        plt.savefig(savefname)
    plt.show()

def multiple_subplots(attribute_list, group, dataset, plot_type = 'hist', row_category_split = 0, row_category_split_col ='dummy', sav_fig=0 , savefname = r'c:\data\temp\ans.png', **kwargs):
    """ Create multiple subplots within a figure ( currently box, hist) based on the attribute list. May purpose is to ensure y-axis auto scaling for each subplot and does not share y axis.
        By default, it create n by column (default 3) number of subplot within a single figure. n is based on len(attribute_list)/column.

        Args:
            attribute_list (list): (row_category_split = 0)list of column names to plot. Each column name is put under one plot
                                   (row_category_split = 1)list of sub category to plot. Each sub cat is put under one plot
            group ('str'):          category option within a plot. Only avaliable for box plot. where the x-axis is group.
            dataset ('dataframe'):  attribute_list items, group and row_category_split_col must be present in the dataset.

        Kwargs:
            plot_type(str): hist (histogram) or box (boxplot) option.
            row_category_split: default 0. Applicable for boxplot. allow sub plot by splitting the plots based on target row (row_category_split_col)
            sav_fig (bool): default 0, if sav_fg = 1, will save figure beside showing it, will use savefname  as the save filename.

        Additional parameters:
            column_default (int): default 3. change the layout of the figure.
            
        Normally for box plot each plot is based on each column group by "group" (if row_category_split = 0)
        if row_category_split = 1 

   
    """
    if kwargs.has_key('column_default'):
        column_default = float(kwargs['column_default'])
    else:
        column_default = 3.0

    num_rows =  int(math.ceil(len(attribute_list)/column_default))
    gs = gridspec.GridSpec(num_rows, int(column_default))

    row_index= 0
    temp_col = 0
    for n in attribute_list:
        ax = plt.subplot(gs[row_index, temp_col])

        if plot_type == 'hist':
            dataset[n].hist(ax =ax) #may need to add title
            ax.set_title(n)
            
        if plot_type == 'box':
            if not row_category_split: 
                dataset[[n,group]].boxplot(by=group, sym='k.', vert=True, whis=1.5, ax =ax) #symbol is as a result of seaborn with pylab issue
            else:
                dataset[dataset[row_category_split_col]== n].boxplot(by=group, sym='k.', vert=True, whis=1.5, ax =ax) #symbol is as a result of seaborn with pylab issue
                ax.set_title(n)

        temp_col = temp_col + 1
        if temp_col == 3:
            row_index = row_index + 1
            temp_col = 0

    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    plt.tight_layout()
    if sav_fig:
        plt.savefig(savefname)
    plt.show()


if __name__ == "__main__":
    print 'start'
