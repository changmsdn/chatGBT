import re


def test_pattern(patterns, text):
    if re.match(patterns, text):
        print(True)
    else:
        print(False)


if __name__ == '__main__':
    # pattern = re.compile(r'(Create|Generate|Execute|Add).*(with child nodes|add the child nodes).*', re.IGNORECASE)
    # string = "Create a sequence node with child nodes correct_positioning and check_assembly."
    # string = "create a sequence node, and then add the child nodes package_detection and target_location."
    # test_pattern(pattern, string)

    # pattern = re.compile(r'(Create|Generate|Execute|Produce|Add).*to.*', re.IGNORECASE)
    # string = "Add child nodes moving_package, target_location, and grab_package to the sequence node."
    # test_pattern(pattern, string)

    # pattern = re.compile(r'(.*? and .*?), then (.*)', re.IGNORECASE)
    # string = "Detect the package type and grab it, then place it at the target location."
    # test_pattern(pattern, string)

    pattern = re.compile(r'(.*?) (to.*)(the same time)', re.IGNORECASE)
    string = "Grab the package and mail it to the target location at the same time."
    test_pattern(pattern, string)
