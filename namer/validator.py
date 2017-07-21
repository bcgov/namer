import logging
import sys
import utils

from copy import deepcopy

logger = logging.getLogger(__name__)


class Validator:
    __severity_error_val = 2
    __severity_warn_val = 1
    __errors_arr = dict(code=1, message=None, severity=1)
    __errors_obj = dict(errors={'SEVERITY_ERROR_VALUE': __severity_error_val,
                                'SEVERITY_WARN_VALUE': __severity_warn_val,
                                'errors': list()},
                        valid=True, value=None)

    @staticmethod
    def corporate(query=None):
        """
        Checks a string to see if it a valid corporation type
        :param query: String to validate
        :return: Dictionary containing result of validating corporation type
        """
        result = deepcopy(Validator.__errors_obj)
        if query not in (None, ''):
            clean_q = utils.clean_string(query)
            if clean_q is None:
                result['errors']['errors'].append(
                    deepcopy(Validator.__errors_arr))

        result['value'] = query
        return result

    @staticmethod
    def validate(query=None):
        """
        Runs all the validation steps and returns a comprehensive dictionary
        :return: Dictionary containing results of all validation steps
        """
        result = dict()
        if query not in (None, ''):
            clean_q = utils.clean_string(query)
            split_q = clean_q.split()

            corp_result = Validator.corporate(split_q[-1])

            # TODO Stubs
            desc_result = deepcopy(Validator.__errors_obj)
            desc_result['value'] = "Descriptive"
            desc_result['errors']['errors'].append(
                deepcopy(Validator.__errors_arr))
            desc_result['errors']['errors'][0]['message'] = "Descriptive Error"
            desc_result['errors']['errors'][0]['severity'] = \
                Validator.__severity_error_val

            # TODO Stubs
            dist_result = deepcopy(Validator.__errors_obj)
            dist_result['value'] = "Distinctive"
            dist_result['errors']['errors'].append(
                deepcopy(Validator.__errors_arr))
            dist_result['errors']['errors'][0]['message'] = "Distinctive Warn"

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

        # TODO: Move logging infrastructure to proper place
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        if len(argv) > 1:
            validate_start = timer()
            results = Validator.validate(argv[1])
            validate_end = timer()

            logger.info('Results: %s', results)
            logger.info('Validate time: %s', str(validate_end - validate_start))
        else:
            logger.error('No search term specified')

if __name__ == "__main__":
    Validator.main(sys.argv)
