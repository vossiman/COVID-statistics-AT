import numpy as np
from lib.util import reds
from matplotlib.lines import Line2D

# These are constants that can be used by external libraries
# we'll use these to rename pandas columns in the data preparation
# modules
YEAR='year'
WEEK='week'
DEATHS='deaths'

def covid_boxplot(data, era=2020, year_col=YEAR, week_col=WEEK, deaths_col=DEATHS):
    """
    plots the post-covid deaths vs. the pre-covid deaths.
    
    The input data frame needs to have the following column names if not specified
    otherwise:
      - year
      - week
      - deaths
    
    `year` and `week` should be integers, but we can handle strings as well.
    """
    data[year_col]   = data[year_col].apply(lambda x: int(x))
    data[week_col]   = data[week_col].apply(lambda x: int(x))
    data[deaths_col] = data[deaths_col].apply(lambda x: int(x))
        
    data_pre  = data[ data[year_col] <  era ]
    data_post = data[ data[year_col] >= era ]

    groupby = data_pre[year_col].unique()
    plot = data_pre.boxplot(column=[deaths_col],
                              by=week_col,
                              figsize=(20,10))

    # This will be the legend
    legend_lines = []
    legend_text  = []

    x_ticks = np.arange(1,54)
    # we go from the latest the first post-covid year, so that the most current
    # data will be bright red (see lib.util.reds()`).
    for year in range( data_post[year_col].max(), data_post[year_col].min() - 1, -1 ):
        # we can't pass the iterator to plot.line(..., color=reds()), as it
        # would internally access it often:
        color = next(reds())
        # create the data for the labels:
        legend_lines.append(Line2D([0], [0], color=color, lw=2))
        legend_text.append('Anzahl Todesfälle ' + str(year))
        # plot the red line on top
        data_post[data_post[year_col]==year].plot.line(
            x='KW',
            y='Anzahl Todesfälle',
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
    plot.set_title('Anzahl der Todesfälle - Vergleich 2000-2019 (box charts) vs. ab 2020 (red lines)')
    
    # update legend
    legend_lines.append(Line2D([0], [0], color="lightblue", lw=2))
    legend_text.append('Anzahl Todesfälle 2000-2019')

    plot.legend(legend_lines, legend_text)

    # better xlabel title
    plot.set_xlabel("Kalenderwoche")
    plot.set_ylabel("Todesfälle")

    lbls = plot.set_xticklabels(x_ticks)
