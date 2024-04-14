import unittest
from rules import apply_condition, apply_rule

class TestRules(unittest.TestCase):

    def test_apply_condition_from_contains(self):
        condition = {
            'field': 'from',
            'predicate': 'contains',
            'value': 'example@example.com'
        }
        email = {
            'from': 'Example User <example@example.com>'
        }
        
        print(f"Testing condition: {condition}, Email: {email}")
        result = apply_condition(condition, email)
        self.assertTrue(result, f"Condition failed: {condition}, Email: {email}")


    def test_apply_condition_subject_contains(self):
        condition = {
            'field': 'subject',
            'predicate': 'contains',
            'value': 'Test'
        }
        email = {
            'subject': 'Test Subject'
        }
        
        print(f"Testing condition: {condition}, Email: {email}")
        result = apply_condition(condition, email)
        self.assertTrue(result, f"Condition failed: {condition}, Email: {email}")
        

    def test_apply_rule_all(self):
        rule = {
            'predicate': 'all',
            'conditions': [
                {
                    'field': 'from',
                    'predicate': 'contains',
                    'value': 'example@example.com'
                },
                {
                    'field': 'subject',
                    'predicate': 'contains',
                    'value': 'Test'
                }
            ],
            'action': {}
        }
        email = {
            'from': 'Example User <example@example.com>',
            'subject': 'Test Subject'
        }

        print(f"Testing rule: {rule}, Email: {email}")
        result = apply_rule(rule, email)
        self.assertTrue(result, f"Rule failed: {rule}, Email: {email}")


if __name__ == '__main__':
    unittest.main()
