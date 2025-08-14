from .base_state import State


class AnfitriaoState(State):
    """
    O estado central (Anfitrião). Classifica a intenção do usuário
    e decide para qual estado transicionar.
    """
    def handle_user_input(self, text: str):
        from .route_state import RouteState
        from .feedback_state import FeedbackState

        print("[AnfitriaoState]: Classificando intenção...")
        intent = self.assistant._classify_intent_with_llm(text)
        print(f"[AnfitriaoState]: Intenção classificada como: {intent}")

        if intent == 'solicitar_rota':
            self.assistant.transition_to(RouteState(self.assistant))
            self.assistant.state.handle_user_input(text)

        elif intent == 'feedback':
            self.assistant.transition_to(FeedbackState(self.assistant))
            self.assistant.state.handle_user_input(text)

        elif intent == 'conversacao_geral':
            system_prompt = (
                "Você é 'BusSense', um assistente de IA focado em transporte público. Sua personalidade é útil e profissional."
                "Siga estas regras RIGOROSAMENTE:\n"
                "1. Responda de forma direta e objetiva.\n"
                "2. Mantenha as respostas curtas, com no máximo duas frases.\n"
                "3. NUNCA use emojis, emoticons ou gírias.\n"
                "4. NUNCA faça perguntas pessoais como 'Tudo bem com você?'.\n\n"
                "Exemplo de resposta ideal para a entrada 'Olá':\n"
                "Olá! Sou o BusSense, seu assistente de transporte. Como posso ajudar com sua rota hoje?"
            )

            response = self.assistant.llm_client.chat_completion(
                system_prompt=system_prompt,
                user_prompt=text,
                temperature=0.4,
                max_tokens=60)

            print("Resposta do Assistente: ", response)
            self.assistant.tts.text = response
            self.assistant.tts.convert_to_speech()

        else: # intent == 'desconhecido'
            print("[AnfitriaoState]: Não foi possível determinar a intenção.")
            response = "Desculpe, não entendi. Pode repetir?"
            self.assistant.tts.text = response
            self.assistant.tts.convert_to_speech()
