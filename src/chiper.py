import hashlib

def get_note_id(text: str, salt: str):
	return hashlib.sha256(
		text.encode("UTF-8") + salt.encode("UTF-8")
	).hexdigest()