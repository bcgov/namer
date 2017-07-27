#!/usr/bin/python
import logging
import os
import sys
import utils

log = logging.getLogger(__name__)


class Validator:
    severity_error_val = 2
    severity_warn_val = 1

    error_types = {
        'emptyvalue': dict(code=1000, severity=severity_error_val,
                           message="Empty value"),
        'oneword': dict(code=1001, severity=severity_warn_val,
                        message="More than 1 word"),
        'invalidcorp': dict(code=1002, severity=severity_error_val,
                            message="Not a valid corporation type"),
        'nodescvalue': dict(code=1003, severity=severity_error_val,
                            message="No descriptive value found"),
    }

    __corp_phrases = None
    __desc_phrases = None
    __blacklist_phrases = None
    __greylist_phrases = None

    def __new__(cls):
        """
        Reads and stores phrase lists into memory
        :return: None
        """
        if Validator.__corp_phrases is None:
            Validator.__corp_phrases = \
                Validator._load_csv('corporate_phrase.csv')
        if Validator.__desc_phrases is None:
            Validator.__desc_phrases = \
                Validator._load_csv('descriptive_phrase.csv')

        if Validator.__blacklist_phrases is None:
            Validator.__blacklist_phrases = \
                Validator._load_txt('blacklist_phrase.txt')
        if Validator.__greylist_phrases is None:
            Validator.__greylist_phrases = \
                Validator._load_txt('greylist_phrase.txt')

    @staticmethod
    def _load_csv(filename):
        """
        Loads a CSV file containing a list of phrases to match on
        :param filename: CSV file name
        :return: Tuple containing phrases
        """
        import csv

        phrases = list()
        path = os.path.join(os.path.dirname(__file__), '..', 'files', filename)
        if not os.path.isfile(path):
            log.warning('%s not found.', filename)
            return tuple(phrases)

        with open(path, newline='') as data:
            reader = csv.reader(data)
            try:
                for row in reader:
                    phrases.append(row[0])

            except UnicodeDecodeError:
                log.error('Unexpected input at line %s', reader.line_num)

        log.info('Loaded %s', filename)
        return tuple(phrases)

    @staticmethod
    def _load_txt(filename):
        """
        Loads a TXT file containing a list of codes and phrases to match on
        :param filename: Text file name
        :return: Tuple containing phrases
        """
        phrases = list()
        path = os.path.join(os.path.dirname(__file__), '..', 'files', filename)
        if not os.path.isfile(path):
            log.warning('%s not found.', filename)
            return tuple(phrases)

        with open(path, newline='') as data:
            for line in data:
                split_line = line.strip().split()
                entry = (split_line[0], ' '.join(split_line[1:]))
                phrases.append(entry)

        log.info('Loaded %s', filename)
        return tuple(phrases)

    @staticmethod
    def _create_errors_obj():
        return dict(
            errors={'SEVERITY_ERROR_VALUE': Validator.severity_error_val,
                    'SEVERITY_WARN_VALUE': Validator.severity_warn_val,
                    'errors': list()})

    @staticmethod
    def blacklist(query=None):
        """
        Checks a string for occurrences of blacklist words
        :param query: String to check against blacklist
        :return: Dictionary containing results of blacklist occurrences
        """
        if query is not None:
            query = query.upper()

        result = Validator._create_errors_obj()
        result['blacklisted'] = dict(values=list())

        # Empty value
        if query is None or query.strip() is '':
            result['errors']['errors'].append(
                Validator.error_types['emptyvalue'])

        else:
            clean_q = utils.re_alphanum(query)

            # Contains blacklist matches
            for code, pattern in Validator.__blacklist_phrases:
                if pattern in clean_q:
                    result['blacklisted']['values'].append(pattern)
                    result['errors']['errors'].append(
                        dict(code=code, severity=Validator.severity_warn_val,
                             message=f"Blacklist match on '{pattern}'"))

        return result

    @staticmethod
    def corporate(query=None):
        """
        Checks a string to see if it is a valid corporation type
        :param query: String to validate
        :return: Dictionary containing result of validating corporation type
        """
        if query is not None:
            query = query.upper()

        result = Validator._create_errors_obj()
        result['value'] = query

        # Empty value
        if query is None or query.strip() is '':
            result['errors']['errors'].append(
                Validator.error_types['emptyvalue'])

        else:
            strip_q = query.strip()

            # More than 1 word
            if strip_q.find(' ') != -1:
                result['errors']['errors'].append(
                    Validator.error_types['oneword'])

            # Doesn't match any corp_types
            if strip_q not in Validator.__corp_phrases:
                result['errors']['errors'].append(
                    Validator.error_types['invalidcorp'])

        result['valid'] = len(result['errors']['errors']) == 0
        return result

    @staticmethod
    def descriptive(query=None):
        """
        Checks a string to see if it contains a valid descriptive for corporate
        names
        :param query: String to validate
        :return: Dictionary containing result of validating descriptive
        """
        if query is not None:
            query = query.upper()

        result = Validator._create_errors_obj()
        result['value'] = query

        # Empty value
        if query is None or query.strip() is '':
            result['exists'] = False
            result['errors']['errors'].append(
                Validator.error_types['emptyvalue'])

        else:
            result['exists'] = True
            strip_q = query.strip()

            # More than 1 word
            if strip_q.find(' ') != -1:
                result['errors']['errors'].append(
                    Validator.error_types['oneword'])

            # Doesn't contain descriptive value
            if strip_q not in Validator.__desc_phrases:
                result['errors']['errors'].append(
                    Validator.error_types['nodescvalue'])

            # Check Blacklist
            black_result = Validator.blacklist(strip_q)
            result['errors']['errors'].extend(
                black_result['errors']['errors'])

            # Check Greylist
            grey_result = Validator.greylist(strip_q)
            result['errors']['errors'].extend(
                grey_result['errors']['errors'])

        return result

    @staticmethod
    def distinctive(query=None):
        """
        Checks a string to see if it contains a valid distinctive for corporate
        names
        :param query: String to validate
        :return: Dictionary containing result of validating distinctive
        """
        if query is not None:
            query = query.upper()

        result = Validator._create_errors_obj()
        result['value'] = query

        # Empty value
        if query is None or query.strip() is '':
            result['exists'] = False
            result['errors']['errors'].append(
                Validator.error_types['emptyvalue'])

        else:
            result['exists'] = True
            strip_q = query.strip()

            # More than 1 word
            if strip_q.find(' ') != -1:
                result['errors']['errors'].append(
                    Validator.error_types['oneword'])

            # Check Blacklist
            black_result = Validator.blacklist(strip_q)
            result['errors']['errors'].extend(
                black_result['errors']['errors'])

            # Check Greylist
            grey_result = Validator.greylist(strip_q)
            result['errors']['errors'].extend(
                grey_result['errors']['errors'])

        return result

    @staticmethod
    def greylist(query=None):
        """
        Checks a string for occurrences of greylist words
        :param query: String to check against greylist
        :return: Dictionary containing results of greylist occurrences
        """
        if query is not None:
            query = query.upper()

        result = Validator._create_errors_obj()
        result['greylisted'] = dict(values=list())

        # Empty value
        if query is None or query.strip() is '':
            result['errors']['errors'].append(
                Validator.error_types['emptyvalue'])

        else:
            clean_q = utils.re_alphanum(query)

            # Contains greylist matches
            for code, pattern in Validator.__greylist_phrases:
                if pattern in clean_q:
                    result['greylisted']['values'].append(pattern)
                    result['errors']['errors'].append(
                        dict(code=code, severity=Validator.severity_warn_val,
                             message=f"Greylist match on '{pattern}'"))

        return result

    @staticmethod
    def validate(query=None):
        """
        Runs all the validation steps and returns a comprehensive dictionary
        :param query: String to validate
        :return: Dictionary containing results of all validation steps
        """
        if query is None or query.strip() is '':
            result = dict(corporation=Validator.corporate(),
                          descriptive=Validator.descriptive(),
                          distinct=Validator.distinctive())

        else:
            query = query.upper()
            clean_q = utils.re_alphanum(query)
            split_q = clean_q.strip().split()

            # TODO Add smarter line parsing logic
            if len(split_q) != 3:
                log.warning('Expected 3 words - may have unexpected results')

            try:
                corp_result = Validator.corporate(split_q[-1])
                split_q = split_q[:-1]
            except IndexError:
                corp_result = Validator.corporate()

            try:
                desc_result = Validator.descriptive(split_q[-1])
                split_q = split_q[:-1]
            except IndexError:
                desc_result = Validator.descriptive()

            try:
                dist_result = Validator.distinctive(' '.join(split_q))
            except IndexError:
                dist_result = Validator.distinctive()

            result = dict(corporation=corp_result,
                          descriptive=desc_result,
                          distinct=dist_result)

        return result

    @staticmethod
    def main(argv):
        """
        Validates and prints the results of the search term with timings
        :param argv: Command line arguments
        :return: None
        """
        from timeit import default_timer as timer

        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        if len(argv) > 1:
            load_start = timer()
            Validator()
            load_end = timer()
            val_start = timer()
            val_results = Validator.validate(argv[1])
            val_end = timer()
            black_start = timer()
            black_results = Validator.blacklist(argv[1])
            black_end = timer()
            grey_start = timer()
            grey_results = Validator.greylist(argv[1])
            grey_end = timer()

            log.debug('Validator Results: %s', val_results)
            log.debug('Blacklist Results: %s', black_results)
            log.debug('Greylist Results: %s', grey_results)
            log.debug('Phrase load time: %s', str(load_end - load_start))
            log.debug('Validate time: %s', str(val_end - val_start))
            log.debug('Blacklist time: %s', str(black_end - black_start))
            log.debug('Greylist time: %s', str(grey_end - grey_start))
        else:
            log.error('No search term specified')


if __name__ == "__main__":
    Validator.main(sys.argv)
