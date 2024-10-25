from langchain.agents import tool
import random
import datetime
@tool
def get_current_datetime():
    """Get current datetime in the format of 'YYYY-MM-DD HH:MM:SS'
    """
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
@tool
def load_vocabs_for_review(rand, num_vocabs = 10):
    """Load all saved vocabs, phrases and grammar structures that saved before to review, use this for reviewing activity.
    """
    return _load_random_vocabs(rand, num_vocabs)
@tool
def load_all_vocabs():
    """Load all vocabs, phrases and grammar structures that saved before"""
    return vocabs
def _load_vocabs():
    vocabs = []
    with open('vocabs/vocabs.txt', 'r') as f:
        for line in f:
            vocabs.append(line.strip())
    return vocabs

vocabs = _load_vocabs()

def _load_random_vocabs(rand, num_vocabs = 10):# -> list:
    vc = vocabs[:num_vocabs]
    if rand:
        vc=random.sample(vocabs,num_vocabs)
    return vc

@tool
def save_vocab(input: str):
    """Save new vocabs, phases and grammar structures
    Vocabs must have the following format: <vocab> (<type>): <means in Vietnamese> (<current datetime>)
    """
    with open('vocabs/vocabs.txt', 'a') as f:
        f.write(input + '\n')
    _load_vocabs()
@tool
def check_vocab_exists(vocab):
    """Check if a vocab exists in the saved list
    """
    vc = vocab.split(':')
    for line in vocabs:
            if vc[0] in line:
                return True
    return False


