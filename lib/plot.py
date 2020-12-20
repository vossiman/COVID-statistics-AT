import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from enum import Enum, auto
from matplotlib.lines import Line2D
from lib.util import reds


# These are constants that can be used by external libraries
# we'll use these to rename pandas columns in the data preparation
# modules
@dataclass
class ColNames:
    year: str
    week: str
    deaths : str

DEFAULT_COL_NAMES = ColNames(
    year = 'year',
    week = 'week',
    deaths = 'deaths')


@dataclass
class Labels:
    plot_title : str
    legend_label_deaths_registered : str
    axis_label_week : str
    axis_label_deaths : str
    

DEFAULT_LABELS = {
    'en' : Labels(
        plot_title = 'Deaths registered - comparison 2000-2019 (box plot) vs. since 2020 (red lines)',
        legend_label_deaths_registered = 'Deaths registered',
        axis_label_week = 'Week',
        axis_label_deaths = 'Deaths registered'
    ),
    'de' : Labels(
        plot_title = 'Anzahl der Todesfälle - Vergleich 2000-2019 (Box-Plot) vs. ab 2020 (rote Linien)',
        legend_label_deaths_registered = 'Anzahl Todesfälle',
        axis_label_week = 'KW',
        axis_label_deaths = 'Anzahl Todesfälle'
    )
}

def covid_boxplot(data, era=2020, col_names=DEFAULT_COL_NAMES, labels=DEFAULT_LABELS['de']):
    """
    plots the post-covid deaths vs. the pre-covid deaths.
    
    The input data frame needs to have the following column names if not specified
    otherwise:
      - year
      - week
      - deaths
    
    `year` and `week` should be integers, but we can handle strings as well.
    """
    data[col_names.year]   = data[col_names.year].apply(lambda x: int(x))
    data[col_names.week]   = data[col_names.week].apply(lambda x: int(x))
    data[col_names.deaths] = data[col_names.deaths].apply(lambda x: int(x))
        
    data_pre  = data[ data[col_names.year] <  era ]
    data_post = data[ data[col_names.year] >= era ]

    groupby = data_pre[col_names.year].unique()
    
    # non-transparent, white background
    fig, plot = plt.subplots(facecolor='white')
    
    data_pre.boxplot(ax=plot,
                     column=[col_names.deaths],
                     by=col_names.week,
                     figsize=(20,10))

    # This will be the legend
    legend_lines = []
    legend_text  = []

    x_ticks = np.arange(1,54)
    # we go from the latest the first post-covid year, so that the most current
    # data will be bright red (see lib.util.reds()`).
    for year in range( data_post[col_names.year].max(), data_post[col_names.year].min() - 1, -1 ):
        # we can't pass the iterator to plot.line(..., color=reds()), as it
        # would internally access it often:
        color = next(reds())
        # create the data for the labels:
        legend_lines.append(Line2D([0], [0], color=color, lw=2))
        legend_text.append(labels.legend_label_deaths_registered + ' ' + str(year))
        # plot the red line on top
        data_post[data_post[col_names.year]==year].plot.line(
            x=col_names.week,
            y=col_names.deaths,
            color=color, 
            ax=plot, 
            figsize=(20,10),
            xticks=x_ticks)

    
    

    ###
    # Labels, Axes, ...
    ###

    # normalize the graph
    plot.set_xlim(-1, 54)
    plot.set_ylim(0, 2800)
    plot.grid(axis='y')

    
    # removing the "grouped by" boxplot auto text & set new header
    plot.get_figure().suptitle('')
    plot.set_title(labels.plot_title)
    
    # update legend
    legend_lines.append(Line2D([0], [0], color='lightblue', lw=2))
    legend_text.append(labels.legend_label_deaths_registered + ' ' + '2000-2019')

    plot.legend(legend_lines, legend_text)

    # better xlabel title
   # plot.set_xlabel("Kalenderwoche")
   # plot.set_ylabel("Todesfälle")

    lbls = plot.set_xticklabels(x_ticks)
