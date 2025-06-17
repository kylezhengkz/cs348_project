import pandas as pd
import numpy as np
import os
import sys
from typing import Optional, Union, List, Dict

from .constants.Paths import UtilsPath
from .constants.ImportLevel import ImportLevel

sys.path.insert(1, UtilsPath)

from PyUtils import DBSecrets, ColNames, TableNames, DBNames, DBTool, DBBuilder, DBCleaner, DateTimeTool


# Importer: The importer for adding data into the database
class Importer(DBTool):
    def __init__(self, secrets: DBSecrets, database: str = DBNames.Toy.value, useConnPool: bool = False):
        super().__init__(secrets, database, useConnPool = useConnPool)

    # toDateTime(data, cols, formats): Converts certain columns in the data to a datetime
    def toDateTime(self, data: pd.DataFrame, cols: List[str], formats: Optional[List[str]] = None) -> pd.DataFrame:
        if (formats is None):
            formats = DateTimeTool.StrFormats

        for col in cols:
            for format in formats:
                try:
                    data[col] = pd.to_datetime(data[col], format = format)
                except ValueError:
                    continue
                else:
                    break

        return data
    
    # fillNaN(data, vals): Fills the NaN values in certain columns of the table with the specified values
    def fillNaN(self, data: pd.DataFrame, vals: Dict[str, str]) -> pd.DataFrame:
        for col in vals:
            replaceVal = vals[col]
            if (replaceVal is None):
                data[col] = data[col].replace(np.nan, None)
                continue

            data[col] = data[col].fillna(vals[col])

        return data

    # replaceIds(data, originalIds, generatedIds, idColName): Replaces the ids in the original data with the newly generated ids
    def replaceIds(self, data: pd.DataFrame, originalIds: pd.DataFrame, generatedIds: pd.DataFrame, idColName: str) -> pd.DataFrame:
        oldIdColName = f"old_{idColName}"
        tempIdColName = f"temp_{idColName}"
        idExistsColName = f"{idColName}_exists"

        data = data.rename(columns = {idColName: oldIdColName})
        data[tempIdColName] = data[oldIdColName]
        originalIds = originalIds.rename(columns = {idColName: tempIdColName})
        originalIds = pd.concat([originalIds, generatedIds], axis = 1)
        
        data[tempIdColName] = np.where(data[idExistsColName] == 0, data[oldIdColName], None)

        originalIds[tempIdColName] = originalIds[tempIdColName].astype(str)
        data[tempIdColName] = data[tempIdColName].astype(str)

        data = pd.merge(data, originalIds, on = tempIdColName, how = "left")
        data[idColName] = data[idColName].infer_objects(copy=False)
        data[idColName] = data[idColName].fillna(value = data[oldIdColName])

        data = data.drop(columns = [tempIdColName, oldIdColName, idExistsColName])
        return data
    
    # insertAndReplaceIds(dataToInsert, insertTableName, dataNeedingReplace, idColName): Inserts the data and replaces the foreign ids of the other
    #   tables with the newly generated ids after the data insertion
    def insertAndReplaceIds(self, dataToInsert: pd.DataFrame, insertTableName: str, dataNeedingReplace: List[pd.DataFrame], idColName: str) -> Optional[Union[List[pd.DataFrame], pd.DataFrame]]:
        originalIds = dataToInsert[[idColName]]
        dataToInsert = dataToInsert.drop(idColName, axis = 1)

        generatedIds = self.insert(dataToInsert, tableName = insertTableName, returnCols = [idColName])

        if (not dataNeedingReplace):
            return

        dataNeedingReplaceLen = len(dataNeedingReplace)
        for i in range(dataNeedingReplaceLen):
            dataNeedingReplace[i] = self.replaceIds(dataNeedingReplace[i], originalIds, generatedIds, idColName)

        if (dataNeedingReplaceLen == 1):
            return dataNeedingReplace[0]
        return dataNeedingReplace
    
    # clean(isSure, cleanLevel): Cleans up a particular dataset
    def clean(self, isSure: bool = False, cleanLevel: ImportLevel = ImportLevel.Tuples):
        dbCleaner = DBCleaner(self)

        if (cleanLevel == ImportLevel.Database):
            print(f"Deleting database by the name, {self.database} ...")
            dbCleaner.deleteDB(isSure = isSure)

        elif (cleanLevel == ImportLevel.Tables):
            print(f"Deleting all tables...")
            dbCleaner.deleteAllTables(isSure = isSure)

            print(f"Deleting all functions...")
            dbCleaner.deleteAllFuncs(isSure = isSure)

        elif (cleanLevel == ImportLevel.Tuples):
            print(f"Clearing all tables...")
            dbCleaner.clearAll(isSure = isSure)

    # importData(dataFolder, buildLevel, clearLevel): Inserts all the data from a particular dataset
    def importData(self, dataFolder: str, buildLevel: ImportLevel = ImportLevel.Tuples, cleanLevel: Optional[ImportLevel] = None):
        userFile = os.path.join(dataFolder, "User.csv")
        buildingFile = os.path.join(dataFolder, "Building.csv")
        roomFile = os.path.join(dataFolder, "Room.csv")
        bookingFile = os.path.join(dataFolder, "Booking.csv")
        cancellationFile = os.path.join(dataFolder, "Cancellation.csv")

        userData = pd.read_csv(userFile)
        buildingData = pd.read_csv(buildingFile)
        roomData = pd.read_csv(roomFile)
        bookingData = pd.read_csv(bookingFile)
        cancellationData = pd.read_csv(cancellationFile)

        # clean the datatypes of the raw datasets
        buildingData = self.fillNaN(buildingData, {ColNames.BuildingName.value: "",
                                                   ColNames.BuildingName.value: "",
                                                   ColNames.BuildingAddressLine1.value: "",
                                                   ColNames.BuildingAddressLine2.value: "",
                                                   ColNames.BuildingCity.value: "",
                                                   ColNames.BuildingProvince.value: "",
                                                   ColNames.BuildingCountry.value: "",
                                                   ColNames.BuildingPostalCode.value: ""})

        bookingData = self.toDateTime(bookingData, [ColNames.BookingStartTime.value, ColNames.BookingEndTime.value, ColNames.BookingTime.value])

        dbBuilder = DBBuilder(self)

        if (cleanLevel is not None):
            self.clean(isSure = True, cleanLevel = cleanLevel)

        if (buildLevel.value >= ImportLevel.Database.value):
            print(f"Constructing the database by the name, {self.database} ...")
            dbBuilder.buildDB()

        if (buildLevel.value >= ImportLevel.Tables.value):
            print(f"Constructing all tables...")
            dbBuilder.build()

        print(f"Inserting User Data...")
        bookingData, cancellationData = self.insertAndReplaceIds(userData, TableNames.User.value, [bookingData, cancellationData], ColNames.UserId.value)

        print(f"Inserting Building Data...")
        roomData = self.insertAndReplaceIds(buildingData, TableNames.Buiding.value, [roomData], ColNames.BuildingId.value)

        print(f"Inserting Room Data...")
        bookingData = self.insertAndReplaceIds(roomData, TableNames.Room.value, [bookingData], ColNames.RoomId.value)

        print(f"Inserting Booking Data...")
        cancellationData = self.insertAndReplaceIds(bookingData, TableNames.Booking.value, [cancellationData], ColNames.BookingId.value)

        print(f"Inserting Cancellation Data...")
        self.insert(cancellationData, TableNames.Cancellation.value)
        