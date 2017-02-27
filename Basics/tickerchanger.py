def yahoo_to_quandl(y_ticker):
    if '-' in y_ticker:
        q_ticker = y_ticker.replace('-', '_')
    else:
        q_ticker = y_ticker

    if '.' in y_ticker:
        q_ticker = q_ticker.split(".", 1)[1] + '_' + q_ticker.split(".", 1)[0]
    return q_ticker


def quandl_to_yahoo(q_ticker):
    if '_' in q_ticker:
        q_ticker = q_ticker.replace('_', '-')

    if 'TO-' in q_ticker[0:3]:
        y_ticker = q_ticker.split("TO-", 1)[1] + '.TO'

    else:
         y_ticker = q_ticker

    return y_ticker


if __name__ == '__main__':
    print(quandl_to_yahoo('TO_BBD_B'))
    print(yahoo_to_quandl('BBD-B.TO'))
