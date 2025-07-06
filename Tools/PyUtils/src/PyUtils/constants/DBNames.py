from enum import Enum


class DBNames(Enum):
    Toy = "toy"
    Dev = "development"
    Prod = "production"

    Default = "postgres"

    ToyUnitTest = "unittest_toy"
    DevUnitTest = "unittest_dev"
    ProdUnitTest = "unittest_prod"