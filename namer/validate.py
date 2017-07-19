import logging

logger = logging.getLogger(__name__)


class Validate(object):
    def __init__(self):
        pass

    @staticmethod
    def validate():
        """
        Runs all the validation steps and returns a comprehensive dictionary
        :return: Dictionary containing results of all validation steps
        """

        stub_obj = {
            "corporation": {
                "errors": {
                    "errors": [
                        {
                            "code": 1,
                            "message": "Test corp error",
                            "severity": 1
                        }
                    ],
                    "ERROR_VALUE": 2,
                    "WARN_VALUE": 1
                },
                "valid": True,
                "value": "Ltd."
            },
            "descriptive": {
                "errors": {
                    "errors": [
                        {
                            "code": 1,
                            "message": "Test descriptive error",
                            "severity": 1
                        }
                    ],
                    "ERROR_VALUE": 2,
                    "WARN_VALUE": 1
                },
                "exists": True,
                "value": "Lawnmower"
            },
            "distinct": {
                "errors": {
                    "errors": [
                        {
                            "code": 1,
                            "message": "Test distinct error",
                            "severity": 2
                        }
                    ],
                    "ERROR_VALUE": 2,
                    "WARN_VALUE": 1
                },
                "exists": True,
                "value": "Bob's"
            }
        }

        return stub_obj
