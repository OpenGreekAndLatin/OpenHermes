from bs4 import BeautifulSoup as b_soup
from glob import glob
from tkinter.filedialog import askdirectory
from collections import defaultdict

orig = askdirectory(title='Where are your original XML lexicon files?')
files = glob('/'.join([orig, '*.xml']))

tr_dict = defaultdict(list)
for file in files:
    with open(file) as f:
        text = f.read()
    soup = b_soup(text)
    for word in soup.find_all('entryfree'):
        for s in word.find_all('sense'):
            try:
                tr_dict[word.orth.text].append(s.tr.text)
            except:
                continue
    
