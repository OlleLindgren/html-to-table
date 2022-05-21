import re
from pathlib import Path
from typing import Iterable, Sequence, Tuple

import pandas as pd
import requests


def get_webpage(url: str) -> str:
    """Get webpage html source.

    Args:
        url (str): Url to get page source from

    Returns:
        str: The html source of the webpage
    """
    # Get html from webpage URL
    return requests.get(url).text


def parse_html(html_string: str) -> Tuple[str, Sequence[pd.DataFrame]]:
    """Parse html and extract page name and a number of tables as pd.DataFrame objects.

    Args:
        html_string (str): html source to parse

    Returns:
        Tuple[str, Sequence[pd.DataFrame]]: page_title, [df1, df2, ...]
    """
    # Read HTML file in in_dir, return as a list of tables in pd.DataFrame form.

    tables = []
    writing = False
    writing_row = False
    writing_entry = False

    writing_page_name = False
    page_name = None

    garbage_phrases = ["&nbsp;"]

    for line in html_string.replace("<", "\n<").splitlines():

        for garbage_string in garbage_phrases:
            line = line.replace(garbage_string, "")
        line = line.strip()

        if "<title" in line and page_name is None:
            writing_page_name = True
            page_name = ""
            level = 0

        if writing_page_name:
            for character in line.strip():
                if character == "<":
                    level += 1
                elif character == ">":
                    level -= 1
                elif level == 0:
                    page_name += character

        if "</title" in line:
            writing_page_name = False
            # Delete non-alphanumeric
            page_name = re.sub(r"\W+", "", page_name)

        if writing:
            # Check for table end
            if "</table" in line:
                try:
                    if current_has_header:
                        result = pd.DataFrame(columns=rows[0], data=rows[1:])
                    else:
                        result = pd.DataFrame(data=rows)
                    tables.append(result)
                except ValueError:
                    pass
                writing = False
                continue

            if writing_row:
                # Check for row end
                if "</tr" in line:
                    rows.append(current_row)
                    writing_row = False
                    continue

                if "<th" in line:
                    current_has_header = True

                if "<th" in line or "<td" in line:
                    writing_entry = True
                    level = 0
                    entry_result = ""

                if writing_entry:
                    for character in line.strip():
                        if character == "<":
                            level += 1
                        elif character == ">":
                            level -= 1
                        elif level == 0:
                            entry_result += character

                if "</th" in line or "</td" in line:
                    writing_entry = False
                    current_row.append(entry_result.strip())

            elif "<tr" in line:
                current_row = []
                writing_row = True

        elif "<table" in line:
            rows = []
            writing = True
            current_has_header = False

    return page_name, tables


def write_excel(filename: Path, tables: Iterable[pd.DataFrame]) -> bool:
    """Write tables to sheets in an excel file.

    Args:
        filename (Path): File to write to
        tables (Iterable[pd.DataFrame]): Tables to write

    Returns:
        bool: True if anything was written
    """

    writes = 0

    table_iterator = (table for table in tables if table is not None)

    with pd.ExcelWriter(filename, engine="xlsxwriter") as writer:
        for table_number, table in enumerate(table_iterator):
            table.to_excel(
                writer,
                sheet_name=f"{table_number}_{table.shape[0]}x{table.shape[1]}",
                index=False,
            )
            writes += 1
        if writes:
            writer.save()

    return writes > 0
