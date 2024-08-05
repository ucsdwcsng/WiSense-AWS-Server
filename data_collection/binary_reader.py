import struct, os
from _CONST import _Const


def read_floats_from_file_with_metadata(filename):
    floats = []

    # Open the file in read-binary mode
    with open(filename, 'rb') as file:
        binary_data = file.read()

    # Calculate the number of floats in the binary data
    num_floats = len(binary_data) // struct.calcsize('d')

    # Convert the binary data back to an array of floats
    array = struct.unpack('d' * num_floats, binary_data)
    
    return array


if __name__ == '__main__':
    CONST = _Const(os)

    # Example usage
    directory_path = CONST.BINARY_FILES_FOLDER
    entries = os.listdir(directory_path)
    file_names_list = [entry for entry in entries if os.path.isfile(os.path.join(directory_path, entry))]
    print(file_names_list)

    
    all_floats_list = list(read_floats_from_file_with_metadata(f'binary_data/1722577142.1067612'))
    parsed_list = []
    for i in range(CONST.ROW_PER_FILE):
        offset = i*CONST.COL_PER_ROW
        parsed_list.append(all_floats_list[offset :offset + CONST.COL_PER_ROW])

    # print(parsed_list)
    print(len(parsed_list[0]))