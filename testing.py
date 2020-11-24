import htmlparser as prs

if __name__ == "__main__":
    # source = r'https://www.bbc.com/news/election/us2020/results'
    # html_string = get_webpage(source)

    source = r'inputs/election.html'

    html_string = prs.get_htmlfile(source)

    pagename, tables = prs.parse_html(html_string)

    filename = f'results/{pagename or "results"}.xlsx'

    success = prs.write_excel(filename, tables)
    
    if success:
        print(f"Wrote files {[i for i, t in enumerate(tables) if t is not None]} to file {filename}.")
    else:
        if len(tables) == 0:
            print(f'No tables found in {source}')
        else:
            print(f"{len(tables)} tables were found, but excel write failed.") 