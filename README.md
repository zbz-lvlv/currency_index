# currency_index

What is it?
The program is a currency index generator which can create a index of the relative strength of a given currency. It compares the strength of the given currency against a basket of 20 currencies, weighted according to the respective countries' GDP.

How to use?
1. Run get_data
2. Wait for the program to download the currency data. The Yahoo finance page tends to be unstable, so you might need to download a few times to get the complete set of data
3. Run make_index
4. Open the csv

Tested on the Singapore Dollar, Malaysian Ringgit and US Dollar. Results seem rather believable.
