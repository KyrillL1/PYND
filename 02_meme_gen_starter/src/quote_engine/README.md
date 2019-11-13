# Quote Engine

## Classes
- QuoteModel(body, author) receives a quote consisting of string body and
string author in the constructor.
- IngestorInterface() is the abstract base class specifying the
required methods for the subclasses.
- CSVIngestor() is responsible for parsing and checking CSV files.
- DOCXIngestor() is responsible for parsing and checking DOCX files.
- PDFIngestor() is responsible for parsing and checking PDF files.
- TXTIngestor() is responsible for parsing and checking TXT files.
- Ingestor() is the final class that combines all logic. Ingestor checks what format
a given file has and then calls one of the strategy subclasses above. If you import
Quote Engine, you only need to work with Ingestor.

## Description
Quote Engine is responsible for representing quotes and for parsing quotes from
CSV, PDF, TXT and DOCX files. It also makes sure, that only such a file is being
specified in the arguments. Otherwise, will throw an error.
However, it doesn't check, if the file is formatted correct, so make sure to
write files in the following format:

body - author
body2 - author2
body3 - author3
...

## Dependencies
abc, os, csv, docx, tika, typing, subprocess

## Example Usage

```python
import quote_engine as qe
quotes = qe.Ingestor().parse("./quotes.csv")
for q in quotes:
  print(q)
```

or


```python
import quote_engine as qe
myIngestor = qe.Ingestor()
print(myIngestor.can_ingest("./quotes.doc"))  
# should print False, as only docx is supported
```
