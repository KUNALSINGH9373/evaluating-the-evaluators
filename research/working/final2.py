import openpyxl,csv,re,os,collections
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.utils import get_column_letter
P='/Users/kunalsingh/Desktop/v11_FINAL.xlsx'
v10=list(csv.DictReader(open('/Users/kunalsingh/evaluating-the-evaluators/v10.csv',encoding='utf-8',errors='ignore')))
V10F={r['Finding ID'] for r in v10}; V10R={r.get('Report ID','') for r in v10}
wb=openpyxl.load_workbook(P); ws=wb['v11 findings']
hdr=[c.value for c in ws[1]]; ix={h:i+1 for i,h in enumerate(hdr) if h}
G=lambda r,k: ws.cell(r,ix[k]).value
S=lambda r,k,v: ws.cell(r,ix[k]).__setattr__('value',v)

# ---- fix the 3 UK AISI collisions against v10 ----
taken=V10F | {str(G(r,'Finding ID')) for r in range(2,ws.max_row+1)}
takenR=V10R | {str(G(r,'Report ID')) for r in range(2,ws.max_row+1)}
for row in (558,559,560):
    fid=str(G(row,'Finding ID')); rid=str(G(row,'Report ID'))
    m=re.match(r'^([A-Z]+)-(\d{4})-(\d{2})(.*)$',rid)
    for suf in 'abcdefghij':
        nrid='%s-%s-%s%s%s'%(m.group(1),m.group(2),m.group(3),suf,m.group(4))
        nfid=fid.replace(rid,nrid)
        if nfid not in taken and nrid not in takenR: break
    taken.add(nfid); takenR.add(nrid)
    S(row,'Finding ID',nfid); S(row,'Report ID',nrid)
    S(row,'Notes',re.sub(r'\[ID regenerated [^\]]*\]','',str(G(row,'Notes') or '')).strip()+
      ' [ID regenerated 2026-08-15: the recorded 2026-08 date was wrong; the UK AISI research index dates this item %s. Suffix "%s" avoids a collision with the existing v10 row %s, which is a different report.]'%(G(row,'Publication Date'),suf,fid))
    print('  ',fid,'->',nfid)

# ---- delete blank trailing rows ----
blank=[r for r in range(ws.max_row,1,-1) if not any(ws.cell(r,c).value for c in range(1,ws.max_column+1))]
for r in blank: ws.delete_rows(r)
print('deleted',len(blank),'blank rows ->',ws.max_row-1,'records')

# ---- export the sheets we are about to drop ----
D='/Users/kunalsingh/Desktop/'
for name,fn in [('Removed','v11_removed_rows.csv'),('Applied Changes','v11_applied_changes.csv'),
                ('Revision Summary','v11_revision_summary.csv'),('Legend','v11_legend.csv'),('Worklist','v11_worklist.csv')]:
    if name in wb.sheetnames:
        with open(D+fn,'w',newline='',encoding='utf-8') as f:
            w=csv.writer(f)
            for r in wb[name].iter_rows(values_only=True): w.writerow(['' if v is None else v for v in r])
        print('  exported',fn,wb[name].max_row,'rows')
for name in list(wb.sheetnames):
    if name!='v11 findings': del wb[name]

# ---- drop the audit columns, keep the 40-col schema + Status/Sign-off ----
for col in ('What to check',):
    if col in ix: ws.delete_cols(ix[col]); hdr=[c.value for c in ws[1]]; ix={h:i+1 for i,h in enumerate(hdr) if h}
G=lambda r,k: ws.cell(r,ix[k]).value
S=lambda r,k,v: ws.cell(r,ix[k]).__setattr__('value',v)

# ---- restyle: one sheet, status colours ----
FILL={'REVIEW-SIGNOFF':'E2EFDA','HOLD':'FCE4D6'}
hf=PatternFill('solid',start_color='D9D9D9',end_color='D9D9D9')
for c in range(1,ws.max_column+1):
    ws.cell(1,c).fill=hf; ws.cell(1,c).font=Font(bold=True)
    ws.cell(1,c).alignment=Alignment(wrap_text=True,vertical='bottom')
for r in range(2,ws.max_row+1):
    f=PatternFill('solid',start_color=FILL.get(G(r,'Status'),'FFFFFF'),end_color=FILL.get(G(r,'Status'),'FFFFFF'))
    for c in range(1,ws.max_column+1): ws.cell(r,c).fill=f
ws.freeze_panes='D2'
ws.auto_filter.ref=f"A1:{get_column_letter(ws.max_column)}{ws.max_row}"
for col,w in (('A',16),('B',64),('C',12),('D',30),('E',24),('F',30),('G',16),('H',44),('I',15),('J',18),('K',30),('L',16),('M',44),('N',70),('O',70)):
    ws.column_dimensions[col].width=w
wb.save(P)
st=collections.Counter(G(r,'Status') for r in range(2,ws.max_row+1))
tier=collections.Counter(('A' if G(r,'Action Trackable?')=='yes' else 'B' if G(r,'Eval? (trackable)')=='yes' else 'C') for r in range(2,ws.max_row+1))
ids=[G(r,'Finding ID') for r in range(2,ws.max_row+1)]
print()
print('sheets     :',wb.sheetnames)
print('records    :',ws.max_row-1,'| columns',ws.max_column)
print('status     :',dict(st))
print('tier       :',dict(tier))
print('unique IDs :',len(set(ids)),'| collisions with v10:',len(set(ids)&V10F))
