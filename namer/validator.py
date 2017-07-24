import logging
import os
import sys

log = logging.getLogger(__name__)


class Validator:
    severity_error_val = 2
    severity_warn_val = 1

    __corp_phrases = None
    __desc_phrases = None

    def __new__(cls):
        """
        Reads and stores phrase lists into memory
        :return: None
        """
        if Validator.__corp_phrases is None:
            Validator.__corp_phrases = \
                Validator._load_data('corporate_phrase.csv')
        if Validator.__desc_phrases is None:
            Validator.__desc_phrases = \
                Validator._load_data('descriptive_phrase.csv')

    @staticmethod
    def _load_data(filename):
        """
        Loads a CSV file containing a list of phrases to match on
        :param filename: CSV file name
        :return: List containing phrases
        """
        import csv

        phrases = list()
        path = os.path.join(os.path.dirname(__file__), '..', 'files', filename)
        if not os.path.isfile(path):
            log.warning('%s not found.', filename)
            return phrases

        with open(path, newline='') as data:
            reader = csv.reader(data)
            try:
                for row in reader:
                    phrases.append(row[0])

            except UnicodeDecodeError:
                log.error('Unexpected input at line %s', reader.line_num)

        log.info('Loaded %s', filename)
        return phrases

    @staticmethod
    def _create_errors_obj():
        return dict(
            errors={'SEVERITY_ERROR_VALUE': Validator.severity_error_val,
                    'SEVERITY_WARN_VALUE': Validator.severity_warn_val,
                    'errors': list()}, value=None)

    @staticmethod
    def corporate(query=None):
        """
        Checks a string to see if it is a valid corporation type
        :param query: String to validate
        :return: Dictionary containing result of validating corporation type
        """
        result = Validator._create_errors_obj()
        result['value'] = query

        # Empty value
        if query is None or query.strip() is '':
            error = dict(code=0,
                         message="Empty value",
                         severity=Validator.severity_error_val)
            result['errors']['errors'].append(error)

        else:
            strip_q = query.strip()

            # More than 1 word
            if strip_q.find(' ') != -1:
                error = dict(code=1,
                             message="More than 1 word",
                             severity=Validator.severity_error_val)
                result['errors']['errors'].append(error)

            # Doesn't match any corp_types
            if strip_q not in Validator.__corp_phrases:
                error = dict(code=2,
                             message="Not a valid corporation type",
                             severity=Validator.severity_error_val)
                result['errors']['errors'].append(error)

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
        result = Validator._create_errors_obj()
        result['value'] = query

        # Empty value
        if query is None or query.strip() is '':
            result['exists'] = False

            error = dict(code=0,
                         message="Empty value",
                         severity=Validator.severity_error_val)
            result['errors']['errors'].append(error)

        else:
            result['exists'] = True
            strip_q = query.strip()

            # More than 1 word
            if strip_q.find(' ') != -1:
                error = dict(code=1,
                             message="More than 1 word",
                             severity=Validator.severity_error_val)
                result['errors']['errors'].append(error)

            # Doesn't contain descriptive value
            if strip_q not in Validator.__desc_phrases:
                error = dict(code=2,
                             message="No descriptive value found",
                             severity=Validator.severity_error_val)
                result['errors']['errors'].append(error)

        return result

    @staticmethod
    def validate(query=None):
        """
        Runs all the validation steps and returns a comprehensive dictionary
        :return: Dictionary containing results of all validation steps
        """
        result = dict()
        if query is not None and query.strip() is not '':
            split_q = query.strip().split()

            # TODO Add smarter line parsing logic
            if len(split_q) != 3:
                log.warning('Expected 3 words - may have unexpected results')

            try:
                corp_result = Validator.corporate(split_q[-1])
            except IndexError:
                corp_result = Validator.corporate()

            try:
                desc_result = Validator.descriptive(split_q[1])
            except IndexError:
                desc_result = Validator.descriptive()

            # TODO Distinct Stub
            dist_result = Validator._create_errors_obj()
            dist_result['value'] = split_q[0]
            dist_result['exists'] = True
            dist_result['errors']['errors'].append(
                dict(code=0, message=None, severity=1))
            dist_result['errors']['errors'][0]['message'] = \
                "Distinctive Warn"

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
            results = Validator.validate(argv[1])
            val_end = timer()

            log.info('Results: %s', results)
            log.info('Phrase load time: %s', str(load_end - load_start))
            log.info('Validate time: %s', str(val_end - val_start))
        else:
            log.error('No search term specified')


if __name__ == "__main__":
    Validator.main(sys.argv)
