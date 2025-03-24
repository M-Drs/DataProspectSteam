import inspect
def my_function(x):
    frame = inspect.currentframe()

    # Extracting useful information from the current frame
    function_name = frame.f_code.co_name
    line_number = frame.f_lineno
    local_vars = frame.f_locals
    global_vars = frame.f_globals
    file_name = frame.f_code.co_filename
    code_line = inspect.getsource(frame).strip().split('\n')[-1]

    print(f"Function Name: {function_name}")
    print(f"Line Number: {line_number}")
    print(f"Local Variables: {local_vars}")
    print(f"Global Variables: {global_vars}")
    print(f"File Name: {file_name}")
    print(f"Code Context: {code_line}")

# Example usage
my_function(42)