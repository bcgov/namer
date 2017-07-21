import logging
import sys

logger = logging.getLogger(__name__)


class Validator:
    __severity_error_val = 2
    __severity_warn_val = 1

    @staticmethod
    def _create_errors_obj():
        return dict(
            errors={'SEVERITY_ERROR_VALUE': Validator.__severity_error_val,
                    'SEVERITY_WARN_VALUE': Validator.__severity_warn_val,
                    'errors': list()}, valid=True, value=None)

    @staticmethod
    def corporate(query=None):
        """
        Checks a string to see if it a valid corporation type
        :param query: String to validate
        :return: Dictionary containing result of validating corporation type
        """
        corp_types = ['(N.P.L.)',
                      '(NON - PERSONAL LIABILITY)',
                      '(NPL)',
                      'ASSOCIATION',
                      'CHURCH',
                      'CLUB',
                      'CO.',
                      'CO.,LTD.',
                      'CO.LTD.',
                      'CORP',
                      'CORP.',
                      'CORPORATION',
                      'CORPORATION.',
                      'FOUNDATION',
                      'INC',
                      'INC.',
                      'INCORPORATED',
                      'L.L.C.',
                      'LIMITED',
                      'LIMITED LIABILITY',
                      'LIMITED.',
                      'LIMITEE',
                      'LLC',
                      'LTD',
                      'LTD.',
                      'LTD.(N.P.L.)',
                      'LTEE',
                      'LTEE.',
                      'SOCIETY',
                      'ULC',
                      'INCORPOREE']

        result = Validator._create_errors_obj()
        result['value'] = query
        if query in (None, ''):
            error = dict(code=0,
                         message="Empty value",
                         severity=Validator.__severity_error_val)

            result['errors']['errors'].append(error)
            result['valid'] = False

        else:
            strip_q = query.strip()

            # More than 1 word
            if strip_q.find(' ') != -1:
                error = dict(code=1,
                             message="More than 1 word",
                             severity=Validator.__severity_error_val)

                result['errors']['errors'].append(error)
                result['valid'] = False

            # Doesn't match any corp_types
            if strip_q not in corp_types:
                error = dict(code=2,
                             message="Not a valid corporation type",
                             severity=Validator.__severity_error_val)

                result['errors']['errors'].append(error)
                result['valid'] = False

        return result

    @staticmethod
    def validate(query=None):
        """
        Runs all the validation steps and returns a comprehensive dictionary
        :return: Dictionary containing results of all validation steps
        """
        result = dict()
        if query not in (None, ''):
            split_q = query.split()
            corp_result = Validator.corporate(split_q[-1])

            # TODO Stubs
            desc_result = Validator._create_errors_obj()
            desc_result['value'] = "Descriptive"
            desc_result['errors']['errors'].append(
                dict(code=0, message=None, severity=1))
            desc_result['errors']['errors'][0]['message'] = "Descriptive Error"
            desc_result['errors']['errors'][0]['severity'] = \
                Validator.__severity_error_val

            # TODO Stubs
            dist_result = Validator._create_errors_obj()
            dist_result['value'] = "Distinctive"
            dist_result['errors']['errors'].append(
                dict(code=0, message=None, severity=1))
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
            val_start = timer()
            results = Validator.validate(argv[1])
            val_end = timer()

            logger.info('Results: %s', results)
            logger.info('Validate time: %s', str(val_end - val_start))
        else:
            logger.error('No search term specified')


if __name__ == "__main__":
    Validator.main(sys.argv)
