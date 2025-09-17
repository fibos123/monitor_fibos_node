import os
import sys
import json
import requests
import smtplib
import ssl
from email.mime.text import MIMEText
from email.header import Header
from dotenv import load_dotenv

def get_config():
    """从环境变量中获取所有配置并进行验证"""
    
    config = {
        "node_names": os.getenv("NODE_NAMES"),
        "api_url": os.getenv("API_URL"),
        "recipient_email": os.getenv("RECIPIENT_EMAIL"),
        "smtp_server": os.getenv("SMTP_SERVER"),
        "smtp_port": os.getenv("SMTP_PORT"),
        "mail_username": os.getenv("MAIL_USERNAME"),
        "mail_password": os.getenv("MAIL_PASSWORD"),
        
        "mail_from_name": os.getenv("MAIL_FROM_NAME"),
        "mail_subject": os.getenv("MAIL_SUBJECT"),
        "mail_body_template": os.getenv("MAIL_BODY_TEMPLATE"),
    }

    # 验证所有必要的环境变量是否都已设置
    required_vars = [
        "node_names", "api_url", "recipient_email", "smtp_server", 
        "smtp_port", "mail_username", "mail_password"
    ]
    missing_vars = [key for key in required_vars if not config[key]]
    if missing_vars:
        print(f"错误: 缺少以下必要的环境变量: {', '.join(missing_vars)}")
        sys.exit(1)

    # 将端口号转换为整数
    try:
        config["smtp_port"] = int(config["smtp_port"])
    except (ValueError, TypeError):
        print(f"错误: SMTP_PORT ('{config['smtp_port']}') 必须是一个有效的整数。")
        sys.exit(1)
        
    # 将节点名称字符串转换为列表
    config["nodes_to_check"] = [name.strip() for name in config["node_names"].split(',')]

    return config

def send_email_alert(config, abnormal_nodes_list):
    """发送邮件警报"""
    # 将节点列表转换为一个逗号分隔的字符串
    nodes_str = ", ".join(abnormal_nodes_list)
    
    # --- 修改：使用配置中的模板并替换占位符 ---
    # 使用 .format() 方法将 {abnormal_nodes} 替换为实际的节点列表字符串
    subject = config['mail_subject'].format(abnormal_nodes=nodes_str)
    body = config['mail_body_template'].format(abnormal_nodes=nodes_str)
    
    # 创建邮件对象
    msg = MIMEText(body, 'plain', 'utf-8')
    # 使用配置中的发件人显示名称
    msg['From'] = Header(config['mail_from_name'], 'utf-8')
    msg['To'] = Header(config['recipient_email'], 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')

    print(f"准备向 {config['recipient_email']} 发送邮件...")
    try:
        # 使用 SSL 连接 SMTP 服务器
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(config['smtp_server'], config['smtp_port'], context=context) as server:
            server.login(config['mail_username'], config['mail_password'])
            server.sendmail(config['mail_username'], [config['recipient_email']], msg.as_string())
        print("邮件发送成功！")
    except Exception as e:
        print(f"错误: 邮件发送失败: {e}")
        sys.exit(1)

# --- 其他函数 (fetch_node_data, find_abnormal_nodes, main) 保持不变 ---

def fetch_node_data(api_url):
    """从 API 获取并返回节点数据"""
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'User-Agent': 'GitHub-Actions-FIBOS-Monitor/1.0',
    }
    print(f"正在从 API ({api_url}) 获取节点数据...")
    try:
        response = requests.post(api_url, headers=headers, json={}, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"错误: API 请求失败，HTTP 状态码: {e.response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"错误: 网络请求失败: {e}")
    except json.JSONDecodeError:
        print("错误: API 返回的不是有效的 JSON 格式。")
    return None

def find_abnormal_nodes(all_node_data, nodes_to_check):
    """在 API 数据中查找指定节点的异常状态"""
    abnormal_nodes = []
    node_data_map = {node.get('name'): node for node in all_node_data if 'name' in node}
    print(f"开始检查以下节点: {', '.join(nodes_to_check)}")
    for node_name in nodes_to_check:
        node_info = node_data_map.get(node_name)
        if not node_info:
            print(f"警告: 在 API 数据中未找到节点 '{node_name}'。")
            continue
        status = node_info.get('abnormal', False)
        print(f"  - 节点 '{node_name}' 的 'abnormal' 状态为: {status}")
        if status is True:
            print(f"    -> 发现异常节点: {node_name}")
            abnormal_nodes.append(node_name)
    return abnormal_nodes

def main():
    """主执行函数"""
    load_dotenv()
    config = get_config()
    all_node_data = fetch_node_data(config['api_url'])
    if all_node_data is None or not isinstance(all_node_data, list):
        print("无法获取或解析节点数据，任务终止。")
        sys.exit(1)
    abnormal_nodes = find_abnormal_nodes(all_node_data, config['nodes_to_check'])
    if abnormal_nodes:
        print(f"发现异常节点列表: {', '.join(abnormal_nodes)}")
        send_email_alert(config, abnormal_nodes)
    else:
        print("所有被监控的节点状态正常，无需发送邮件。")

if __name__ == "__main__":
    main()