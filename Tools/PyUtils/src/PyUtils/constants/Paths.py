import os
from enum import Enum


FileDir = os.path.dirname(__file__)


class Paths(Enum):
    ProjectFolder = os.path.abspath(os.path.join(FileDir, "..", "..", "..", "..", ".."))
    SQLQueriesFolder = os.path.abspath(os.path.join(ProjectFolder, "SQL Queries"))
    SQLCreationQueriesFolder = os.path.abspath(os.path.join(SQLQueriesFolder, "Creation"))
    PyUtilsFolder = os.path.abspath(os.path.join(FileDir, "..", ".."))
    DataImporterFolder = os.path.abspath(os.path.join(ProjectFolder, "Tool", "DataImporter", "src"))