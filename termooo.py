import re
import heapq

class TermoooGame:
    def __init__(self, word: str) -> None:
        self._word = word.lower()
        self._won = False
        self._max_guesses = 6
        self._guesses = []

    def play(self) -> None:
        self.print()
        while not self._won and len(self._guesses) < self._max_guesses:
            word = input("Guess: ")
            self.guess(word)
            self.print()
        if self._won:
            print("You won!")
        else:
            print("You lost!")

    def guess(self, word: str) -> str:
        if len(word) != len(self._word):
            print("Wrong length, try again")
            return None

        word = word.lower()
        output = ""
        for i, l in enumerate(word):
            if l == self._word[i]:
                output += l.upper()
            elif l in self._word:
                output += l
            else:
                output += '-'
        self._guesses.append(output)

        if word == self._word:
            self._won = True

        return output
        
    def print(self) -> None:
        for i in range(self._max_guesses):
            if i < len(self._guesses):
                print(" ".join(self._guesses[i]))
            else:
                print(" ".join(['_' for l in range(len(self._word))]))



class TermoooSolver:
    """ TermooSolver solves term.ooo
    TODO:
    How to represent current known information:
        * Known positions of known letters
        * Known unposition of known letters
        * Known unletters
    """
    def __init__(self, wlen: int, dictionary: str) -> None:
        # Length of the word to be guessed
        self._wlen = wlen       
        # Current Working Guess
        self._cwg = "".join(['-' for l in range(self._wlen)])      
        # Letters that are in the word whose location is unknown
        self._contains = set()  
        # Letters that are not in the word
        self._excludes = set()
        # Heap to organize dictionary
        # NOTE: heapq provided only a minheap implementation
        # The maxheap will be implemented by using negative numbers
        self._h = []
        with open(dictionary) as d:
            for word in d.readlines():
                word = word.strip().lower()
                if len(word) == self._wlen:
                    heapq.heappush(self._h, [0, word])
            print(self._h)

    def guess(self) -> str:
        """Produces a guess based on the current state
        Simply returns a copy of heap[0]"""
        return self._h[0]

    def update(self, update: str) -> None:
        """Updates current state based on the information
        gained from the past guess. Assumes past guess is
        heap[0] and pops it from the heap"""
        pguess = heapq.heappop(self._h)
        nwg = ""
        for i, l in enumerate(update):
            if l.isupper():
                nwg += l
            elif l.islower():
                self._contains.add(l)
                nwg += '-'
            else:
                self._excludes.add(pguess[i])
        to_pop = []
        for i, e in enumerate(self._h):
            pass
        heapq.heapify(self._h)

    def _create_regex(self) -> str:
        """Creates a regex string from current state"""
        raise NotImplemented

    def _cmp_word(self, word: str) -> int:
        sum = 0
        for i, l in enumerate(word):
            if l == self._cwg[i]:
                sum += 1
            elif l in self._contains:
                sum += 1
        return -sum


def findSmallestCoveringSubset(words: list, alpha: dict) -> list:
    def cuniq(w, a):
        return sum([1 for i, l in enumerate(w) if a[l] and l not in w[:i]])
    subset = []
    words = [[cuniq(w, alpha), w] for w in words if cuniq(w, alpha) > 0]
    while True in alpha.values() and len(words) > 0:
        word = max(words)[1]
        subset.append(word)
        for l in word: alpha[l] = False
        words = [[cuniq(w[1], alpha), w[1]] for w in words if cuniq(w[1], alpha) > 0]
    return subset

with open('br-sem-acentos.txt') as f:
    words = [l.strip().lower() for l in f if len(l.strip()) == 5]
    alphabet = {l: True for l in 'abcdefghijklmnopqrstuvwxyz'}
    subset = findSmallestCoveringSubset(words, alphabet)
    print(subset)


# newgame = TermoooGame("amar")
# newgame.play()
# print(newgame.guess("caar"))
# solver = termooosolver(5, "br-sem-acentos.txt")