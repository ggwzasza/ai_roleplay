from openai import OpenAI


class APIClient:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self._clients = {}

    def _get_client(self, api_config):
        api_id = api_config.get('id', '')
        if api_id not in self._clients:
            base_url = api_config.get('url', '').rstrip('/')
            if base_url.endswith('/v1'):
                pass
            self._clients[api_id] = OpenAI(
                api_key=api_config.get('api_key', ''),
                base_url=base_url
            )
        return self._clients[api_id]

    def build_system_prompt(self, character_id, chat_data, other_character_outputs=None):
        character = self.data_manager.get_character(character_id)
        if not character:
            return ''

        api_id = character.get('api_id')
        api_config = self.data_manager.get_api(api_id) if api_id else None

        parts = []

        if api_config and api_config.get('prefix_prompt'):
            parts.append(api_config['prefix_prompt'])

        if chat_data and chat_data.get('prefix_prompt'):
            parts.append(chat_data['prefix_prompt'])

        if api_config and api_config.get('system_prompt'):
            parts.append(api_config['system_prompt'])

        char_desc = self._build_character_description(character)
        parts.append(char_desc)

        user_char = self.data_manager.user_character
        if user_char and user_char.get('prompt'):
            parts.append(f"用户角色设定:\n{user_char['prompt']}")

        if chat_data and chat_data.get('macro_prompt'):
            parts.append(f"世界背景与宏观设定:\n{chat_data['macro_prompt']}")

        if other_character_outputs:
            context_lines = ["当前场景中其他角色已经做出的反应:"]
            for char_name, output in other_character_outputs:
                context_lines.append(f"  {char_name}: {output}")
            parts.append('\n'.join(context_lines))

        role_constraint = (
            f"【重要规则】你必须且只能扮演角色「{character.get('name', '未知')}」，"
            "不得扮演任何其他角色。你的所有回复都必须以该角色的身份、性格、言谈风格进行。"
            "不要替用户做决定或描述用户的行为。"
        )
        parts.append(role_constraint)

        return '\n\n'.join(parts)

    def _build_character_description(self, character):
        fields = {
            'name': '名字',
            'age': '年龄',
            'race': '种族',
            'body': '身材',
            'experience': '经历',
            'personality': '性格',
            'speech_style': '言谈风格',
            'habits': '癖好'
        }
        lines = ["角色设定:"]
        for key, label in fields.items():
            val = character.get(key, '')
            if val:
                lines.append(f"  {label}: {val}")
        return '\n'.join(lines)

    def build_messages(self, chat_id, character_id, user_input,
                       other_character_outputs=None):
        chat = self.data_manager.get_chat(chat_id)
        if not chat:
            return []

        system_prompt = self.build_system_prompt(
            character_id, chat, other_character_outputs
        )

        memory_count = chat.get('memory_count', 20)
        messages = chat.get('messages', [])

        relevant = messages[-memory_count:] if len(messages) > memory_count else messages

        result = [{'role': 'system', 'content': system_prompt}]

        for msg in relevant:
            if msg['role'] == 'user':
                result.append({'role': 'user', 'content': msg['content']})
            elif msg['role'] == 'assistant':
                char_id = msg.get('character_id')
                char_name = ''
                if char_id:
                    char = self.data_manager.get_character(char_id)
                    if char:
                        char_name = char.get('name', '')
                if char_name:
                    result.append({
                        'role': 'assistant',
                        'content': f"【{char_name}】{msg['content']}"
                    })
                else:
                    result.append({'role': 'assistant', 'content': msg['content']})

        if user_input:
            result.append({'role': 'user', 'content': user_input})

        return result

    def send_message(self, chat_id, character_id, user_input, stream=True,
                     other_character_outputs=None):
        chat = self.data_manager.get_chat(chat_id)
        if not chat:
            return None

        character = self.data_manager.get_character(character_id)
        if not character:
            return None

        api_id = character.get('api_id')
        api_config = self.data_manager.get_api(api_id) if api_id else None

        if not api_config:
            return None

        messages = self.build_messages(
            chat_id, character_id, user_input, other_character_outputs
        )

        client = self._get_client(api_config)

        model = api_config.get('model', 'deepseek-chat')

        try:
            if stream:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    stream=True,
                    temperature=api_config.get('temperature', 0.8),
                    max_tokens=api_config.get('max_tokens', 2048)
                )
                return self._stream_response(response)
            else:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    stream=False,
                    temperature=api_config.get('temperature', 0.8),
                    max_tokens=api_config.get('max_tokens', 2048)
                )
                return response.choices[0].message.content
        except Exception as e:
            return self._error_response(str(e))

    def _stream_response(self, response):
        def generator():
            try:
                for chunk in response:
                    if chunk.choices and chunk.choices[0].delta:
                        content = chunk.choices[0].delta.content
                        if content:
                            yield content
            except Exception as e:
                yield f"[API错误] {str(e)}"
        return generator()

    def _error_response(self, error_msg):
        def error_gen():
            yield f"[API错误] {error_msg}"
        return error_gen()

    def clear_client_cache(self, api_id=None):
        if api_id:
            self._clients.pop(api_id, None)
        else:
            self._clients.clear()
