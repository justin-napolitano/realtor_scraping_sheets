import os

def confirm_folder_structure(dictionary):
    for (k,v) in dictionary['tasks']['universal_vars']['directories'].items():
        
        try:
            dictionary['tasks']['confirm_folder_structure']['log']['trying'] = "{} at {}".format(k,v)
            #pass
            os.makedirs(v)
            dictionary['tasks']['confirm_folder_structure']['log']['success'] = "{} at {}".format(k,v)
        except FileExistsError:
            dictionary['tasks']['confirm_folder_structure']['log']['exception'] = "{} at {}".format(k,v)
            # directory already exists
            pass
    return True