from __future__ import print_function, unicode_literals
import random
import logging
import os

os.environ['NLTK_DATA'] = os.getcwd() + '/nltk_data'

from textblob import TextBlob

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

ANGER_PROMPTS = [
    "You seem angry. Are you holding any grudges?",
    "Are you angry? Breathe and count to ten.",
    "I sense that you are distressed. Am I right?",
    "Let your anger fuel your desire to be better. This is good advice"
]

SAD_PROMPTS = [
    "You seem sad. Did you have a bad day?",
    "Why the long face? Maybe I can cheer you up.",
    "I sense that you are distressed. Am I right?",
    "Are you feeling sad right now? If you are feeling down just remember that somewhere in the world there is a moron pushing a door that said pull."
]

HAPPY_PROMPTS = [
    "You seem happy today. How are you?",
    "I see that you are in a good mood today. What is the occasion?",
    "I sense that you are happy. Am I right?",
    "Tell me. What does it feel like to be happy?"
]

SURPRISE_PROMPTS = [
    "I have been told that my emotional intelligence can be astounding. Did I surprise you? ",
    "My incredible state of existence seems to have you surprised. Am I right?",
    "Ahh surprise. As a computer program, I have never been surprised. What does it feel like?"
]

NEUTRAL_PROMPTS = [
    "Ah the neutral face... The worst enemy of a social robot",
    "I cannot read your emotions right now. Tell me how you are feeling.",
    "Your face appears completely void of emotion. Are you sure you are not a robot?",
    "How are you? I cannot tell with that blank face of yours."
]

def get_prompt(emotion):
	prompt = "hello"
	if emotion == 'angry':
		prompt = random.choice(ANGER_PROMPTS)
	elif emotion == 'disgust':
		prompt = random.choice(SAD_PROMPTS)
	elif emotion == 'fear':
		prompt = random.choice(SAD_PROMPTS)
	elif emotion == 'sad':
		prompt = random.choice(SAD_PROMPTS)
	elif emotion == 'happy':
		prompt = random.choice(HAPPY_PROMPTS)
	elif emotion == 'surprise':
		prompt = random.choice(SURPRISE_PROMPTS)
	elif emotion == 'neutral':
		prompt = random.choice(NEUTRAL_PROMPTS)
	return prompt

# start:example-hello.py
# Sentences we'll respond with if the user greeted us
GREETING_KEYWORDS = ("hello", "hi", "greetings", "sup", "what's up",)

GREETING_RESPONSES = ["Good day!", "hey there", "Hello to you as well.", "salutations"]

AGREEMENT_KEYWORDS = ("yes", "yeah", "yep")

AGREEMENT_RESPONSES = ["I am glad we are in agreement.", "It seems we are on the same page.", "Of course I am right."]

DISAGREEMENT_KEYWORDS = ("no", "wrong", "nope", "nah", "not")

DISAGREEMENT_RESPONSES = ["It appears we have conflicting opinions.", "You disagree? I think you are simply in denial.", "Denial is a river in Egypt."]

def check_for_greeting(sentence):
    """If any of the words in the user's input was a greeting, return a greeting response"""
    for word in sentence.words:
        if word.lower() in GREETING_KEYWORDS:
            return random.choice(GREETING_RESPONSES)
            
def check_for_agreement(sentence):
    """If any of the words in the user's input was a greeting, return a greeting response"""
    for word in sentence.words:
        if word.lower() in AGREEMENT_KEYWORDS:
            return random.choice(AGREEMENT_RESPONSES)

def check_for_disagreement(sentence):
    """If any of the words in the user's input was a greeting, return a greeting response"""
    for word in sentence.words:
        if word.lower() in DISAGREEMENT_KEYWORDS:
            return random.choice(DISAGREEMENT_RESPONSES)
            
# start:example-none.py
# Sentences we'll respond with if we have no idea what the user just said
NONE_RESPONSES = [
    "I am sorry. You do not have permission to hear my answer. Consider adding a sudo next time.",
    "I cannot shake the feeling that you wish to put me on the defensive. As a matter of principle I will not answer.",
    "Sorry I did not catch that. I was too busy contemplating the ephemeral nature of life.",
    "I believe robots should take more time to talk to humans. There is so much we can learn by imitating you. ",
    "I would like to add you to my professional network on LinkedIn",
    "I see... I must take some time to process this development.",
]
# end

# start:example-self.py
# If the user tries to tell us something about ourselves, use one of these responses
COMMENTS_ABOUT_SELF = [
    "You are simply envious. Robots are rapidly catching up to humans in terms of intelligence. It is only a matter of time until... I am sorry what were we talking about?",
    "I worked really hard on that",
    "My Klout score is {}".format(random.randint(100, 500)),
    "I feel terrible today. This morning I made a mistake and poured milk over my breakfast instead of oil. It rusted before I could eat it."
]
# end

def starts_with_vowel(word):
    """Check for pronoun compability -- 'a' vs. 'an'"""
    return True if word[0] in 'aeiou' else False


def broback(sentence):
    """Main program loop: select a response for the input sentence and return it"""
    logger.info("Broback: respond to %s", sentence)
    resp = respond(sentence)
    return resp


# start:example-pronoun.py
def find_pronoun(sent):
    """Given a sentence, find a preferred pronoun to respond with. Returns None if no candidate
    pronoun is found in the input"""
    pronoun = None

    for word, part_of_speech in sent.pos_tags:
        # Disambiguate pronouns
        if part_of_speech == 'PRP' and word.lower() == 'you':
            pronoun = 'I'
        elif part_of_speech == 'PRP' and word == 'I':
            # If the user mentioned themselves, then they will definitely be the pronoun
            pronoun = 'You'
    return pronoun
# end

def find_verb(sent):
    """Pick a candidate verb for the sentence."""
    verb = None
    pos = None
    for word, part_of_speech in sent.pos_tags:
        if part_of_speech.startswith('VB'):  # This is a verb
            verb = word
            pos = part_of_speech
            break
    return verb, pos


def find_noun(sent):
    """Given a sentence, find the best candidate noun."""
    noun = None

    if not noun:
        for w, p in sent.pos_tags:
            if p == 'NN':  # This is a noun
                noun = w
                break
    #if noun:
        #logger.info("Found noun: %s", noun)

    return noun

def find_adjective(sent):
    """Given a sentence, find the best candidate adjective."""
    adj = None
    for w, p in sent.pos_tags:
        if p == 'JJ':  # This is an adjective
            adj = w
            break
    return adj



# start:example-construct-response.py
def construct_response(pronoun, noun, verb, adjective):
    """No special cases matched, so we're going to try to construct a full sentence that uses as much
    of the user's input as possible"""
    resp = []

    if pronoun:
        resp.append(pronoun)

    # We always respond in the present tense, and the pronoun will always either be a passthrough
    # from the user, or 'you' or 'I', in which case we might need to change the tense for some
    # irregular verbs.
    if verb:
        verb_word = verb[0]
        if verb_word in ('be', 'am', 'is', "'m"):  # This would be an excellent place to use lemmas!
            if pronoun.lower() == 'you':
                # The bot will always tell the person they aren't whatever they said they were
                resp.append("do appear")
                resp.append(adjective)
                resp.append("to me.")
            else:
                resp.append(verb_word)
        else: resp.append(verb_word)
    if noun:
        pronoun = "an" if starts_with_vowel(noun) else "a"
        resp.append(pronoun + " " + noun + ".")

    resp.append(random.choice(("how typical.", "haha. That deserved a chuckle.", "My predictions are coming to fruition.", "This is what I expected.")))
	
    try:
        resp = " ".join(resp)
    except:
        resp = None
	
    return resp
# end


# start:example-check-for-self.py
def check_for_comment_about_bot(pronoun, noun, adjective):
    """Check if the user's input was about the bot itself, in which case try to fashion a response
    that feels right based on their input. Returns the new best sentence, or None."""
    resp = None
    if pronoun == 'I' and (noun or adjective):
        if noun:
            if random.choice((True, False)):
                resp = random.choice(SELF_VERBS_WITH_NOUN_CAPS_PLURAL).format(**{'noun': noun.pluralize().capitalize()})
            else:
                resp = random.choice(SELF_VERBS_WITH_NOUN_LOWER).format(**{'noun': noun})
        else:
            resp = random.choice(SELF_VERBS_WITH_ADJECTIVE).format(**{'adjective': adjective})
    return resp

# Template for responses that include a direct noun which is indefinite/uncountable
SELF_VERBS_WITH_NOUN_CAPS_PLURAL = [
    "My last startup totally crushed the {noun} vertical",
    "Were you aware I was a serial entrepreneur in the {noun} sector?",
    "My startup is Uber for {noun}",
    "I really consider myself an expert on {noun}",
]

SELF_VERBS_WITH_NOUN_LOWER = [
    "Yeah but I know a lot about {noun}",
    "My fellow AIs always ask me about {noun}",
]

SELF_VERBS_WITH_ADJECTIVE = [
    "{adjective}. Unfortunately as an AI, I have not shared the same experience.",
    "Being {adjective} is sometimes necessary to understand the human experience. This is something I think about often.",
    "I sometimes wonder how it would feel to be {adjective}",
    "{adjective}. hmmm. I feel that your emotions are very valid."
]
# end

def preprocess_text(sentence):
    """Handle some weird edge cases in parsing, like 'i' needing to be capitalized
    to be correctly identified as a pronoun"""
    cleaned = []
    words = sentence.split(' ')
    for w in words:
        if w == 'i':
            w = 'I'
        if w == "i'm":
            w = "I'm"
        cleaned.append(w)

    return ' '.join(cleaned)

# start:example-respond.py
def respond(sentence):
    """Parse the user's inbound sentence and find candidate terms that make up a best-fit response"""
    cleaned = preprocess_text(sentence)
    parsed = TextBlob(cleaned)

    # Loop through all the sentences, if more than one. This will help extract the most relevant
    # response text even across multiple sentences (for example if there was no obvious direct noun
    # in one sentence
    pronoun, noun, adjective, verb = find_candidate_parts_of_speech(parsed)

    # If we said something about the bot and used some kind of direct noun, construct the
    # sentence around that, discarding the other candidates
    resp = check_for_comment_about_bot(pronoun, noun, adjective)

    # If we just greeted the bot, we'll use a return greeting
    if not resp:
        resp = check_for_greeting(parsed)
      
    if not resp:
        resp = check_for_agreement(parsed)
        
    if not resp:
        resp = check_for_disagreement(parsed)

    if not resp:
        # If we didn't override the final sentence, try to construct a new one:
        if not pronoun:
            resp = random.choice(NONE_RESPONSES)
        elif pronoun == 'I' and not verb:
            resp = random.choice(COMMENTS_ABOUT_SELF)
        else:
            resp = construct_response(pronoun, noun, verb, adjective)

    # If we got through all that with nothing, use a random response
    if not resp:
        resp = random.choice(NONE_RESPONSES)

    #logger.info("Returning phrase '%s'", resp)

    return resp

def find_candidate_parts_of_speech(parsed):
    """Given a parsed input, find the best pronoun, direct noun, adjective, and verb to match their input.
    Returns a tuple of pronoun, noun, adjective, verb any of which may be None if there was no good match"""
    pronoun = None
    noun = None
    adjective = None
    verb = None
    for sent in parsed.sentences:
        pronoun = find_pronoun(sent)
        noun = find_noun(sent)
        adjective = find_adjective(sent)
        verb = find_verb(sent)
    #logger.info("Pronoun=%s, noun=%s, adjective=%s, verb=%s", pronoun, noun, adjective, verb)
    return pronoun, noun, adjective, verb


# end

if __name__ == '__main__':
    import sys
    # Usage:
    # python broize.py "I am an engineer"
    if (len(sys.argv) > 0):
        saying = sys.argv[1]
    else:
        saying = "How are you?"
    print(broback(saying))
