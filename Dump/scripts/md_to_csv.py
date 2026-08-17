#!/usr/bin/env python3
"""
Convert syllabus Markdown files in the workspace into a single Record.csv
Usage: python scripts/md_to_csv.py
Outputs: Record.csv in the workspace root
"""
import re
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_CSV = ROOT / 'Record.csv'

md_files = sorted([p for p in ROOT.glob('*.md') if p.name.lower() not in ('readme.md','readme.markdown')])
if not md_files:
    print('No .md files found in', ROOT)
    raise SystemExit(1)

nodes = []

course_counter = 0
unit_counter = 0
co_counter = 0
lab_counter = 0


def next_id(prefix, counter):
    return f"{prefix}{counter:03d}"


def clean_text(value):
    return ' '.join(value.strip().split())


def parse_course_line(text):
    text = text.strip().replace('|', ' ')
    if not text or re.match(r'^[|\-\s]+$', text):
        return None
    if re.search(r'^(Total|Semester|Program Outcomes|Savitribai|Faculty|Syllabus for|Course\s+Name|Teaching|Examination|Credits?)\b', text, re.IGNORECASE):
        return None
    m = re.match(r'^(\d{3,6})\s+(.+?)(?:\s{2,}(-|\d+(?:\.\d+)?)(?=\s|$)|$)', text)
    if not m:
        return None
    code = m.group(1)
    title = m.group(2).strip()
    if len(title) < 4 or re.search(r'^(Total|Semester|Program Outcomes|Faculty|Savitribai|Course|Remarks?)\b', title, re.IGNORECASE):
        return None
    hours = ''
    if m.group(3) and m.group(3) != '-':
        hours = f"{m.group(3)} Hrs" if re.match(r'^\d+(?:\.\d+)?$', m.group(3)) else m.group(3)
    return code, title, hours


def parse_unit_line(text):
    text = clean_text(text.replace('|', ' '))
    m = re.match(r'^(Unit\s+[IVX\d]+)[:\.]?\s*-?\s*(.*?)(?:\s+(\d+\s*Hrs?)\.?\s*)?$', text, re.IGNORECASE)
    if not m:
        return None
    title = m.group(1).title()
    tail = m.group(2).strip()
    if tail:
        title += ': ' + tail
    hours = m.group(3) or ''
    return title, hours


def parse_co_line(text):
    text = clean_text(text.replace('|', ' '))
    m = re.match(r'^(CO\s*\d+)[:\)\.-]?\s*(.+)$', text, re.IGNORECASE)
    if not m:
        return None
    return m.group(1).upper(), m.group(2).strip()


def parse_lab_line(text):
    text = clean_text(text.replace('|', ' '))
    if re.search(r'\b(lab|practical|tutorial|tut\b)', text, re.IGNORECASE):
        return text
    return None

for md in md_files:
    text = md.read_text(encoding='utf-8')
    lines = [l.rstrip() for l in text.splitlines()]
    current_node = None

    for line in lines:
        trimmed = line.strip()
        if not trimmed:
            continue

        course_match = parse_course_line(trimmed)
        if course_match:
            code, title, hours = course_match
            course_counter += 1
            cid = 'CRS' + code
            current_node = {
                'ID': cid,
                'PARENT_ID': '',
                'TYPE': 'COURSE',
                'TITLE': f'{code}: {title}',
                'HOURS_OR_MARKS': hours,
                'DETAILS': '',
                'STATUS_TAG': 'PENDING'
            }
            nodes.append(current_node)
            continue

        if current_node is None:
            continue

        unit_match = parse_unit_line(trimmed)
        if unit_match:
            unit_counter += 1
            uid = next_id('UNT', unit_counter)
            current_node = {
                'ID': uid,
                'PARENT_ID': nodes[-1]['ID'],
                'TYPE': 'UNIT',
                'TITLE': unit_match[0],
                'HOURS_OR_MARKS': unit_match[1],
                'DETAILS': '',
                'STATUS_TAG': 'PENDING'
            }
            nodes.append(current_node)
            continue

        co_match = parse_co_line(trimmed)
        if co_match:
            co_counter += 1
            coid = next_id('CO', co_counter)
            current_node = {
                'ID': coid,
                'PARENT_ID': nodes[-1]['PARENT_ID'] or nodes[-1]['ID'],
                'TYPE': 'CO',
                'TITLE': co_match[0],
                'HOURS_OR_MARKS': '',
                'DETAILS': co_match[1],
                'STATUS_TAG': 'PENDING'
            }
            nodes.append(current_node)
            continue

        lab_match = parse_lab_line(trimmed)
        if lab_match:
            lab_counter += 1
            lid = next_id('LAB', lab_counter)
            current_node = {
                'ID': lid,
                'PARENT_ID': nodes[-1]['ID'],
                'TYPE': 'LAB',
                'TITLE': lab_match,
                'HOURS_OR_MARKS': '',
                'DETAILS': '',
                'STATUS_TAG': 'PENDING'
            }
            nodes.append(current_node)
            continue

        if current_node is not None:
            if current_node['DETAILS']:
                current_node['DETAILS'] += '\n' + trimmed
            else:
                current_node['DETAILS'] = trimmed

# write CSV
headers = ['ID','PARENT_ID','TYPE','TITLE','HOURS_OR_MARKS','DETAILS','STATUS_TAG']
with OUT_CSV.open('w',encoding='utf-8',newline='') as f:
    w = csv.writer(f)
    w.writerow(headers)
    for n in nodes:
        row = [n.get(h,'') for h in headers]
        w.writerow(row)

print(f'Wrote {len(nodes)} rows to {OUT_CSV}')
print('Files processed:')
for p in md_files:
    print(' -', p.name)
print('\nOpen Record.csv with the viewer or import into the app.')
