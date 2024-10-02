from gardentool import Converter

GITBOOK_PATH = "/Users/kimshan/Public/learn/DigitalGarden/PKM-BOOK"
NOTEBOOK_PATH = "/Users/kimshan/Public/learn/DigitalGarden/NoteBook"
# NOTEBOOK_PATH = "/Users/kimshan/Public/learn/DigitalGarden/NoteBookTEMP2"

converter = Converter()
converter.load(GITBOOK_PATH)
# converter.check(NOTEBOOK_PATH)
converter.sync(NOTEBOOK_PATH)

