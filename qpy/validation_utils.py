def validate_number_params_not_negative(function_name, **args):
    for param_name, value in args.items():
        if value is None:
            continue
        elif not isinstance(value, (int, float)):
            raise ValueError(f"Invalid type for parameter '{param_name}' in function '{function_name}'. Expected a number.")
        elif value < 0:
            raise ValueError(f"Invalid negative value for parameter '{param_name}' in function '{function_name}'.")

def validate_object_params_not_none(function_name, **args):
    for param_name, value in args.items():
        if value is None:
            raise ValueError(f"Invalid 'None' value for parameter '{param_name}' in function '{function_name}'.")

def validate_number_params_not_negative_and_not_none(function_name, **args):
    validate_object_params_not_none(function_name, **args)
    validate_number_params_not_negative(function_name, **args)