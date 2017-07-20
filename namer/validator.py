import logging
import sys

logger = logging.getLogger(__name__)


class Validate(object):
    def __init__(self):
        pass

    @staticmethod
    def corporate(value):
        """
        Checks a string to see if it a valid corporation type
        :param value: String to validate
        :return: Dictionary containing result of validating corporation type
        """
        stub_obj = {
            "errors": {
                "SEVERITY_ERROR_VALUE": 2,
                "SEVERITY_WARN_VALUE": 1,
                "errors": [
                    {
                        "code": 1,
                        "message": "Test corp error",
                        "severity": 1
                    }
                ]
            },
            "valid": True,
            "value": "Ltd."
        }

        return stub_obj

    @staticmethod
    def validate():
        """
        Runs all the validation steps and returns a comprehensive dictionary
        :return: Dictionary containing results of all validation steps
        """
        corp_result = Validate.corporate('')
        desc_result = {
            "errors": {
                "SEVERITY_ERROR_VALUE": 2,
                "SEVERITY_WARN_VALUE": 1,
                "errors": [
                    {
                        "code": 1,
                        "message": "Test descriptive error",
                        "severity": 1
                    }
                ]
            },
            "exists": True,
            "value": "Lawnmower"
        }
        dist_result = {
            "errors": {
                "SEVERITY_ERROR_VALUE": 2,
                "SEVERITY_WARN_VALUE": 1,
                "errors": [
                    {
                        "code": 1,
                        "message": "Test distinct error",
                        "severity": 2
                    }
                ]
            },
            "exists": True,
            "value": "Bob's"
        }

        return dict(corporation=corp_result,
                    descriptive=desc_result,
                    distinct=dist_result)

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
            results = Validate.validate()
            validate_end = timer()

            logger.info('Results: %s', results)
            logger.info('Validate time: %s', str(validate_end - validate_start))
        else:
            logger.error('No search term specified')

if __name__ == "__main__":
    Validate.main(sys.argv)
