import re
from os.path import exists
import argparse

class Kebabify:
    def __init__(self):
        self.patterns = []
    
    def addPattern(self, pattern):
        '''Adds a regex pattern that will be used on the file'''
        self.patterns.append(pattern)

    def getFileContent(self, theFile):
        '''Returns the file content as a string'''
        if not exists(theFile):
            raise Exception('''File doesn't exist''')
        with open(theFile) as file:
            return file.read()
        
    def getMatches(self, text):
        '''Returns a list of all matches to the regex patterns'''
        allMatches = []
        for pattern in self.patterns:
            matches = re.findall(pattern, text)
            allMatches.extend(matches)
        return allMatches
    
    def kebabReplacements(self, lst):
        '''Converts the list to kebabified list'''
        pattern = r'(_|(?<=[a-z])(?=[A-Z]))'
        lst = lst.copy()
        for i in range(len(lst)):
            lst[i] = re.sub(pattern, '-', lst[i])
        return lst
        
    def kebab(self, theFile):
        '''Kebabifies the file'''
        text = self.getFileContent(theFile)
        allMatches = self.getMatches(text)
        allMatchesConverted = self.kebabReplacements(allMatches)

        for i in range(len(allMatchesConverted)):
            text = text.replace(allMatches[i], allMatchesConverted[i], -1)
        return text



def main():

    parser = argparse.ArgumentParser(description='Kebabifiies every variable.')
    parser.add_argument('-f', '--file', help='input file')

    args = parser.parse_args()

    if args.file is None:
        raise Exception('''There is no -f argument''')

    kebab = Kebabify()
    kebab.addPattern(r'(?:def\s+|\b)(?:class\s+|\b)([a-z]+(?:[A-Z][a-z]*)+)(?=\s*=)') # camelCase match
    kebab.addPattern(r'(?:def\s+|\b)(?:class\s+|\b)([A-Z][a-z]*(?:[A-Z][a-z]*)+)(?=\s*=|\b)') # PascalCase match
    kebab.addPattern(r'(?:def\s+|\b)(?:class\s+|\b)([a-z]+(?:_[a-z]+)+)(?=\s*=|\b)') # snake_case match
    
    kebab.kebab(args.file)



if __name__ == '__main__':
    main()
