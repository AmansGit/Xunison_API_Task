def key_validation(request_json):
	status = True
	msg = ""
	if "name" not in request_json:
		status = False
		msg += "Key 'name' is missing, "
	
	if "description" not in request_json:
		status = False
		msg += "Key 'description' is missing, "
	
	if "date_of_release" not in request_json:
		status = False
		msg += "Key 'date_of_release' is missing"

	return status, msg