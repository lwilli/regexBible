import json
import re
import copy

"""
    Parses JSON Bibles and searches them with regex.

    Verse dictionaries look like:
        {
            "chapter":1,
            "verse":1,
            "text":"In the beginning God created the heaven and the earth.",
            "translation_id":"KJV",
            "book_id":"Gen",
            "book_name":"Genesis"
         }

     A JSON Bible should be an ordered list of the above.
"""


BIBLE_RESOURCES_DIR = "bibles"
ASV = "asv.json"
KJV = "kjv.json"


def parse_json_bible(filename):
    with open(filename, "r") as bibleraw:
        return json.loads(bibleraw.read())


KJV_JSON = parse_json_bible(BIBLE_RESOURCES_DIR + "/" + KJV)
ASV_JSON = parse_json_bible(BIBLE_RESOURCES_DIR + "/" + ASV)


def get_reference_text(verseDict):
    return verseDict["book_name"] + " " + str(verseDict["chapter"]) + ":" + str(verseDict["verse"])


def regex_search_bibles(versionsToSearch, searchPattern):
    """
    Returns the matching verses from the given Bible versions that match the regex search

    :param versionsToSearch: A list of string filenames that represent the versions of the Bible to search
    :param searchPattern: A regex string to search for matching verses with
    :return: A list of matching verse dictionaries (see above for structure) including the re.Match object
            as the value for the "match" entry in the dict
    """
    results = []

    print("Searching '" + searchPattern + "' in " + ", ".join(versionsToSearch))

    for version in versionsToSearch:
        bibleToSearch = None
        strippedLoweredVersion = version.lower().strip()
        if strippedLoweredVersion == "kjv":
            bibleToSearch = KJV_JSON
        elif strippedLoweredVersion == "asv":
            bibleToSearch = ASV_JSON

        for verseDict in bibleToSearch:
            verseMatch = re.search(searchPattern, verseDict["text"])
            if verseMatch:
                print("Found match: " + get_reference_text(verseDict))
                newResult = copy.deepcopy(verseDict)
                newResult["match"] = verseMatch
                newResult["reference"] = get_reference_text(verseDict)
                results.append(newResult)

    return results