import json

def extract(in_file, out_file):
    with open(in_file, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    with open(out_file, 'w', encoding='utf-8') as f:
        for cell in nb.get('cells', []):
            if cell.get('cell_type') == 'code':
                f.write(''.join(cell.get('source', [])))
                f.write('\n\n')

extract('c:/ECC/ECC/main.ipynb', 'c:/ECC/ECC/main_code.py')
extract('c:/ECC/ECC/encontristas.ipynb', 'c:/ECC/ECC/encontristas_code.py')
