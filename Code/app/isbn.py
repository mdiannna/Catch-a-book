
def filter_raw_ISBN(raw_text):
	isbn = ""
	print "raw_isbn:", raw_text
	for i in raw_text:
		if i.isdigit():
			isbn += i
	print "isbn adter filtering:", isbn
	return isbn


def check_ISBN(text):
	if not text:
		return False

	# ISBN-13 standard - after 1 Jan 2007
	if len(text) == 13 and text.isdigit():
		return True
	
	# ISBN-10 standard - before 1 Jan 2007
	if len(text) == 10 and text.isdigit():
		return True

	
	return False