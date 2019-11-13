from abc import ABC, abstractmethod  # Abstract base class
import os
import csv
from docx import Document
from tika import parser
from typing import Callable, Iterator, Union, Optional, List
import subprocess
import pandas as pd

acceptedFileTypes = [".csv", ".docx", ".pdf", ".txt"]

class QuoteModel():
    """ Encapsulates body and author of a quote """

    def __init__(self, body, author):
        self.author = author
        self.body = body

    def __str__(self):
        return self.body+' - '+self.author


class IngestorInterface(ABC):
    """ Handle file ingesting into meme generator """

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """ Return if path to file can be ingested """
        filename, file_extension = os.path.splitext(path)
        if file_extension in acceptedFileTypes:
            return True
        else:
            return False

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """ Return List of QuoteModels of ingested file """
        pass


class CSVIngestor(IngestorInterface):
    """ Handle CSV file parsing """

    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise TypeError("Cant ingest specified file. Should be .csv")
        quotes = []
        df = pd.read_csv(path)
        for index, row in df.iterrows():
            a = row["author"]
            b = row["body"]
            quotes.append(QuoteModel(b, a))
        return quotes


class DOCXIngestor(IngestorInterface):
    """ Handle DOCX file parsing """

    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise TypeError("Cant ingest specified file. Should be .docx")
        quotes = []
        doc = Document(path)
        for para in doc.paragraphs:
            if not para.text.strip():  # empty paragraph
                continue
            a = para.text.split('-')[1].strip()
            b = para.text.split('-')[0].strip()
            quotes.append(QuoteModel(b, a))
        return quotes


class PDFIngestor(IngestorInterface):
    """ Handle PDF file parsing """

    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise TypeError("Cant ingest specified file. Should be .pdf")
        quotes = []
        tmp_path = "./_tmp.txt"
        subprocess.call(['pdftotext', path, tmp_path])
        quotes = Ingestor().parse(tmp_path)
        os.remove(tmp_path)
        return quotes


class TXTIngestor(IngestorInterface):
    """ Handle TXT file parsing """

    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise TypeError("Cant ingest specified file. Should be .txt")
        quotes = []
        f = open(path, "r")
        for line in f:
            if not line.strip():  # empty line
                continue
            a = line.split("-")[1].strip()
            b = line.split("-")[0].strip()
            quotes.append(QuoteModel(b, a))
        f.close()
        return quotes


class Ingestor(IngestorInterface):
    """ Final Ingestor class which handles all file types """

    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise TypeError("""Not a valid file type.
            Supported file types are %s""" % acceptedFileTypes)
        filename, file_extension = os.path.splitext(path)
        if file_extension == '.csv':
            return CSVIngestor.parse(cls, path)
        elif file_extension == '.docx':
            return DOCXIngestor.parse(cls, path)
        elif file_extension == '.pdf':
            return PDFIngestor.parse(cls, path)
        elif file_extension == '.txt':
            return TXTIngestor.parse(cls, path)
        else:
            raise TypeError("""Not a valid file type.
            Supported file types are %s""" % acceptedFileTypes)
