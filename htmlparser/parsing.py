import pandas as pd 
import os 
import re
import requests
from lxml import html
import tempfile

def get_htmlfile(in_dir):
    # Get html from html file
    with open(in_dir, 'r', encoding='UTF-8') as f:
        return f.read()

def get_webpage(url):
    # Get html from webpage URL
    return requests.get(url).text

def parse_html(html_string):

    # Read HTML file in in_dir, return as a list of tables in pd.DataFrame form.

    tables = []
    writing = False
    writing_row = False
    writing_entry = False

    writing_page_name = False
    page_name = None

    garbage_phrases = ['&nbsp;']

    for _, l in enumerate(html_string.replace('<', '\n<').split('\n')):
        
        for g in garbage_phrases:
            l = l.replace(g, '')
        l = l.strip()

        if '<title' in l and page_name is None:
            writing_page_name = True
            page_name = ''
            level=0
        
        if writing_page_name:
            for ch in l.strip():
                if ch == '<':
                    level += 1
                elif ch == '>':
                    level -= 1
                elif level == 0:
                    page_name += ch
        
        if '</title' in l:
            writing_page_name = False
            # Delete non-alphanumeric
            page_name = re.sub(r'\W+', '', page_name)

        if writing:
            # Check for table end
            if '</table' in l:
                try:
                    result = pd.DataFrame(columns=rows[0], data=rows[1:]) if current_has_header else pd.DataFrame(data=rows)
                    tables.append(result)
                except ValueError:
                    tables.append(None)
                writing = False
                continue

            if writing_row:
                # Check for row end
                if '</tr' in l:
                    rows.append(current_row)
                    writing_row = False
                    continue
                
                if '<th' in l:
                    current_has_header = True
                
                if '<th' in l or '<td' in l:
                    writing_entry = True
                    level = 0
                    entry_result = ''

                if writing_entry:
                    for ch in l.strip():
                        if ch == '<':
                            level += 1
                        elif ch == '>':
                            level -= 1
                        elif level == 0:
                            entry_result += ch
                
                if '</th' in l or '</td' in l:
                    writing_entry = False
                    current_row.append(entry_result.strip())
                
            elif '<tr' in l:
                current_row = []
                writing_row = True
        elif '<table' in l:
            rows = []
            writing = True
            current_has_header = False

    return page_name, tables

def write_excel(filename, tables):
    success = False

    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        for i, t in enumerate(tables):
            if t is not None:
                t.to_excel(writer, sheet_name=f'{i}_{t.shape[0]}x{t.shape[1]}', index=False)
                success = True
        if success:
            writer.save()
    return success