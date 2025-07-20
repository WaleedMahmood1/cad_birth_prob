# cad_birth_prob


### Additional Comments

#### "?format=json&per_page=30000"
- I added this because I would like a json format as json files have smaller sizes. 
- The default is 50 results per page. And since we need to fetch data of all countries over many years, I have kept the per_page as a high number to ensure all records are fetched in one request. (highest number possible without an HTTPError is 32767)
Citation: (https://datahelpdesk.worldbank.org/knowledgebase/articles/898581-api-basic-call-structures)

#### raise_for_status()
- I have used this method to ensure a check if any error occurred during the request. (useful for checking the highest per_page value in the url)
Citation: (https://www.geeksforgeeks.org/python/response-raise_for_status-python-requests/)

#### response.json()
- Parses the response content into a Python dictionary.
Citation: (https://developer.mozilla.org/en-US/docs/Web/API/Response/json)

#### json_normalize()
- This is a method I used, from the pandas library that converts nested JSON objects into a flat table. The flat table (dataframe) can be more easily used for data analysis. 
Citation: (https://pandas.pydata.org/docs/reference/api/pandas.json_normalize.html)

