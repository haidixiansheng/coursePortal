INITIAL_RATING = 200

def object_delta_rating():
	return 10
	
def vote_up_delta_rating():
	return 1
	
def vote_down_delta_rating():
	return -1
	
def content_object_delta_rating():
	return object_delta_rating()

	
def topic_object_delta_rating():
	return 0