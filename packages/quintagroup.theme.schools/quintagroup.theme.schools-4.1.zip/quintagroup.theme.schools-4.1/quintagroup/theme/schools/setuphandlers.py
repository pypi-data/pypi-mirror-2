def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('quintagroup.theme.schools_various.txt') is None:
        return

    # Add additional setup code here

def uninstallVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/uninstall.

    if context.readDataFile('quintagroup.theme.schools_uninstall.txt') is None:
        return

    # Add additional uninstall code here

## -*- extra stuff goes here -*-
from quintagroup.theme.schools.utils import checkIfImport, performImportToPortal

def importZEXPs(context):

    if context.readDataFile("quintagroup.theme.schools_various.txt") is None:
        return

    site = context.getSite()
    if checkIfImport():
        performImportToPortal(site)
