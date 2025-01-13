# Code for activation records and procedure structures.

class ActivationRecord:
    def __init__(self, access_link, local_variables):
        self.access_link = access_link                      # Tuple with actual parameters x and y (global variables)
        self.local_variables = local_variables              # Hashmap with procedure parameters a and b

    # Values for local variables are set to x and y from access_link, so they know that f.ex a has same value as x if they are in
    # the same position
    def set_local_variables(self):
        index = 0
        for var in self.local_variables.keys():
            self.local_variables[var] = self.access_link[index]
            index += 1

    def get_global_variables(self):
        return self.access_link

    # Returns value of local variable in statement
    def get_local_variable(self, key):
        # Checking if a/b is in local_variables, if not, then key is x/y so we check the global variables
        if key in self.local_variables.keys():
            return self.local_variables[key]
        else:
            for var in self.access_link:
                if var == key:
                    return var


# Skeleton for procedures. I tried writing it so it resembles the AST. Needed a way to access the instance variables.
class Procedure:
    def __init__(self, identifier, proc_body, proc_params):
        self.identifier = identifier
        self.proc_body = proc_body
        self.proc_params = proc_params     # hashmap to be sent to Activation Record to store value of actual parameters, x and y

    def get_identifier(self):
        return self.identifier

    def get_proc_params(self):
        return self.proc_params

    def get_proc_body(self):
        return self.proc_body
