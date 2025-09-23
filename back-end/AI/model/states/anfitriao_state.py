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
        intent_svm, conf = self.assistant.intent_svm.predict(text)
        print(f"[AnfitriaoState]: SVM -> {intent_svm} ({conf:.2f})")

        if conf < self.assistant.intent_svm.threshold:
            # 2) fallback LLM
            intent = self.assistant._classify_intent_with_llm(text)  # já existe
            source = "llm"
        else:
            intent = intent_svm
            source = "svm"


        print(f"[AnfitriaoState]: Intenção final: {intent} (source={source})")
        log_data = {"user_text": text, "predicted_intent": intent, "source": source}
        self.assistant.last_interaction_id = self.assistant.logger.log(log_data)


        if intent == 'solicitar_rota':
            self.assistant.transition_to(RouteState(self.assistant))
            self.assistant.state.handle_user_input(text)

        elif intent == 'feedback':
            self.assistant.transition_to(FeedbackState(self.assistant))
            self.assistant.state.handle_user_input(text)

        elif intent == 'conversacao_geral':
            #TODO: Rechecar prompt
            system_prompt = (
                "Você é 'BusSense', um assistente de IA focado em transporte público. Sua personalidade é útil e profissional."
                "Siga estas regras RIGOROSAMENTE:\n"
                "1. Responda de forma direta e objetiva.\n"
                "2. Mantenha as respostas curtas, com no máximo duas frases.\n"
                "3. NUNCA use emojis, emoticons ou gírias.\n"
                "4. NUNCA faça perguntas pessoais como 'Tudo bem com você?'.\n\n"
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
