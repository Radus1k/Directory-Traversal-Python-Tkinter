from fake_useragent import UserAgent


def genUA():
    """returns a fake random user-agent"""
    return str(UserAgent().random)
