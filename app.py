import sys
from flask import (Flask, render_template, request, redirect, flash, url_for)

from bokeh.embed import components
from bokeh.io import curdoc

from plot_bokeh import stocksplot

print(sys.argv)
if len(sys.argv) != 2:
    print("You must provide an AlphaVantage \
          API key as a command line argument.")
    exit()
apikey = sys.argv[1]

SECRET_KEY = 'qwdkqjwgd87263et233gwqbsuskg'

app = Flask(__name__)
app.config.from_object(__name__)


plot = stocksplot(apikey, 'MSFT')


@app.route('/')
def bkapp_page():
    '''Render the main page.'''
    doc = curdoc()
    graph = plot.stocksplot_plot(doc)
    script, div = components(graph)
    return render_template('embed.html.j2', script=script,
                           div=div, template='Flask',
                           values=zip(plot.vdims, plot.selected_list),
                           current_symbol=plot.symbol)


@app.route('/new_symbol', methods=['POST'])
def new_symbol():
    '''Load a new ticker symbol, then render the main page.'''
    symbol = request.form['symbol']
    val = request.form['myvalue']
    plot.selected = val
    success = plot.getDataAlphaVantage(api_key_av=apikey, symbol=symbol)
    if success:
        flash('New data successfully retrieved.')
    else:
        flash('Invalid symbol.')
    return redirect(url_for('bkapp_page'))


if __name__ == '__main__':
    app.run(port=33507)
