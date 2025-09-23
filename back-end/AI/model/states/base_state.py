class State:
    """ Classe base para estados do assistente. """
    def __init__(self, assistant):
        self.assistant = assistant

    def handle_user_input(self, text: str):
        """ Método que será implementado por cada estado para lidar com o input. """
        raise NotImplementedError("Subclasses must implement this method.")
