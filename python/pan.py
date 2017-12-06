# Credits to: https://raw.githubusercontent.com/webis-de/savoy13-authorship-attribution/master/pan.py?token=AVfOvTqGcG9_-XTWbTq1SMnuw_-OfUWaks5aKUj1wA%3D%3D


from bs4 import BeautifulSoup
from collections import Counter
from heapq import nlargest
import re


class PAN_training:
    def cleanup(self, path):
        with open(path, 'r') as infile:
            data = re.sub(r'<(?!\/?(text|training|author|body|NAME))', '', infile.read())
        with open(path, 'w') as outfile:
            outfile.write(data)

    def __init__(self, xml_location):

        self.cleanup(xml_location)

        self.data = {}
        with open(xml_location) as fp:
            xml_soup = BeautifulSoup(fp, "xml")
        root = xml_soup.training
        for child in root.findAll('text'):
            author = child.find('author').get('id')
            text = child.body.text.lower() \
                .replace("don't", "do not") \
                .replace("doesn't", "does not") \
                .replace("didn't", "did not") \
                .replace("can't", "cannot") \
                .replace("mustn't", "must not") \
                .replace("won't", "will not") \
                .replace("shouldn't", "should not") \
                .replace("couldn't", "could not") \
                .replace("wouldn't", "would not") \
                .replace("haven't", "have not") \
                .replace("hasn't", "has not") \
                .replace("wasn't", "was not") \
                .replace("'ll", " will")

            wordlist = []

            pointer = 0
            for i, c in enumerate(text):

                if not (65 <= ord(c) <= 90 or 97 <= ord(c) <= 122):
                    if i - pointer >= 1:
                        wordlist.append(text[pointer:i])
                    if c in ".,:;-!?'":
                        wordlist.append(c)
                    pointer = i + 1
            # todocount=child.get("file")
            self.data[author] = self.data.get(author, []) + [(wordlist, Counter(wordlist))]

            # print(todocount)

    def reduce_author_set(self, n=20):  # TODO move to superclass
        self.data = dict(nlargest(n, self.data.items(), key=lambda a: len(a[1])))

    def total_freqs(self):
        return sum((self.author_freqs(a) for a in self.data), Counter())

    def total(self):
        return sum(self.data.values(), [])

    def author_freqs(self, author):
        return sum((a[1] for a in self.data[author]), Counter())


if __name__ == "__main__":
    p = PAN_training("raw/LargeTrain.xml")
    p.reduce_author_set(20)
    print("Number of articles by the", 20, "most active authors:", sum(len(p.data[v]) for v in p.data))
    print(sum(p.total_freqs().values()))
    print(p.total_freqs().most_common(200))
    p.total()