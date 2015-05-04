from bs4 import BeautifulSoup
import requests


def retrieve_from_url(url):
    """
    Retrieves text from url, removes all string formatting \n and \t
    """
    soup = BeautifulSoup(requests.get(url).text)
    soup = soup.text.replace("\n", " ").replace("\t", " ")
    return soup.lower()


def check_format(string_query, url):
    """
    Raises errors
    """
    # Testing NOT OR AND are uppercase
    query_list = string_query.split()
    query_list = [elem for elem in query_list if elem in ["NOT", "AND", "OR"]]
    test_list = string_query.lower().split()
    test_list = [elem.upper() for elem in test_list if elem in ["not", "and", "or"]]
    if len(query_list) - len(test_list) != 0:
        raise SyntaxError('All words NOT, AND, OR must be upper case.')
    # Parenthesis are spaced test
    for item in string_query.split():
        if ('(' in item and len(item) != 1) or (')' in item and len(item) != 1):
            raise SyntaxError("Space the parenthesis")
    # Make sure compound statements have parenthesis
    if "OR" in string_query and query_list.count("OR") + query_list.count("AND") > 1:
        if '(' not in string_query or ')' not in string_query:
            raise SyntaxError("Complex statements must use parenthesis")
    # Test proper use of parenthesis, or all statements are closed properly
    stack = []
    for elem in string_query:
        if elem == '(':
            stack.append(elem)
        if elem == ')' and '(' in stack:
            stack.remove('(')
        elif elem == ')' and '(' not in stack:
            raise SyntaxError("Check opening and closing of parenthesis")
    # Test url
    if "http" not in url:
        raise SyntaxError("Fix url, add http://")


def process_text(text):
    """
    Changes text from a string into a list of words, splits on empty space. This makes sure whole words are searched
    only. For example "found" query of "foundation" returns false.
    """
    text = text.split(" ")
    text = [elem for elem in text if elem != '']
    return text


def query(string_query, url):
    """
    Main function. Takes a query, and url in the form of a string. Returns boolean.
    """
    check_format(string_query, url)
    text = retrieve_from_url(url)
    text = process_text(text)
    return statement_complexity_evaluator(string_query, text)


def statement_complexity_evaluator(query_string, text):
    """
    Assuming the formats very followed well
    Decides on query complexity- simple statements get processed simple, complex statements sent to the tree
    """
    query_list = query_string.split()
    # changing to lower case for all letters in the html text to achieve case insensitivity
    lowercase_list = []
    for elem in query_list:
        if elem not in ["NOT", "AND", "OR"]:
            lowercase_list.append(elem.lower())
        else:
            lowercase_list.append(elem)
    query_string = " ".join(lowercase_list)
    # For complex statements
    if "OR" in query_string and query_list.count("OR") + query_list.count("AND") > 1:
        tree = build_tree(query_string)
        boolean = evaluate_tree(tree, text)
        return boolean
    # For simple statements
    else:
        boolean = build_list(query_string, text)
        return boolean


def build_list(query_string, text):
    """
    Takes a simple query and builds a list of Items
    """
    query_list = query_string.split()
    # Build list of class Item
    query_list = [Item(elem) for elem in query_list]
    # Update Item objects with sign attribute
    for elem in query_list:
        if elem.name == "NOT":
            query_list[query_list.index(elem) + 1].sign = "NOT"
    # Remove NOT and AN, OR is passed only for OR compound states, all OR possibilities should go to complex evaluation
    query_list = [elem for elem in query_list if elem.name != "NOT" and elem.name != 'AND']
    return evaluate_list(query_list, text)


def evaluate_list(query_list, text):
    """
    Takes a list of Items and evaluates the list as True or false
    """
    or_statement = False
    bool_list = []
    for elem in query_list:
        # For "or" compound statements
        if elem.name == 'OR':
            or_statement = True
            continue
        sign = elem.sign
        if elem.name in text:
            boolean = True
        else:
            boolean = False
        if sign is not None:
            boolean = not boolean
        bool_list.append(boolean)
    if or_statement:
        if bool_list[0] is True or bool_list[1] is True:
            return True
        else:
            return False
    for elem in bool_list:
        if elem is False:
            return False
    return True


class Item:
    """
    Class Item. Every word in query except "NOT" becomes a Item object where name variable describes the object
    and the sign variable indicates the presence of a preceding "NOT".
    """
    def __init__(self, name, sign=None):
        self.name = name
        self.sign = sign

    def __str__(self):
        return self.name


def tree_bool_evaluation(root_obj, text):
    """
    Takes self.get_root_Value and text. Does not return anything, only changes objects. Changes the tree from a tree of
    Item objects to a tree of bools
    """
    # If strings
    if type(root_obj.get_left_child().get_root_value()) is Item:
        left_child = str(root_obj.get_left_child().get_root_value().name)
        if left_child in text:
            left_child = True
        else:
            left_child = False
        if root_obj.get_left_child().get_root_value().sign is not None:
            left_child = not left_child
    if type(root_obj.get_right_child().get_root_value()) is Item:
        right_child = str(root_obj.get_right_child().get_root_value().name)
        if right_child in text:
            right_child = True
        else:
            right_child = False
        if root_obj.get_right_child().get_root_value().sign is not None:
            right_child = not right_child
    # If booleans
    if type(root_obj.get_left_child().get_root_value()) is bool:
        left_child = root_obj.get_left_child().get_root_value()
    if type(root_obj.get_right_child().get_root_value()) is bool:
        right_child = root_obj.get_right_child().get_root_value()
    # Left and right children have been defined, now current leaf is evaluated
    # If "AND" leaf
    node_sign = root_obj.get_root_value().sign
    if root_obj.get_root_value().name == 'AND':
        root_obj.set_root_value(left_child and right_child)
    # If "OR" leaf
    elif root_obj.get_root_value().name == 'OR':
        root_obj.set_root_value(left_child or right_child)
    if node_sign is not None:
        root_obj.set_root_value(not root_obj.get_root_value())

def evaluate_tree(tree, text):
    """
    Traverses the tree in the preorder fashion. Once the base case is found, bool_tree_evaluation is called to change
    the tree of Item objects to a tree of booleans
    """
    if str(tree.left_child.get_root_value()) in ['AND', 'OR']:
        evaluate_tree(tree.left_child, text)
    if str(tree.right_child.get_root_value()) in ['AND', 'OR']:
        evaluate_tree(tree.right_child, text)
    # Establishing the base case
    # If neither children are AND/OR
    if str(tree.get_left_child().get_root_value()) not in ['AND', 'OR'] and \
            str(tree.get_right_child().get_root_value()) not in ['AND', 'OR']:
        tree_bool_evaluation(tree, text)
    return tree.get_root_value()


class BinaryTree:
    """
    Builds tree for complex statements
    """
    def __init__(self, root_obj):
        self.key = root_obj
        self.left_child = None
        self.right_child = None

    def insert_left(self, new_node):
        self.left_child = BinaryTree(new_node)

    def insert_right(self, new_node):
        self.right_child = BinaryTree(new_node)

    def get_right_child(self):
        return self.right_child

    def get_left_child(self):
        return self.left_child

    def set_root_value(self, obj):
        self.key = obj

    def get_root_value(self):
        return self.key

    def __str__(self):
        return self.key


def process_not(index, alist):
    """
    Takes list of objects, NOT, and changes the correct object so object.sign == NOT
    Function used for complex statements, only called by build_Tree
    """
    count = 0
    for item in alist[index:]:
        if item.name == '(':
            count += 1
            continue
        if item.name == ')':
            count -= 1
            if count == 0 and item.name == ')':
                alist[alist.index(item)-2].sign = 'NOT'
                break
            continue
        elif count == 0:
            item.sign = 'NOT'
            break


def correct_query_input(input_string):
    """
    Adds parenthesis to both ends of strings
    """
    if '(' in input_string and input_string[-1] != ')' or '(' not in input_string:
        input_string = "( " + input_string + " )"
    return input_string

def build_tree(input_string):
    """
    For complex statements involving parenthesis. Also called a parse tree.
    """
    input_string = correct_query_input(input_string)
    # Need to isolate simple cases where trees need not be build
    input_list = input_string.split()
    input_list = [Item(elem) for elem in input_list]
    tree = BinaryTree('temp_value')
    stack = []
    stack.append(tree)
    current_node = tree
    for item in input_list:
        if item.name == 'NOT':
            process_not((input_list.index(item)), [elem for elem in input_list if elem.name != 'NOT'])
            continue
        if item.name == '(':
            current_node.insert_left("temp_value")
            stack.append(current_node)
            current_node = current_node.get_left_child()
        elif item.name not in ['AND', 'OR', ')']:
            current_node.set_root_value(item)
            parent = stack.pop()
            current_node = parent
        elif item.name in ['AND', 'OR']:
            current_node.set_root_value(item)
            current_node.insert_right('temp_value')
            stack.append(current_node)
            current_node = current_node.get_right_child()
        elif item.name == ')':
            current_node = stack.pop()
    return current_node


