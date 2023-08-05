
# list of tuple<DeviceClass class, Device impl class, tango device class name>
class_list = []

# list of tuple<DeviceClass name, tango device class name>
cpp_class_list = []

# list of DeviceClass objects, one for each registered device class
constructed_class = []

def get_classes():
    global class_list
    return class_list

def get_class(name):
    for klass_info in get_classes():
        if klass_info[2] == name:
            return klass_info
    return None

def get_cpp_classes():
    global cpp_class_list
    return cpp_class_list

def get_cpp_class(name):
    for klass_info in get_cpp_classes():
        if klass_info[1] == name:
            return klass_info
    return None

def get_constructed_classes():
    global constructed_class
    return constructed_class

def get_constructed_class(name):
    for klass in get_constructed_classes():
        if klass.get_name() == name:
            return klass
    return None

#
# A method to delete Tango classes from Python
#

def delete_class_list():
    global constructed_class
    if len(constructed_class) != 0:
       del(constructed_class[:])

#
# A generic class_factory method
#

def class_factory():
    global class_list
    global cpp_class_list

    if ((len(class_list) + len(cpp_class_list)) == 0):
        print 'Oups, no Tango class defined within this device server !!!'
        print 'Sorry, but I exit'
        sys.exit()

    # Call the delete_class_list function in order to clear the global
    # constructed class Python list. This is necessary only in case of
    # ServerRestart command
    delete_class_list()

    global constructed_class
    for class_info in class_list:
        device_class_class = class_info[0]
        tango_device_class_name = class_info[2]
        device_class = device_class_class(tango_device_class_name)
        constructed_class.append(device_class)

