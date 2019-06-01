import numpy as np
import time



"""
this part queries the user on certain starting conditions
"""

# change file source
file_location = input("Where is the file located? \n")





"""
the 'binary_converter' takes in the data file and then converts them into a
visual 64-bit binary representation of 1's and 0's
"""

def binary_convert(array):
    lst = []
    for i in array:
        lst.append(np.binary_repr(i,64))
    return lst





"""
the 'binary-to-decimal converter with range', or 'b2d_with_range', helps to
convert the timing information for a specific range of bits from binary to
decimal representation. this range can be adjusted at the start of the file,
simply select which bits are needed, no need to account for the 0th position etc..
"""

def b2d_with_range(binary_data_to_act_on):
    new_list = []
    binary_data = binary_convert(binary_data_to_act_on)

    end_bit = 64 - int(input("Please choose the starting bit position: \n"))
    start_bit = 63 - int(input("Please choose the ending bit position: \n"))    
    print("The number of bits you have selected is:")
    difference = end_bit - start_bit
    print(difference)
    
    print("\n")
    
    for item in binary_data:
        summation = 0
        reversed_item = item[start_bit:end_bit][::-1]
        
        for index, value in enumerate(reversed_item):
            summation += int(value)*(2**index)
        new_list.append(summation)
        
    return new_list





"""
this code is to get the count rate from the number of events in the source
file
"""

def countrate(in_file):
    all_events = binary_convert(in_file)

    def decimal_timing_individual(input_binary_string):
        time = float(0)
        for index, value in enumerate(input_binary_string):
            if int(value) == 1:
                time += (1/256)*float(10**(-9))*float(2**int(index))
        return time

    event_counts, seconds, cps = 0, float(1), []
    counter = 0
    while counter < len(all_events):
        individual_reversed = all_events[counter][0:54][::-1]

        if decimal_timing_individual(individual_reversed) >= seconds:
            cps += [event_counts]
            event_counts = 0
            seconds += float(1)
            counter += 1
        else:
            event_counts += 1
            counter += 1
    return cps





"""
this is a script for g2; it is supposed to be similar to the current g2 script,
but adapted for higher timing resolutions
"""

def g2(in_list):
    return "The function 'g2' has not been created yet"





"""
this code automatically compiles the moment you've keyed in your values above
(if that option is set to be on). it also asks for the functions you want to use
"""

def run():

    # change name of input file
    file_source = input("What is the name of the input file? \n")
    data = np.fromfile("/Users/Mervin/" + file_location + "/" + file_source, dtype="uint64")

    # change name of output file
    file_dest = input("What is the name of the output file? \n")
    file_destination = "/Users/Mervin/" + file_location + "/" + file_dest

    
    function_mappings = {'binary_to_decimal': b2d_with_range,
                         'convert_binary': binary_convert,
                         'count_rate': countrate,
                         'g2': g2
                         }

    print("\n")
    print("List of functions available: \n")
    for key, value in function_mappings.items():
        print(key)
    print("\n")
    
    function_request = input("Please input the function you want to use \n")
    selected_function = function_mappings[function_request](data)
    print("\n")

    with open(file_destination, 'w') as writer:
        for item in selected_function:
            writer.write("%s\n" % item)
        writer.close()

    print("Done!\n")
    
    """
    print("The total computational time was:\n")
    print(toc-tic) + print(" nanoseconds")
    """




while True:
    run()
