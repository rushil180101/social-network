import uuid


# The following function will generate a string representing unique ID.
# The ID is generated based on time, computer hardware, etc.
# e.g. dbe3178d-4b83-5024-9b26-9b8e1b280514
def get_random_code():
    # There are other functions like uuid1(), uuid3(), uuid5(), etc.
    # but uuid4() does not compromise with privacy because it keeps the MAC address hidden unlike uuid1().
    code = str(uuid.uuid4())[:8].replace('-', '').lower()
    return code
