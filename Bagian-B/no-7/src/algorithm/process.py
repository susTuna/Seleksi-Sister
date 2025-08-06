import ahocorasick
import re
import threading
import queue
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Set, Tuple
from algorithm.regex import word_to_regex_pattern

list1 = ['kontol', 'memek', 'anjing', 'babi', 'monyet']
whitelist = ['babi', 'monyet']
blacklist = ['tolol', 'jancuk']

ulist = list(set(list1) - set(whitelist) | set(blacklist)) 

class VeritasShield:
    def __init__(self, chunk_size: int = 100000, max_workers: int = None):
        self.chunk_size = chunk_size
        self.max_workers = max_workers
        self.resulsts_queue = queue.Queue()

    def build_automaton(self, patterns: List[str]) -> ahocorasick.Automaton:
        automaton = ahocorasick.Automaton()
        for idx, pattern in enumerate(patterns):
            automaton.add_word(pattern, (idx, pattern))
            common_subs = {
                'a' : '4',
                'e' : '3',
                'i' : '1',
                'o' : '0',
                's' : '5',
                't' : '7',
                'b' : '8',
                'g' : '9'
            }
            for i, char in enumerate(pattern):
                if char.lower() in common_subs:
                    variant = pattern[:i] + common_subs[char.lower()] + pattern[i+1:]
                    automaton.add_word(variant, (idx, pattern))
        automaton.make_automaton()
        return automaton
    
    def process_chunk(self, patterns: List[str], text: str, regex_filter: str = None) -> Set[Tuple[int, str]]:
        automaton = self.build_automaton(patterns)
        matches = set()

        for end_idx, (pat_idx, pattern) in automaton.iter(text):
            start_idx = end_idx - len(pattern) + 1
            if regex_filter and not re.search(regex_filter, pattern):
                continue
            matches.add((start_idx, pattern))
        for pattern in patterns:
            regex_pattern = word_to_regex_pattern(pattern)
            for match in re.finditer(regex_pattern, text, re.IGNORECASE):
                start_idx = match.start()
                matches.add((start_idx, pattern))
        return matches
    
    def find_patterns(self, patterns: List[str], text: str, regex_filter: str = None) -> Set[Tuple[int, str]]:
        if not patterns or not text:
            return []

        pattern_chunks = [patterns[i:i+self.chunk_size] 
                         for i in range(0, len(patterns), self.chunk_size)]
        all_matches = set()
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_chunk = {
                executor.submit(self.process_chunk, chunk, text, regex_filter): i
                for i, chunk in enumerate(pattern_chunks)
            }
            for future in future_to_chunk:
                chunk_matches = future.result()
                all_matches.update(chunk_matches)
        return sorted(all_matches, key=lambda x: x[0])