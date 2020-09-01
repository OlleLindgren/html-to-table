import pandas as pd 
import os 

html_file_dir = r'C:\Users\lindg\Documents\tma947 Nonlinear Optimization\tma_course_page.html'
out_dir = r'C:\Users\lindg\Documents\tma947 Nonlinear Optimization\tma_course_page_table_parse'

tab_name = 'table'
tab_row_name = 'tr'
tab_elem_name = 'td'
tab_colname_name = 'th'

colnames = None
tab_start = None
tab_end = None

tables = []
writing = False
writing_row = False
writing_entry = False

if __name__ == "__main__":
    with open(html_file_dir, 'r', encoding='UTF-8') as f:

        for i, l in enumerate(f.readlines()):

            l = l.replace('&nbsp;', '').strip()

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

    write_success = False
    for i, t in enumerate(tables):
        if not os.path.isdir(out_dir):
            os.mkdir(out_dir)
        if t is not None:
            t.to_excel(os.path.join(out_dir, f'{i}_{t.shape[0]}x{t.shape[1]}.xlsx'))
            write_success = True
    if write_success:
        print(f"Wrote files {[i for i, t in enumerate(tables) if t is not None]} in directory {out_dir}.")
    else:
        print(f"No file was successfully written.")