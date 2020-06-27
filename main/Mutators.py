import random
import main.fuzzing_vars as fv


# class responsable to range the mutaitons, and the mutation evolution, saving the original content
class MultipleMutation:
    def __init__(self, url, mutations):
        self.url = url
        self.mutations = mutations
        self.seed = self.url
        self.fuzzed = []
        # self.container = get_shellcode()
        self.container = get_fshellcode()
        # First, use the mutators function 10 times

    # Shorter way to fuzz the url`
    def fuzz_elem(self):
        try:
            self.url = self.seed
            for _ in range(1):
                self.url = mutate(self.url)
            self.fuzzed.append(self.url)
            for i in self.container:
                cont_url = self.url
                cont_url += str(i)
                self.fuzzed.append(cont_url)
        except Exception as e:
            print(e)
        return self.fuzzed

    # Fuzz with mutators multiple times
    def fuzz_deep(self):
        for _ in range(self.mutations):
            self.fuzz_elem()
        return self.fuzzed


def get_shellcode():
    shellcode = fv.shellcode
    shellcode = [shellcode, fv.Special_Patterns, fv.Special_Sufixes,
                 fv.Special_Prefixes, fv.slashes_exploitable, fv.dots_exploitable]
    return shellcode


def mutate(s):
    """Return s with a random mutation applied"""
    mutators = [
        delete_random_character,
        insert_random_character,
        flip_random_character
    ]
    mutator = random.choice(mutators)
    return mutator(s)


def insert_random_character(s):
    """Returns s with a random character inserted"""
    if s == "":
        return s
    pos = random.randint(0, len(s))
    random_character = chr(random.randrange(32, 127))
    # print("Inserting", repr(random_character), "at", pos)
    return s[:pos] + random_character + s[pos:]


def delete_random_character(s):
    """Returns s with a random character deleted"""
    if s == "":
        return s
    pos = random.randint(0, len(s) - 1)
    # print("Deleting", repr(s[pos]), "at", pos)
    return s[:pos] + s[pos + 1:]


def flip_random_character(s):
    """Returns s with a random bit flipped in a random position"""
    if s == "":
        return s

    pos = random.randint(0, len(s) - 1)
    c = s[pos]
    bit = 1 << random.randint(0, 6)
    new_c = chr(ord(c) ^ bit)
    return s[:pos] + new_c + s[pos + 1:]


def overflow_fuzz(s):
    if s == "":
        return s


def add_long_strings(s, container):
    if s == "":
        return s
    for length in [128, 255, 256, 257, 511, 512, 513, 1023, 1024, 2048, 2049, 4095, 4096, 4097, 5000, 10000, 20000,
                   32762, 32763, 32764, 32765, 32766, 32767, 32768, 32769, 0xFFFF - 2, 0xFFFF - 1, 0xFFFF, 0xFFFF + 1,
                   0xFFFF + 2, 99999, 100000, 500000]:
        long_string = str(s * length)
        container.__append__(long_string)
    return container


def rand_string(max_length=100, char_start=32, char_range=32):
    """A string of up to `max_length` characters
       in the range [`char_start`, `char_start` + `char_range`]"""
    string_length = random.randrange(50, max_length + 1)
    out = ""
    for i in range(0, string_length):
        out += chr(random.randrange(char_start, char_start + char_range))
    return repr(out)


def get_fshellcode():
    ad = ["a", "b"]
    return ad
