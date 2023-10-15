import fire
from llama_cpp import Llama
from Summariz_ru import summarization 


def get_text(text = """МультНайтКлип. Удалите маркетплейсы,'Специальное включение с «черной пятницы» от мужчин! МультНайтКлип от юмористического нарисованного вечернего шоу «МультНайтШоу', где обсуждаются актуальные новости страны и мира. Cмотрите «МультНайтШоу» каждую пятницу!"""):
    summarization_text = summarization(text)
    default_text = text
    return summarization_text, default_text

Lama_text = " "
def Generate(sentence):
    
    SYSTEM_PROMPT = "Ты — Сайга, русскоязычный автоматический ассистент. Ты разговариваешь с людьми и помогаешь им."
    SYSTEM_TOKEN = 1788
    USER_TOKEN = 1404
    BOT_TOKEN = 9225
    LINEBREAK_TOKEN = 13

    ROLE_TOKENS = {
        "user": USER_TOKEN,
        "bot": BOT_TOKEN,
        "system": SYSTEM_TOKEN
    }


    def get_message_tokens(model, role, content):
        message_tokens = model.tokenize(content.encode("utf-8"))
        message_tokens.insert(1, ROLE_TOKENS[role])
        message_tokens.insert(2, LINEBREAK_TOKEN)
        message_tokens.append(model.token_eos())
        return message_tokens


    def get_system_tokens(model):
        system_message = {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
        return get_message_tokens(model, **system_message)


    
    questions = ["Действие должно очень кратко описывать самые важные действия действие или событие которое происходит с центральным объектом и его взаимодействие в тексте.",
                "Напиши предметы которые есть в тексте предметы (не живые) по 1 - 2 слова через запятую",
                "Объект должен найти в тексте тех кто находится на сцене и перечилси их"]
    def interact(
        model_path = "model-q8_0.gguf",
        n_ctx=2000,
        top_k=30,
        top_p=0.9,
        temperature=0.2,
        repeat_penalty=1.1
    ):
        global Lama_text
        model = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            n_parts=1,
        )

        system_tokens = get_system_tokens(model)
        tokens = system_tokens
        model.eval(tokens)
        between =""
  
        for quest in questions:
            user_message = f"""User:
                        Используй следующий формат с обязательными правилами для выполнения использовать слова только из текста.
                        {quest}

        Текст:
        {sentence}"""
            message_tokens = get_message_tokens(model=model, role="user", content=user_message)
            role_tokens = [model.token_bos(), BOT_TOKEN, LINEBREAK_TOKEN]
            tokens += message_tokens + role_tokens
            generator = model.generate(
                tokens,
                top_k=top_k,
                top_p=top_p,
                temp=temperature,
                repeat_penalty=repeat_penalty
            )
            for token in generator:
                token_str = model.detokenize([token]).decode("utf-8", errors="ignore")
                tokens.append(token)
                if token == model.token_eos():
                    break
                between += token_str
            print(between)
            Lama_text += "\n"+between
            between = " "
        #print("LLama== ", Lama_text)


    fire.Fire(interact)

    return Lama_text


#res = Generate(sentence = get_text()[0])
#print(res)

