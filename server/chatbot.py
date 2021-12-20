'''
This module implements the core logic of the chatbot by generating responses
based on user input.
'''

import re

def message_probability(user_message, recognised_words, required_words=[]):
    message_certainty = 0
    has_required_words = False

    # Counts how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculates the percent of recognised words in a user message
    percentage = float(message_certainty)

    # Checks that the required words are in the string
    for word in required_words:
        if word in user_message:
            has_required_words = True
            break

    # Must either have the required words, or be a single response
    if has_required_words:
      return int(percentage * 100)
    else:
      return 0


def check_all_messages(message):
    highest_prob_list = {}

    # Simplifies response creation / adds it to the dict
    def response(bot_response, list_of_words, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, required_words)

    # Responses -------------------------------------------------------------------------------------------------------
    response('Hello!', ['hello', 'hi', 'hey', 'sup', 'heyo'], required_words=['hello', 'hi', 'hey', 'sup', 'heyo'])
    response('Bye!', ['bye', 'goodbye'], required_words=['bye', 'goodbye'])
    response('You\'re welcome!', ['thank', 'thanks'], required_words= ['thank', 'thanks'])
    response('You probably need to go to an Ear, Nose, and Throat clinic', ['headache','thyroid','swallowing','smelling','taste','sense' ,'of' ,'smell','nasal','nose','ear','tonsil', 'inflammation','i', 'have','runny ', 'nose','sore', 'thoat','caugh','sneezing','hearing', 'loss','snoring','obstructive', 'sleep', 'apnea','balance', 'problems','sinus', 'pressure','sinusitis'], required_words=['headache','swallowing','smelling','taste','smell','nasal','ear','tonsil','nose','sinusitis','sinus','balance','apnea','nose','throat','caugh','sneezing','thyroid','hearing','snoring'])
    response('You probably need to go to a Chest clinic', ['breath','breathing','shortness','cough','in','out','blood','mucus','not', 'gettig','enough', 'air','wheezing','chest','apnea'], required_words=['apnea','breath','cough','air','wheezing','chest'])
    response('You probably need to go to a Skin clinic', ['acne','persistent','rash','hives','scars','eczema','psoriasis','face','skin','warts','hair','nail','signs', 'of', 'aging','varicose','spider', 'veins','vitiligo'], required_words=['vitiligo','spider', 'veins','varicose','aging','nail','hair','warts','skin','face','psoriasis','acne','rash','hives','scars','eczema'])
    response('You probably need to go to an Oculist clinic', ['eye','see','blurry','blur','shades','shadows'], required_words=['eye','see','blurry','blur','shades','shadows'])
    response('You probably need to go to an Orthopedic clinic', ['back','bone','arm','leg','broken'], required_words=['back','bone','arm','leg','broken'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    if highest_prob_list[best_match] == 0:
      return "Not sure i got what you said"
    else:
      return best_match


# Used to get the response
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response
