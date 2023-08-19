import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=True, index_col='date')

# Clean data
df = df[(df.value >= df.value.quantile(0.025))
        & (df.value <= df.value.quantile(0.975))]


def draw_line_plot():
  # Draw line plot
  fig = plt.figure(figsize=(32, 9))
  plt.plot(df.index, df.value)
  plt.xlabel('Date')
  plt.ylabel('Page Views')
  plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

  # Save image and return fig (don't change this part)
  fig.savefig('line_plot.png')
  return fig


def draw_bar_plot():
  # Copy and modify data for monthly bar plot
  df['year'] = df.index.year
  df['month'] = df.index.month_name()

  df_bar = pd.DataFrame(
    df.groupby(['year', 'month'])['value'].mean().reset_index())
  #df_bar = df_bar.unstack()
  months = [
    'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
  ]
  #print(df_bar.head())
  table = pd.pivot_table(df_bar,
                         values='value',
                         index='year',
                         columns='month',
                         dropna=False)
  table = table.reindex(columns=months)
  # Draw bar plot
  fig = table.plot(kind='bar', figsize=(16, 9)).figure
  plt.xlabel('Years')
  plt.ylabel('Average Page Views')
  #plt.legend(title = 'Months', fontsize = 15, labels = months)
  #plt.show()

  # Save image and return fig (don't change this part)
  fig.savefig('bar_plot.png')
  return fig


def draw_box_plot():
  # Prepare data for box plots (this part is done!)
  df_box = df.copy()
  df_box.reset_index(inplace=True)
  df_box['year'] = [d.year for d in df_box.date]
  df_box['month'] = [d.strftime('%b') for d in df_box.date]

  #print(df_box.head())
  # Draw box plots (using Seaborn)
  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 9))
  sns.boxplot(x=df_box['year'], y=df_box['value'],
              ax=ax1).set(title='Year-wise Box Plot (Trend)',
                          xlabel='Year',
                          ylabel='Page Views')

  sns.boxplot(x=df_box['month'],
              y=df_box['value'],
              ax=ax2,
              order=[
                'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
                'Oct', 'Nov', 'Dec'
              ]).set(title='Month-wise Box Plot (Seasonality)',
                     xlabel='Month',
                     ylabel='Page Views')

  # Save image and return fig (don't change this part)
  fig.savefig('box_plot.png')
  return fig
