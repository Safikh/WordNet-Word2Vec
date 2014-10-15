import sys
from nltk.corpus import wordnet as wn
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("english")

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--verbose', '-v', action='count')
parser.add_argument('--out', '-o')
args = vars(parser.parse_args())

verbose = args['verbose'] > 0

def same_stem(one, two):
	if stemmer.stem(one) == stemmer.stem(two):
		return True
	else:
		return False


def getAntonyms(ss):
	for l in ss.lemmas():
		if len(l.antonyms()) > 0:
			return [stemmer.stem(l.name()) for l in l.antonyms()]
		return []


def intersect(a, b):
    """ return the intersection of two lists """
    return list(set(a) & set(b))


def translatePOS(pos):
	if pos == "verb":
		return wn.VERB
	return None


def getSynsets(word, pos=None):
	if pos:
		return wn.synsets(word, pos=pos)
	else:
		return wn.synsets(word)


'''
includes antonyms
'''


def synononymous(worda, wordb):
    intersection = intersect(getSynsets(worda), getSynsets(wordb))
    if verbose:
        for i in intersection:
            print i.definition()
            print i.examples()
    if len(intersection) > 0:
        return True
    return False


def antonymous(a, b):
	synsets_a = getSynsets(a)
	total_antonyms_a = []

	for a in synsets_a:
		total_antonyms_a.extend(getAntonyms(a))
	if stemmer.stem(b) in total_antonyms_a:
		return True
	return False


def hyoponomous(a, b):
    synsets_a = getSynsets(a)

    hyponyms = []
    for a in synsets_a:
        hyponyms.extend(a.hyponyms())

    synsets_b = getSynsets(b)
    return len(intersect(set(hyponyms), (set(synsets_b))))


def hypernomous(a, b):
    synsets_a = getSynsets(a)

    hypernyms = []
    for a in synsets_a:
        hypernyms.extend(a.hypernyms())

    synsets_b = getSynsets(b)
    return len(intersect(set(hypernyms), (set(synsets_b))))


def not_in_wordnet(w):
    syns = getSynsets(w)
    if len(syns) == 0:
        return True
    return False


def get_meronyms(w):
    syns = getSynsets(w)
    out = []
    for s in syns:
        out.extend([s for s in s.member_meronyms()])
        out.extend([s for s in s.substance_meronyms()])
        out.extend([s for s in s.part_meronyms()])
    return set(out)


def get_holonyms(w):
    syns = getSynsets(w)
    out = []
    for s in syns:
        out.extend([s for s in s.member_holonyms()])
        out.extend([s for s in s.substance_holonyms()])
        out.extend([s for s in s.part_holonyms()])
    return set(out)


def meronymous(a, b):
    syn_a = getSynsets(a)
    syn_b = get_meronyms(b)
    intersection = intersect(syn_a, syn_b)
    if len(intersection) > 0:
        return True
    return False


def holonymous(a, b):
    syn_a = getSynsets(a)
    syn_b = get_holonyms(b)
    intersection = intersect(syn_a, syn_b)
    if len(intersection) > 0:
        return True
    return False
