import sys


def xpath(top, path):
    result = top
    for i in path:
        result = result[i]
    return result


def truncate(s, n):
    return s if len(s) < n else s[:n - 2] + ".."

# stolen from nodemanager.tools
# replace a target file with a new contents - checks for changes
# can handle chmod if requested
# can also remove resulting file if contents are void, if requested
# performs atomically:
#    writes in a tmp file, which is then renamed(from sliverauth originally)
# returns True if a change occurred, or the file is deleted


def compare_without_trailing_newline(a ,b):
    """
    returns True if both strings are almost equal
    if any of the input strings ends with a "\n", 
    it is ignored is the comparison
    """
    a_ref = a if (not a or a[-1] != "\n") else a[:-1]
    b_ref = b if (not b or b[-1] != "\n") else b[:-1]
    return a_ref == b_ref

def replace_file_with_string(target, new_contents):
    try:
        with open(target) as reader:
            current = reader.read()
    except Exception as e:
        current = ""
    if compare_without_trailing_newline(current, new_contents):
        return False
    # overwrite target file
    with open(target, 'w') as writer:
        writer.write(new_contents)
    return True
