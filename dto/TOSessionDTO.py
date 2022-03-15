from trafficops import TOSession


class TOSessionDTO:
    def __init__(self, session: TOSession):
        self.__session = session

    def get_session(self) -> TOSession:
        return self.__session
