import os
from enum import Enum


FileDir = os.path.dirname(__file__)


class Paths(Enum):
    ProjectFolder = os.path.abspath(os.path.join(FileDir, "..", "..", "..", "..", ".."))

    DataFolder = os.path.abspath(os.path.join(ProjectFolder, "Data"))
    ToyDatasetFolder = os.path.abspath(os.path.join(DataFolder, "Toy Dataset"))
    SampleDatasetFolder = os.path.abspath(os.path.join(DataFolder, "Sample Dataset"))
    ProdDatasetFolder = os.path.abspath(os.path.join(DataFolder, "Production Dataset"))

    SQLQueriesFolder = os.path.abspath(os.path.join(ProjectFolder, "SQL Queries"))
    SQLTableCreationFolder = os.path.abspath(os.path.join(SQLQueriesFolder, "Table Creation"))
    SQLDBCreationFolder = os.path.abspath(os.path.join(SQLQueriesFolder, "Database Creation"))
    SQLTriggerCreationFolder = os.path.abspath(os.path.join(SQLQueriesFolder, "Trigger Creation"))

    SQLFeaturesFolder = os.path.abspath(os.path.join(SQLQueriesFolder, "Features"))
    PyUtilsFolder = os.path.abspath(os.path.join(FileDir, "..", ".."))
    DataImporterFolder = os.path.abspath(os.path.join(ProjectFolder, "Tools", "DataImporter", "src"))

    BackEndFolder = os.path.abspath(os.path.join(ProjectFolder, "Backend"))
    FrontEndFolder = os.path.abspath(os.path.join(ProjectFolder, "Frontend"))
    DataPopulatorFolder = os.path.abspath(os.path.join(ProjectFolder, "Tools", "DataPopulator"))

    UnitTesterFolder = os.path.abspath(os.path.join(ProjectFolder, "Tools", "UnitTester"))
    UnitTestsFolder = os.path.abspath(os.path.join(UnitTesterFolder, "UnitTests"))