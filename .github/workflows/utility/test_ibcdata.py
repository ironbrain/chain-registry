import re
import json
from os import getcwd, listdir
from os.path import isfile, join

import pytest

mypath = join(getcwd(),"_IBC")
fileList = [f for f in listdir(mypath) if isfile(join(mypath, f))]

@pytest.mark.parametrize("input", fileList)
def test_fileName(input):
    # validates that the json file name has two "strings" separated by a hyphen (-) and ends with ".json"
    pattern = re.compile(r'.*-.*.json$')
    result = re.match(pattern, input)
    assert result

@pytest.mark.parametrize("input", fileList)
def test_alphabeticalOrder(input):
    # validates that chain_1 and chain_2 in file name are in alphabetical order
    pattern = re.compile(r'(.*)-(.*).json$')
    m = pattern.match(input)
    toSort = [(m.group(1)), (m.group(2))]
    toSort.sort(key=str.lower)
    assert (m.group(1) == toSort[0]) and (m.group(2) == toSort[1])

@pytest.mark.parametrize("input", fileList)
def test_chainNameMatchFileName(input):
    # validates that the chain-name for chain-1 and chain-2 inside the json file match the order used in the file name.
    pattern = re.compile(r'(.*)-(.*).json$')
    m = pattern.match(input)
    fileName_chain1 = m.group(1).lower()
    fileName_chain2 = m.group(2).lower()
    with open(join(mypath,input), "r") as read_file:
        json_file = json.load(read_file)
        chain_1 = str(json_file["chain-1"]["chain-name"]).lower()
        chain_2 = str(json_file["chain-2"]["chain-name"]).lower()
    assert fileName_chain1 == chain_1 and fileName_chain2 == chain_2