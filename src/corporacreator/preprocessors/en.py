def en(client_id, sentence):
    """Cleans up the passed sentence, removing or reformatting invalid data.

    Args:
      client_id (str): Client ID of sentence's speaker
      sentence (str): Sentence to be cleaned up.

    Returns:
      (str): Cleaned up sentence. Returning None or a `str` of whitespace flags the sentence as invalid.
    """
    if client_id == "f2909ec9143e4ff4792b0ccb2e109da938c1c5bfc91641165b0fd32f6caf67ad234318233affcaa4117a36212440eae89dbf06c75e2cb9d4a19ddec3663044ac":
        sentence = sentence.replace("=", "equal to")
    if client_id == "3c8f07827758e9ce8070ed287139d6d3e6457c1c16dcb972edac76c4d4333dc9e9c428711237e2b34fa29f4d249287fd238ac884534e33075958233643bbd0a1":
        sentence = sentence.replace("C++", "C plus plus")
    ## collapse all apostrophe-like marks
    ## e.g. common_voice_en_18441344.mp3	‘I’m not a serpent!’ --> 'I'm not a serpent!'
    sentence = sentence.replace("’","'") # right-ticks --> apostrophes
    sentence = sentence.replace("‘","'") # left-ticks --> apostrophes
    ## Change em-dash to dash
    ## e.g. common_voice_en_18607891.mp3  Nelly, come here — is it morning? --> Nelly, come here – is it morning?
    sentence = sentence.replace("—","–")
    return sentence
