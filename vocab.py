from tool.dictionary import translate
from tool.translate import connect
import json
import os
from dotenv import load_dotenv
load_dotenv()
from llama_index.core.llms import ChatMessage
import argparse
parser = argparse.ArgumentParser(description='处理方法选择。')
parser.add_argument('--method', type=str, choices=['local', 'azure', 'openai'], required=True, help='选择处理方法,参照README。')
args = parser.parse_args()
# 定义文件路径
words_path = '/Users/eva/Desktop/M-Agent/data/words/words.txt'
words_json_path = '/Users/eva/Desktop/M-Agent/data/words/vocab.json'
if args.method == 'local':
    """
    this needs you put the llm model and embed model in the same folder as this file -> checkpoint and change the local.py.
    """
    from load_model.local import get_llm,get_embed_model
    args.llm = get_llm("./checkpoint/chatglm3-6b")
    args.embed_model = get_embed_model("./checkpoint/bge-large-en-v1.5")
elif args.method == 'azure':
    from load_model.azure import get_llm,get_embed_model
    args.llm = get_llm(model_temperature = 0)
    args.embed_model = get_embed_model()
elif args.method == 'openai':
    from llama_index.llms.openai import OpenAI
    from llama_index.embeddings.openai import OpenAIEmbedding
    from load_model.local import get_embed_model
    API_SECRET_KEY = os.getenv("API_SECRET_KEY").encode().decode('utf-8')
    BASE_URL = os.getenv("BASE_URL")
    args.llm = OpenAI(api_key = API_SECRET_KEY, api_base = BASE_URL, temperature=0.1, model="gpt-3.5-turbo")
    args.embed_model = OpenAIEmbedding(api_key = API_SECRET_KEY, api_base = BASE_URL, model="text-embedding-3-small")
# 尝试读取vocab.json文件，如果不存在则创建一个空列表
try:
    with open(words_json_path, 'r', encoding='utf-8') as f:
        vocab_list = json.load(f)
except:
    vocab_list = []

trans = 0
no_trans = 0
from tqdm import tqdm
# 读取words.txt文件中的单词
with open(words_path, 'r', encoding='utf-8') as f:
    for word in tqdm(f):
        # 去除单词末尾的换行符
        word = word.strip()
        #print(word)
        
        # 检查单词是否已经存在于vocab_list中
        if any(item["word"] == word for item in vocab_list):
            continue  # 如果单词已存在，则跳过该单词
        
        # 翻译单词
        try:
            chinese_translation = translate(word)
            trans += 1
        except:
            try:
                chinese_translation = connect(word)
                trans += 1
            except:
                try:
                    chinese_translation = str(args.llm.chat([ChatMessage(content=f"解释一下该单词的意思:{word}")])).split('assistant:')[-1]
                except:
                    chinese_translation = "翻译失败"
                    no_trans += 1 
        
        # 将单词和翻译存入字典，并添加到列表中
        con = f"向我解释一下{word}怎么去记，简单的说出你认为最好的方法"
        if chinese_translation != "翻译失败":
            con = f"向我解释一下{word}「{chinese_translation}」怎么去记，简单的说出你认为最好的方法"
        helping_text = str(args.llm.chat([ChatMessage(content=f"简洁地说出记住这个单词{word}和它的意思的联系方式")])).split('assistant:')[-1]
        vocab_list.append({"word": word, "mean": chinese_translation, "memory": 'No', 'helping_text': helping_text})
        #break

print('翻译成功：', trans, '翻译失败：', no_trans,"总计", trans+no_trans)

# 将列表写入vocab.json文件
with open(words_json_path, 'w', encoding='utf-8') as f:
    json.dump(vocab_list, f, ensure_ascii=False, indent=4)

print("翻译完成，结果已保存到vocab.json文件。")


