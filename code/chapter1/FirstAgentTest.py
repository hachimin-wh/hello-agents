import yaml
from pathlib import Path
import os
import re
import requests
from openai import OpenAI

# ── 从 config.yaml 加载配置 ──
_config_path = Path(__file__).resolve().parents[3] / "config.yaml"
with open(_config_path) as f:
    _config = yaml.safe_load(f)
_model_cfg = _config["model"]
_amap_cfg = _config["amap"]


AGENT_SYSTEM_PROMPT = """
你是一个智能旅行助手。你的任务是分析用户的请求，并使用可用工具一步步地解决问题。

# 可用工具:
- `get_weather(city: str)`: 查询指定城市的实时天气。
- `get_attraction(city: str, keywords: str)`: 根据城市和关键词搜索推荐的旅游景点。

# 输出格式要求:
你的每次回复必须严格遵循以下格式，包含一对Thought和Action：

Thought: [你的思考过程和下一步计划]
Action: [你要执行的具体行动]

Action的格式必须是以下之一：
1. 调用工具：function_name(arg_name="arg_value")
2. 结束任务：Finish[最终答案]

# 重要提示:
- 每次只输出一对Thought-Action
- Action必须在同一行，不要换行
- 当收集到足够信息可以回答用户问题时，必须使用 Action: Finish[最终答案] 格式结束

请开始吧！
"""


def get_weather(city: str) -> str:
    """通过高德天气 API 查询指定城市的实时天气。"""
    try:
        # 地理编码：城市名 → adcode
        geo_url = f"https://restapi.amap.com/v3/geocode/geo?key={_amap_cfg['api_key']}&address={city}"
        geo_resp = requests.get(geo_url).json()
        if geo_resp.get("status") != "1" or not geo_resp.get("geocodes"):
            return f"错误：无法找到城市 '{city}'"
        adcode = geo_resp["geocodes"][0]["adcode"]

        # 天气查询
        weather_url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={_amap_cfg['api_key']}&city={adcode}&extensions=base"
        weather_resp = requests.get(weather_url).json()
        if weather_resp.get("status") != "1" or not weather_resp.get("lives"):
            return "错误：查询天气失败"

        live = weather_resp["lives"][0]
        return f"{live['city']}当前天气：{live['weather']}，气温{live['temperature']}°C，{live['winddirection']}风{live['windpower']}级，湿度{live['humidity']}%"
    except Exception as e:
        return f"错误：查询天气时遇到问题 - {e}"


def get_attraction(city: str, keywords: str) -> str:
    """通过高德 POI 搜索查询指定城市的旅游景点。"""
    try:
        url = f"https://restapi.amap.com/v3/place/text?key={_amap_cfg['api_key']}&keywords={keywords}&city={city}&offset=5"
        resp = requests.get(url).json()
        if resp.get("status") != "1":
            return "错误：搜索景点失败"

        pois = resp.get("pois", [])
        if not pois:
            return f"抱歉，在{city}没有找到与'{keywords}'相关的景点。"

        lines = [f"在{city}搜索'{keywords}'，为您找到以下景点："]
        for poi in pois[:5]:
            name = poi["name"]
            addr = poi.get("address", "未知地址")
            rating = poi.get("biz_ext", {}).get("rating", "暂无评分")
            lines.append(f"- {name}（{addr}，评分：{rating}）")
        return "\n".join(lines)
    except Exception as e:
        return f"错误：搜索景点时出现问题 - {e}"


available_tools = {
    "get_weather": get_weather,
    "get_attraction": get_attraction,
}


class OpenAICompatibleClient:
    def __init__(self, model: str, api_key: str, base_url: str):
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def generate(self, prompt: str, system_prompt: str) -> str:
        print("正在调用大语言模型...")
        try:
            messages = [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt}
            ]
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=False
            )
            answer = response.choices[0].message.content
            print("大语言模型响应成功。")
            return answer
        except Exception as e:
            print(f"调用LLM API时发生错误: {e}")
            return "错误：调用语言模型服务时出错。"


# --- 1. 配置LLM客户端 ---
llm = OpenAICompatibleClient(
    model=_model_cfg["model"],
    api_key=_model_cfg["api_key"],
    base_url=_model_cfg["base_url"]
)

# --- 2. 初始化 ---
user_prompt = "你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。"
prompt_history = [f"用户请求: {user_prompt}"]

print(f"用户输入: {user_prompt}\n" + "=" * 40)

# --- 3. 运行主循环 ---
for i in range(5):
    print(f"--- 循环 {i + 1} ---\n")

    full_prompt = "\n".join(prompt_history)

    llm_output = llm.generate(full_prompt, system_prompt=AGENT_SYSTEM_PROMPT)
    match = re.search(
        r'(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)',
        llm_output, re.DOTALL
    )
    if match:
        truncated = match.group(1).strip()
        if truncated != llm_output.strip():
            llm_output = truncated
            print("已截断多余的 Thought-Action 对")
    print(f"模型输出:\n{llm_output}\n")
    prompt_history.append(llm_output)

    action_match = re.search(r"Action: (.*)", llm_output, re.DOTALL)
    if not action_match:
        observation = "错误: 未能解析到 Action 字段。请确保你的回复严格遵循 'Thought: ... Action: ...' 的格式。"
        observation_str = f"Observation: {observation}"
        print(f"{observation_str}\n" + "=" * 40)
        prompt_history.append(observation_str)
        continue
    action_str = action_match.group(1).strip()

    if action_str.startswith("Finish"):
        final_answer = re.match(r"Finish\[(.*)\]", action_str).group(1)
        print(f"任务完成，最终答案: {final_answer}")
        break

    tool_name = re.search(r"(\w+)\(", action_str).group(1)
    args_str = re.search(r"\((.*)\)", action_str).group(1)
    kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str))

    if tool_name in available_tools:
        observation = available_tools[tool_name](**kwargs)
    else:
        observation = f"错误：未定义的工具 '{tool_name}'"

    observation_str = f"Observation: {observation}"
    print(f"{observation_str}\n" + "=" * 40)
    prompt_history.append(observation_str)
