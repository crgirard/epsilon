from flask import Flask, request, redirect, render_template, Markup, session
from pprint import pprint
import hashlib
import json
import time
import random
import os
import re
import build_results



app = Flask(__name__)

db = build_results.DB()

with open('pages.json','r') as f:
    pages = json.load(f)

db = build_results.DB()
for page in pages:
    db.addPage(page)

@app.route('/')
def home():
    return render_template('home.html')

def makeNavbarButton(disabled,e):
    if type(e) == type('string'):
        data = {'disabled':disabled,
                'payload':Markup('  <i class="material-icons">{0}</i>'.format(e))}
    else:
        data = {'disabled':disabled,
                'payload':Markup('  <span style="font-weight:400;font-size:20px;line-height:20px">{0}</span>'.format(e))}

    return render_template('results_navbar.html',**data)


def makeNavbar(navbar):
    symbolToIconName = {'|<':'first_page',
                        '<': 'chevron_left',
                        '>': 'chevron_right',
                        '>|': 'last_page'}

    button = []
    for n in navbar:
        if type(n) == type(1):
            if n == 2:
                disabled = 'disabled'
            else:
                disabled = ''
            button.append(makeNavbarButton(disabled,n))
        elif n in symbolToIconName.keys():
            button.append(makeNavbarButton('',symbolToIconName[n]))
    return '\n'.join(button)


def makeChip(keyword):
    data = {'keyword':keyword}

    return render_template('results_chip.html',**data)

def makeCard(url,chips):
    chips = [makeChip(c) for c in chips]

    data = {'title':re.sub('_',' ',url)+' - Wikipedia',
            'url':'https://en.wikipedia.org/wiki/'+url,
            'summary':'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris sagittis pellentesque lacus eleifend lacinia...',
            'chips':Markup('\n'.join(chips))}

    return render_template('results_card.html',**data)

def makeResults(query,results,navbar):
    cards = [makeCard(r,['Chip 1','Chip 2','Chip 3']) for r in results]

    data = {'query':' '.join(query),
            'results':Markup('\n'.join(cards)),
            'navbar':Markup(makeNavbar(navbar))}

    return render_template('results.html',**data)



@app.route('/search')
def search():
    query = request.args.get('q')
    if query == None:
        return redirect('/')

    results = db.query(query)
    return makeResults([query],results[:10],['|<',1,2,3,4])



if __name__ == '__main__':
    app.run(debug=True)
