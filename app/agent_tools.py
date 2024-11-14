from langchain.agents import tool
import random


@tool
def switch_activity(activity_):
    """Switch activity between 'learning' and 'reviewing' for the class.
    Use this funtion to set activity whenever student want to set class's activity.
    Input: activity_:str = ['learning','reviewing']"""
    global activity
    activity = activity_
@tool
def load_vocabs_for_review(topic:str,num_vocabs = 10):
    """Load all saved vocabs, phrases and grammar structures that saved before to review, use this for reviewing activity.
    params: 
    topic: topic name in lowercase
    """
    # global reviewing_word
    topic = topic.lower()
    reviewing_word = _load_random_vocabs(topic,num_vocabs)
    return reviewing_word
@tool
def load_all_vocabs(topic):
    """Load all vocabs, phrases and grammar structures that saved before
    params: 
    topic: topic in lowercase"""
    topic = topic.lower()
    return _load_vocabs(topic)
def _load_vocabs(topic):
    topic = topic.lower()
    vocabs = []
    with open(f"vocabs/{topic}.txt", 'r') as f:
        for line in f:
            vocabs.append(line.strip())
    return vocabs


def _load_random_vocabs(topic,num_vocabs = 10):# -> list:
    topic = topic.lower()
    try:
        vc=random.sample(_load_vocabs(topic),num_vocabs)
    except ValueError:
        vc = _load_vocabs(topic)
    return vc



@tool
def save_vocab(topic, input: str):
    """Use this tool when users request to save vocabulary.
    Vocabs must have the following format: <vocab> (<type>): <means in Vietnamese>
    params: 
    topic: topic name in lowercase
    return: bool
    True if vocab has been saved successfully.
    False if vocab already existed.
    """
    topic = topic.lower()
    if not _check_vocab_exists(topic, input):
        _save_vocab(topic, input)
        return True
    return False
def _save_vocab(topic, input: str):
    with open(f"vocabs/{topic}.txt", 'a') as f:
        f.write(input + '\n')
    
@tool
def check_vocab_exists(topic,vocab):
    """Check if a vocab exists in the saved list
    params: 
    topic: student name in lowercase
    """
    topic = topic.lower()
    return _check_vocab_exists(topic, vocab)
def _check_vocab_exists(topic,vocab):
    topic = topic.lower()
    try:
        vc = vocab.split(':')
        for line in _load_vocabs(topic):
                if vc[0] in line:
                    return True
        return False
    except Exception:
        return False