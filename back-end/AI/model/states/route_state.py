from .base_state import State
# from .anfitriao_state import AnfitriaoState

class RouteState(State):
    """ Estado para processar uma solicitação de rota. """
    def handle_user_input(self, text: str):
        from .anfitriao_state import AnfitriaoState

        print("[RouteState]: Processando solicitação de rota...")
        log_data = {'user_query': text}

        # Extrai origin e destination pela query
        locations = self.assistant._extract_location_from_text(text)
        # Filtra no banco pela origin e destination
        filtered_data, _ = self.assistant.route_searcher.search(locations['origin'], locations['destination'])
        print(filtered_data)
        # Gera o prompt para o modelo Llama
        prompt = self.assistant._generate_route_prompt(filtered_data)

        # Obtém a resposta do LLM
        response_text = self.assistant.llm_client.chat_completion(system_prompt=prompt, user_prompt=text, temperature=0.2)

        print(f"[DEBUG]: IA Output: {response_text}")

        self.assistant.tts.text = response_text
        self.assistant.tts.convert_to_speech()

        log_data['assistant_response'] = response_text
        self.assistant.last_interaction_id = self.assistant.logger.log(log_data)

        print("[RouteState]: Mudando para estado Anfitrião.")
        self.assistant.transition_to(AnfitriaoState(self.assistant))
