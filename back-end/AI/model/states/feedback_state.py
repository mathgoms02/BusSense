from .base_state import State


class FeedbackState(State):
    """ Estado para aguardar e processar o feedback do usuário."""
    def handle_user_input(self, text: str):
        from .anfitriao_state import AnfitriaoState


        print("[FeedbackState]: Processando feedback...")
        # Usa o agente classificador para entender a intenção
        intent_subtype = self.assistant.feedback_classifier._classify_intent(text)
        print(f"Intenção detectada: {intent_subtype}")

        if self.assistant.last_interaction_id:
            self.assistant.feedback_classifier._handle_intent(self.assistant.last_interaction_id, intent_subtype, text)
        else:
            print("Registrando feedback geral do usuário.")
            self.assistant.logger.log({'user_feedback_geral': text})

        response = "Obrigado pelo seu feedback!"
        print("Resposta do Assistente:", response)
        self.assistant.tts.text = response
        self.assistant.tts.convert_to_speech()

        print("[FeedbackState]: Retornando ao estado anfitrião.")
        self.assistant.transition_to(AnfitriaoState(self.assistant))
