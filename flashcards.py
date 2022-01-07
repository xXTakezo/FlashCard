import json
import argparse
from io import StringIO
import random
memory_file = StringIO()

class Flashcard:

    flashcard = "Card:\n{term}\nDefinition:\n{definition}"
    all = {}
    terms_definitions = {}
    only_terms = list(terms_definitions.keys())
    memory_file.read()
    memory_file.write('Object Flashcard has been created.\n')

    def __init__(self, term, definition, error_count = 0):
        self.term = term
        self.definition = definition
        self.error_count = error_count

    def __str__(self):
        return self.flashcard.format(term=self.term, definition = self.definition)

    def check_answer(self):
        answer = input('Print the definition of "{term}":\n'.format(term=self.term))
        memory_file.write('Print the definition of "{term}":\n'.format(term=self.term))
        if self.definition == answer:
            print('Correct!')
            memory_file.write('Correct!\n')
        else:
            self.error_count += 1
            if answer in Flashcard.terms_definitions.values():
                right_term = list(Flashcard.terms_definitions.keys())[list(Flashcard.terms_definitions.values()).index(answer)]
                print('Wrong. The right answer is "{0}", but your definition is correct for "{1}".'.format(self.definition, right_term))
                memory_file.write('Wrong. The right answer is "{0}", but your definition is correct for "{1}".\n'.format(self.definition, right_term))
            else:
                print('Wrong. The right answer is "{0}".'.format(self.definition))
                memory_file.write('Wrong. The right answer is "{0}".\n'.format(self.definition))

def create_flashcards():
    print('The card:')
    memory_file.write('The card:\n')
    term = input()
    while True:
        if term in Flashcard.terms_definitions.keys():
            print('The term "{0}" already exists. Try again:'.format(term))
            memory_file.write('The term "{0}" already exists. Try again:\n'.format(term))
            term = input()
            continue
        else:
            break
    print('The definition of the card:')
    memory_file.write('The definition of the card:\n')
    definition = input()
    while True:
        if definition in Flashcard.terms_definitions.values():
            print('The definition "{0}" already exists. Try again:'.format(definition))
            memory_file.write('The definition "{0}" already exists. Try again:\n'.format(definition))
            definition = input()
            continue
        else:
            break
    print('The Pair ("{0}":"{1}") has been added.'.format(term,definition))
    Flashcard.all[term] = Flashcard(term, definition)
    Flashcard.terms_definitions[term] = definition
    #logging.info('Flashcard pair {0}:{1} has been created.'.format(term, definition))
    memory_file.read()
    memory_file.write('The Pair ("{0}":"{1}") has been added.\n'.format(term,definition))

def remove():
        print('Which card?')
        memory_file.write('Which card?\n')
        card_to_delete = input()
        if card_to_delete in Flashcard.all.keys():
            del Flashcard.all[card_to_delete]
            del Flashcard.terms_definitions[card_to_delete]
            print('The card has been removed.')
            #logging.info('User removed card "{0}"'.format(card_to_delete))
            memory_file.read()
            memory_file.write('The card has been removed.\n'.format(card_to_delete))
        else:
            print('Can\'t remove "{0}": there is no such card.'.format(card_to_delete))
            #logging.info('User tried to remove non-existing card "{0}"'.format(card_to_delete))
            memory_file.read()
            memory_file.write('Can\'t remove "{0}": there is no such card.\n'.format(card_to_delete))

def ask():
    print("How many times to ask?")
    memory_file.write("How many times to ask?\n")
    n = int(input())
    entry_list = list(Flashcard.all.values())
    for i in range(n):
        random_entry = random.choice(entry_list)
        random_entry.check_answer()

def import_file(file_name):
    try:
        file = open("C:\\Users\\Ramin\\PycharmProjects\\Flashcards\\Flashcards\\task\\" + file_name)
        data = json.load(file)
        for k, v in data.items():
            term = k
            definition = v[0]
            error_count = v[1]
            Flashcard.all[term] = Flashcard(term, definition, error_count)
            Flashcard.terms_definitions[term] = definition
        print("{0} cards have been loaded.".format(str(len(data))))
        memory_file.write("{0} cards have been loaded.".format(str(len(data))))
        file.close()
    except FileNotFoundError:
        print('File not found.')
        #logging.warning('FileNotFoundError: File {0} was not found.'.format(file_name))
        memory_file.read()
        memory_file.write('File not found.\n'.format(file_name))

def export_file(file_name):
    all_cards  = {}
    for term, object in Flashcard.all.items():
        all_cards[term] = [object.definition, object.error_count]
    json.dump(all_cards, open(file_name, 'w'))
    print("{0} cards have been saved.".format(str(len(all_cards))))
    #logging.info('File {0} with {1} cards exported.'.format(file_name, str(len(Flashcard.terms_definitions))))
    memory_file.read()
    memory_file.write("{0} cards have been saved.\n".format(str(len(Flashcard.terms_definitions))))

def set_logger():
    print('File name:')
    memory_file.write('File name:\n')
    file_name = input()
    memory_file.getvalue()
    memory_file.seek(0)
    with open(file_name, 'w') as log:
        for line in memory_file:
            log.write(line)
    print('The log has been saved.')
    memory_file.write('The log has been saved.\n')

def hardest_card():
        error_dictionary = {}
        for term, object in Flashcard.all.items():
            error_dictionary[term] = object.error_count
        if len(error_dictionary) == 0:
            print('There are no cards with errors.')
            memory_file.write('There are no cards with errors.\n')
        elif max(error_dictionary.values()) == 0:
            print('There are no cards with errors.')
            memory_file.write('There are no cards with errors.\n')
        else:
            mx = max(error_dictionary.values())
            highest_values = [k for k, v in error_dictionary.items() if v == mx]
            max_error_dictionary = {}
            for entry in highest_values:
                max_error_dictionary[entry] = Flashcard.all[entry].error_count
            if len(max_error_dictionary) == 1:
                hardest_term = highest_values[0]
                print('The hardest card is "{0}". You have {1} errors answering it.'.format(hardest_term, max_error_dictionary[hardest_term]))
                memory_file.write('The hardest card is "{0}". You have {1} errors answering it.\n'.format(hardest_term, max_error_dictionary[hardest_term]))
            elif len(max_error_dictionary) == 2:
                first_hardest_term = highest_values[0]
                second_hardest_term = highest_values[0]
                print('The hardest cards are "{0}", "{1}".'.format(first_hardest_term, second_hardest_term))
                memory_file.write('The hardest cards are "{0}", "{1}".\n'.format(first_hardest_term, second_hardest_term))

def reset_stats():
    for term, object in Flashcard.all.items():
        object.error_count = 0
    print('Card statistics have been reset.')
    memory_file.write('Card statistics have been reset.\n')

parser = argparse.ArgumentParser(description='This program let\'s you import and export flashcards, create them, start a quiz and get you some insight about your learning behaviour.')
parser.add_argument('--import_from')
parser.add_argument('--export_to')
args = parser.parse_args()

def parser_import():
    if args.import_from is not None:
        import_file(args.import_from)

def parser_export():
    if args.export_to is not None:
        export_file(args.export_to)


def main_program():
    memory_file.write('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n')
    parser_import()
    while True:
        print('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):')
        action = input()
        if action == 'add':
            create_flashcards()
            print('\n')
            memory_file.write('\n')
        elif action == 'remove':
            remove()
            print('\n')
            memory_file.write('\n')
        elif action == 'import':
            print("File name:")
            memory_file.write("File name:\n")
            file_name = input()
            import_file(file_name)
            print('\n')
            memory_file.write('\n')
        elif action == 'export':
            print("File name:")
            memory_file.write("File name:\n")
            file_name = input()
            export_file(file_name)
            print('\n')
            memory_file.write('\n')
        elif action == 'ask':
            ask()
            print('\n')
            memory_file.write('\n')
        elif action == 'log':
            set_logger()
            print('\n')
            memory_file.write('\n')
        elif action == 'hardest card':
            hardest_card()
            print('\n')
            memory_file.write('\n')
        elif action == 'reset stats':
            reset_stats()
            print('\n')
            memory_file.write('\n')
        elif action == 'exit':
            print("Bye bye!")
            parser_export()
            memory_file.read()
            memory_file.write("Bye bye!\n")
            break

main_program()









