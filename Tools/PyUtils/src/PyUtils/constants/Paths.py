import os
from enum import Enum


FileDir = os.path.dirname(__file__)


class Paths(Enum):
    ProjectFolder = os.path.abspath(os.path.join(FileDir, "..", "..", "..", "..", ".."))
    SQLQueriesFolder = os.path.abspath(os.path.join(ProjectFolder, "SQL Queries"))
    SQLTableCreationFolder = os.path.abspath(os.path.join(SQLQueriesFolder, "Table Creation"))
    SQLDBCreationFolder = os.path.abspath(os.path.join(SQLQueriesFolder, "Database Creation"))
    SQLTriggerCreationFolder = os.path.abspath(os.path.join(SQLQueriesFolder, "Trigger Creation"))
    PyUtilsFolder = os.path.abspath(os.path.join(FileDir, "..", ".."))
    DataImporterFolder = os.path.abspath(os.path.join(ProjectFolder, "Tool", "DataImporter", "src"))