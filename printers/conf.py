'''config helper functions'''
def supported_protocols():
    '''List of all supported printer protocols'''
    return [("ipp", "ipp"), \
			("socket", "socket"), \
			("lpd", "lpd"), \
			("http", "http"),]
