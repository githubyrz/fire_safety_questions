# pushquestion.py
import json
import random
import requests
import os

def load_questions():
    """加载消防安全题库"""
    try:
        with open('fire_safety_questions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['fire_safety_questions']
    except FileNotFoundError:
        print("错误：找不到题库文件 fire_safety_questions.json")
        exit(1)
    except Exception as e:
        print(f"错误：加载题库失败 - {e}")
        exit(1)

def send_question():
    """发送题目到企业微信"""
    webhook_url = os.getenv('WECHAT_WEBHOOK_URL')
    if not webhook_url:
        print("错误：未设置企业微信Webhook地址")
        exit(1)
    
    questions = load_questions()
    print(f"成功加载 {len(questions)} 道题目")
    
    selected_question = random.choice(questions)
    print(f"选中题目: {selected_question['question'][:50]}...")
    
    # 构建消息内容
    msg_content = f"""## 🧯 消防安全每日一题

**分类：** {selected_question['category']}
**难度：** {selected_question['difficulty']}

**题目：** {selected_question['question']}

"""
    
    for option in selected_question['options']:
        msg_content += f"\n- {option}"
    
    msg_content += f"\n\n<font color=\"comment\">💡 思考后回复答案，稍后公布解析</font>"
    
    data = {
        "msgtype": "markdown",
        "markdown": {"content": msg_content}
    }
    
    try:
        response = requests.post(webhook_url, json=data, timeout=10)
        if response.json().get('errcode') == 0:
            print("✅ 题目发送成功！")
        else:
            print(f"❌ 发送失败: {response.text}")
            exit(1)
    except Exception as e:
        print(f"❌ 发送异常: {e}")
        exit(1)

if __name__ == "__main__":
    send_question()