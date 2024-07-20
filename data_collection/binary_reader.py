import struct

class _Const(object):
    MAX_BINARY_ENTRY_COUNT = 100
    COL_PER_ROW = 1024
    ROW_PER_FILE = 100

def read_floats_from_file_with_metadata(filename):
    floats = []
    
    # # Open the file in read-binary mode
    # with open(f'binary_data/1721434991.2359798', 'rb') as binary_data:
    #         # # Read the metadata (length of the next array)
    #         # metadata = file.read(struct.calcsize('I'))
    #         # if not metadata:
    #         #     break
    #         # (length,) = struct.unpack('I', metadata)

    #         # Read the binary data for the array

    #         # binary_data = file.read(length * struct.calcsize('f'))
    #     array = struct.unpack('f', binary_data)
    
    # return array

    # Open the file in read-binary mode
    with open(filename, 'rb') as file:
        binary_data = file.read()

    # Calculate the number of floats in the binary data
    num_floats = len(binary_data) // struct.calcsize('d')

    # Convert the binary data back to an array of floats
    array = struct.unpack('d' * num_floats, binary_data)
    
    return array


if __name__ == '__main__':
    CONST = _Const()

    # Example usage
    all_floats_list = list(read_floats_from_file_with_metadata(f'binary_data/1721439530.3639653'))
    parsed_list = []
    for i in range(CONST.ROW_PER_FILE):
        offset = i*CONST.COL_PER_ROW
        parsed_list.append(all_floats_list[offset :offset + CONST.COL_PER_ROW])

    # print(all_floats_list[99*CONST.COL_PER_ROW:100*CONST.COL_PER_ROW])
    # print(all_floats_list)
    # print(len(parsed_list))