from datetime import datetime
import requests
import os,dotenv
dotenv.load_dotenv()
tomorrow_api = os.getenv("TOMORROW_API")
city = os.getenv("LOCATION")
def try_multi_decode(subject):
    if type(subject) == str:
        return subject
    try:
        # 尝试使用 UTF-8 编码解码
        subject = subject.decode('utf-8')
    except UnicodeDecodeError:
        try:
            # 如果 UTF-8 失败，尝试使用 Latin-1 编码解码
            subject = subject.decode('latin1')
        except UnicodeDecodeError:
            try:
                # 如果 Latin-1 也失败，尝试使用 ASCII 编码解码
                subject = subject.decode('ascii', 'ignore')  # 'ignore' 将忽略无法解码的字节
            except Exception as e:
                # 如果所有尝试都失败，输出错误信息
                print(f"无法解码 subject: {e}")
    return subject

def get_current_time():
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time
def get_weather(api_key, city):
    # OpenWeatherMap API的URL
    current_date = datetime.now().strftime('%Y-%m-%d')
    url = f"https://api.tomorrow.io/v4/weather/forecast?location={city}&apikey={api_key}"
    print(url)
    # 发送GET请求
    response = requests.get(url)
    data_h = []
    # 检查响应状态码
    if response.status_code == 200:
        # 解析JSON响应
        data = response.json()
        # 提取天气信息
        h_data = data['timelines']['hourly']
        for hour_data in h_data:
            time = datetime.strptime(hour_data['time'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M:%S')
            if time.startswith(current_date):
                temperature = hour_data['values']['temperature']
                precipitation_probability = hour_data['values']['precipitationProbability']
                data_h.append(f"时间: {time}, 温度: {temperature}°C, 降水概率: {precipitation_probability}%")
    else:
        # 如果请求失败，返回错误信息
        return "无法获取天气信息"
    print("OK,the weather is following...\n")
    for i in data_h:
        print(i)
    return data_h

if __name__ == "__main__":
    get_current_time()
    response = get_weather(tomorrow_api, city)
    print(response)