# currencyExchangeDemo
<h3>List of currencies</h3>
Get a list of all available currencies + the last 5 exchange transactions<br><code>/currency/</code>

<hr>
Get a list of currencies filtering by keyword + the last 5 exchange transactions<br><code>/currency/?filter_currency=eu</code>

<hr>
Get a list of currencies filtering by keyword + filtering by the most frequently sold and the last 5 exchange transactions<br><code>/currency/?filter_currency=eu&most_frequent=seles</code>

<hr>
Get a list of currencies filtering by keyword + filtering by the most frequently purchased one and the last 5 exchange transactions<br><code>/currency/?filter_currency=eu&most_frequent=shopping</code>

<hr>
Get a list of all available currencies + the list of all exchange transactions with amount of all pages and current pages<br><code>/currency/?all_activity=True</code>

<hr>
Get a list of all available currencies + the list of exchange transactions by particular page, with amount of all and current pages<br><code>/currency/?all_activity=True&page=6</code>

<hr>
Get a list of all available currencies + the list of exchange transactions by particular page filtering by particular currency, with amount of all and current pages
<br><code>/currency/?all_activity=True&page=6&filter_activity=pl</code>
<hr>

<h3>Exchange rate</h3>
Get exchange rate for EUR/USD<br><code>/currency/EUR/USD/</code>
