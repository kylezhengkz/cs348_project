import os
import csv

from ..utils.CmdMessages import TagTypes, print_tagged_message

def init_resource_files(parent_dir, files, file_defaults=None, overwrite=False):
    for key, fname in files.items():
        full_path = os.path.join(parent_dir, fname)
        folder = os.path.dirname(full_path)
        os.makedirs(folder, exist_ok=True)
        
        should_write = overwrite
        if not os.path.exists(full_path):
            should_write = True
        elif os.stat(full_path).st_size == 0:
            should_write = True
        
        if should_write:
            with open(full_path, 'w') as f:
                if file_defaults is not None:
                    f.write('\n'.join(file_defaults[key]) + '\n')
                    print_tagged_message(TagTypes.Success, 'INFO', f'Wrote defaults to: {full_path}')
                else:
                    print_tagged_message(TagTypes.Success, 'INFO', f'Create empty file: {full_path}')
            continue
        print_tagged_message(TagTypes.Warning, 'SKIP', f'File exists and is not empty: {full_path}')

def load_resource_file_data(parent_dir, files, file_defaults):
    data = {}
    for key, fname in files.items():
        path = os.path.join(parent_dir, fname)
        try:
            with open(path) as f:
                lines = [line.strip() for line in f if line.strip()]
                data[key] = lines if lines else file_defaults[key]
        except Exception:
            data[key] = file_defaults[key]
    return data 

def save_to_csv_file(parent_dir, file, labels, rows):
    full_path = os.path.join(parent_dir, file)
    with open(full_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(labels)
        for row in rows:
            writer.writerow(row)
        print_tagged_message(TagTypes.Success, 'INFO', f'Wrote dataset to: {full_path}')
