import argparse
import bibtexparser  # pip install --no-cache-dir --force-reinstall git+https://github.com/sciunto-org/python-bibtexparser@main


_PAPER_TEMPLATE = '''
                <div id="main-pub-card-container" class="activated hide">
                    <div class="pub-card" data-topic="{topics}" data-year="{year}" data-selected="{selected}">
                        <div class="row">
                            <div class="col-r col-xs-12 col-12">
                                <div class="pub-card-body">
                                    <h5 class="title">{title}</h5>
                                    <h6 class="authors">
                                        <u>{authors}</u>
                                    </h6>
                                    <p class="info">
                                        {site}
                                        &nbsp;&nbsp;&nbsp;<a href="{link}"
                                            target="_blank">Paper</a><br>
                                        <span class="highlight">{note}</span>
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
'''


def process_authors(authors: str) -> str:
    authors = authors.split(' and ')
    authors = map(lambda x: reversed([y.strip() for y in x.strip().split(',')]), authors)
    authors = map(lambda x: ' '.join(x), authors)
    return ', '.join(authors)


if __name__ == '__main__':
    with open('data/grounding.bib') as f:
        library = bibtexparser.parse_string(f.read())

    entries = list()
    for item in library.entries:
        year = item['year']
        authors = process_authors(item['author'])
        topics = [x.strip() for x in item['keywords'].split(',')]
        selected = True if 'selected' in topics else False
        title = item['title']
        link = '#'
        note = item['note'] if 'note' in item else ''
        if item.entry_type == 'phdthesis':
            site = f'PhD Thesis, {item["school"]}'
        else:
            site = item['journal'] if 'journal' in item else item['booktitle']
        site += f' {item["year"]}'
        entry = _PAPER_TEMPLATE.format(
            topics=','.join(topics),
            year=year,
            selected='true' if selected else 'false',
            title=title,
            authors=authors,
            site=site,
            link=link,
            note=note
        )
        entries.append(entry)

    with open('index_template.html') as f:
        template = f.read()
        html = template.replace('<!--Papers Come Here-->', '\n'.join(entries))
    with open('index.html', 'w') as f:
        f.write(html)
