# html-to-table

This repository is no longer maintained, as a better version is available at https://github.com/fhightower/html-to-json.

Repository for parsing html files as tables (in pd.DataFrame format), and writing to excel files.

## Dependencies
```
python>=3.6
pandas
xlwt
requests
xlsxwriter
```

## Install
`pip install git+https://github.com/OlleLindgren/html-to-table@v0.1.1`

## Usage: Parsing html

```
import htmlparser as prs

# Read from url
source_url = r'https://www.bbc.com/news/election/us2020/results'
html_string = prs.get_webpage(source_url)

# Read from downloaded file
source_file = r'inputs/election.html'
html_string = prs.get_htmlfile(source_file)

# Parse html
pagename, tables = prs.parse_html(html_string)
filename = f'{pagename or "results"}.xlsx'

# Write excel. Returns True if anything was written, False otherwise.
success = prs.write_excel(filename, tables)
```
