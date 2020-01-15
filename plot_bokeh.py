import requests
import pandas as pd

from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.themes import Theme


class stocksplot:
    '''encapsulates Bokeh plot and methods to retrieve new data'''

    def __init__(self, api_key_av, symbol=None):
        self.api_key_av = api_key_av
        self.data = None  # no data loaded yet.
        self.symbol = None
        self.selected = 'close'
        self.vdims = ['No data loaded']
        if symbol is not None:
            print("*******************trying to get data")
            self.getDataAlphaVantage(api_key_av, symbol)

    def getDataAlphaVantage(self, api_key_av, symbol):
        '''get new data from Alpha Vantage'''
        if self.symbol == symbol:
            # we already have this loaded; do nothing
            return 1
        old_symbol = self.symbol
        self.symbol = symbol
        old_data = self.data

        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol + '&outputsize=full&apikey=' + api_key_av
        r = requests.get(url)
        if r.ok:
            try:
                data = pd.DataFrame(r.json()['Time Series (Daily)']).transpose()
                data.columns = ['open', 'high', 'low', 'close', 'volume']
                self.vdims = ['close', 'open', 'high', 'low', 'volume']
                data.index = pd.to_datetime(data.index)
                data.open = pd.to_numeric(data.open)
                data.high = pd.to_numeric(data.high)
                data.low = pd.to_numeric(data.low)
                data.close = pd.to_numeric(data.close)
                data.volume = pd.to_numeric(data.volume)
                data = data.reset_index()
                self.data = data
                return 1
            except Exception as inst:
                print(inst)
                self.data = old_data
                self.symbol = old_symbol
                return 0
        else:
            self.symbol = old_symbol
            self.data = old_data
            return 0

    # Define the Bokeh application
    def stocksplot_plot(self, doc):
        '''create a plot based on the current data and selected price'''
        df = self.data
        source = ColumnDataSource(data=df)
        plot = figure(x_axis_type='datetime',
                      y_axis_label=self.selected,
                      x_axis_label='time',
                      title=self.symbol + " ("
                      + self.selected + ")",
                      plot_height=400)
        plot.line('index', self.selected, source=source)
        plot.sizing_mode = 'scale_width'
        doc.theme = Theme(filename="theme.yaml")
        return plot

    @property
    def selected_list(self):
        '''Helper property for the jinja2 selector.
        Determines which value of the pulldown menu is preselected.'''
        return [n == self.selected for n in self.vdims]
