#coding=utf-8

def split_words(line):
    words = []
    buffer = ""
    for c in line:
        if c.isalpha():
            buffer += c.lower()
        else:
            if len(buffer):
                words.append(buffer)
                buffer = ""
    if len(buffer):
        words.append(buffer)
    return words


def read_book(filename):
    words = {} #word, count
    fin = open(filename)
    for line in fin.readlines():
        for word in split_words(line):
            if not words.has_key(word):
                words[word] = 0
            words[word] += 1

    res = []

    #for word in sorted(words.keys(), key = lambda r:words[r], reverse = True):
    #    res.append(word)
    for word in words.keys():
        res.append(word)
    return res

def get_file_word(filename):
    res = []
    fin = open(filename)
    for line in fin.readlines():
        if line[-1] == '\n':
            line = line[:-1]
        if line[-1] == '\r':
            line = line[:-1]
        res.append(line)
    fin.close()
    return res

def get_know_word():
    know = get_file_word("know.txt")
    return know
def get_ouch_word():
    ouch = get_file_word("ouch.txt")
    return ouch
