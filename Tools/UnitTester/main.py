import UnitTester as UT
import UnitTests as UTests


def main():
    unitTester = UT.UnitTester.create()

    unitTester.addTestSuite(UTests.R6Test)
    unitTester.addTestSuite(UTests.R7Test)
    unitTester.addTestSuite(UTests.R8Test)

    unitTester.run()


if __name__ == "__main__":
    main()
