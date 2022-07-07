# USD / NIO converter tool
This small Flask web app converts United States dollars to Nicaraguan cordobas and vice versa.
The exchange rate is web-scraped from the official website of the [Central Bank of Nicaragua](https://www.bcn.gob.ni/).
*Warning: every single conversion sends a new request to the Central Bank's web server, so please be kind and do not abuse it.*
You can use this tool in either of two ways:
* Go to the home page and use the web form.
* Directly enter your currency amounts from your browser's address bar (e.g. "http://appurl/usdtonio/123.45" or "http://appurl/niotousd/123.45").
The latter option is especially useful if you combine it with your browser's built-in address bar search engine capabilities.
*(see instructions on how to configure your browser to do this [here](https://www.groovypost.com/howto/add-custom-search-engine-chrome/)*
If you have any issues or suggestions for this web app, feel free to contact me at [rleonblandon@gmail.com](mailto:rleonblandon@gmail.com).
