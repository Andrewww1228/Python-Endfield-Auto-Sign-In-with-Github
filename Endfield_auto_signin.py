#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: auto_sign.py
Author: sjtt2
cron: 0 30 8 * * *
new Env('终末地签到');
Update: 2026/2/20
"""
import hashlib
import hmac
import json
import os
import random
import time
from urllib import parse
import requests

try:
    import notify
except ImportError:
    class notify:
        @staticmethod
        def send(title, content): pass

# ========== 防封号配置 ==========
REQUEST_DELAY_MIN = 2
REQUEST_DELAY_MAX = 8
ACCOUNT_DELAY_MIN = 15
ACCOUNT_DELAY_MAX = 45
SIGN_DELAY_MIN = 3
SIGN_DELAY_MAX = 10

USER_AGENTS = [
    'Skland/1.0.0 (com.skland.grass; Android; SDK_INT 33; Build/TQ3A.230901.001)',
    'Skland/1.0.0 (com.skland.grass; Android; SDK_INT 34; Build/UP1A.231005.004)',
    'Skland/1.0.0 (com.skland.grass; Android; SDK_INT 35; Build/AP2A.240405.002)',
    'Skland/1.0.1 (skport; Android; SDK_INT 33; Build/TQ3A.230901.001)',
    'Skland/1.0.1 (skport; Android; SDK_INT 34; Build/UP1A.231005.004)',
]

skyland_notify = os.getenv('SKPORT_NOTIFY') or os.getenv('SKYLAND_NOTIFY') or ''
run_message: str = ''
account_num: int = 1
sign_token = ''
PLATFORM = '3'
VNAME = '1.0.0'

# Store results for Discord webhook
sign_results = []

SERVER_CONFIG = {
    "cn": {
        "name": "国服",
        "ENV_TOKEN": "SKYLAND_TOKEN",
        "MANUAL_TOKENS": "", # 如果你想直接写token就在这里填，多个用 ; 分隔
        "APP_CODE": "4ca99fa6b56cc2ba",
        "GRANT_URL": "https://as.hypergryph.com/user/oauth2/v2/grant",
        "CRED_URL": "https://zonai.skland.com/api/v1/user/auth/generate_cred_by_code",
        "BIND_URL": "https://zonai.skland.com/api/v1/game/player/binding",
        "SIGN_URL": "https://zonai.skland.com/api/v1/game/endfield/attendance",
    },
    "global": {
        "name": "Global",
        "ENV_TOKEN": "SKPORT_TOKEN",
        "MANUAL_TOKENS": "", # 如果你想直接写token就在这里填，多个用 ; 分隔
        "APP_CODE": "6eb76d4e13aa36e6",
        "GRANT_URL": "https://as.gryphline.com/user/oauth2/v2/grant",
        "CRED_URL": "https://zonai.skport.com/web/v1/user/auth/generate_cred_by_code",
        "BIND_URL": "https://zonai.skport.com/api/v1/game/player/binding",
        "SIGN_URL": "https://zonai.skport.com/web/v1/game/endfield/attendance",
    }
}

BASE_HEADER = {
    'cred': '',
    'User-Agent': random.choice(USER_AGENTS),
    'Accept-Encoding': 'gzip',
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

def get_random_header():
    return {**BASE_HEADER, 'User-Agent': random.choice(USER_AGENTS)}

def random_delay(min_sec=REQUEST_DELAY_MIN, max_sec=REQUEST_DELAY_MAX):
    time.sleep(random.uniform(min_sec, max_sec))

def send_notify(title, content):
    if not skyland_notify or skyland_notify.strip().lower() == 'false':
        return
    notify.send(title, content)

def generate_sign(token, path, body):
    t = str(int(time.time()))
    token = token.encode('utf-8')
    sign_header = {
        "platform": PLATFORM,
        "timestamp": t,
        "dId": "",
        "vName": VNAME
    }
    sign_header_str = json.dumps(sign_header, separators=(',', ':'))
    sign_str = path + body + t + sign_header_str
    hmac_hex = hmac.new(token, sign_str.encode('utf-8'), hashlib.sha256).hexdigest()
    md5_sign = hashlib.md5(hmac_hex.encode('utf-8')).hexdigest()
    return md5_sign, sign_header

def get_grant_code(token, cfg):
    random_delay(1, 3)
    try:
        t = json.loads(token)
        token = t['data']['content']
    except:
        pass
    resp = requests.post(
        cfg["GRANT_URL"],
        json={'appCode': cfg["APP_CODE"], 'token': token, 'type': 0},
        headers=get_random_header(),
        timeout=15
    ).json()
    if resp.get('status') != 0:
        raise Exception(f'获取grant code失败：{resp.get("msg", resp.get("message"))}')
    return resp['data']['code']

def get_cred(grant_code, cfg):
    global sign_token
    random_delay(1, 3)
    resp = requests.post(
        cfg["CRED_URL"],
        json={'code': grant_code, 'kind': 1},
        headers=get_random_header(),
        timeout=15
    ).json()
    if resp['code'] != 0:
        raise Exception(f'获取cred失败：{resp["message"]}')
    sign_token = resp['data']['token']
    return resp['data']['cred']

def login(token, cfg):
    grant = get_grant_code(token, cfg)
    cred = get_cred(grant, cfg)
    return cred

def get_endfield_roles(cred, cfg):
    random_delay(2, 5)
    parse_url = parse.urlparse(cfg["BIND_URL"])
    sign, sign_header = generate_sign(sign_token, parse_url.path, '')
    header = {
        'cred': cred,
        'platform': PLATFORM,
        'vName': VNAME,
        'timestamp': sign_header['timestamp'],
        'sk-language': 'en',
        'sign': sign,
        'Content-Type': 'application/json'
    }
    resp = requests.get(cfg["BIND_URL"], headers=header, timeout=15).json()
    if resp['code'] != 0:
        raise Exception(f'获取角色失败：{resp["message"]}')
    binding = None
    for app in resp['data']['list']:
        if app.get('appCode') == 'endfield' and app.get('bindingList'):
            binding = app['bindingList'][0]
            break
    if not binding:
        raise Exception('未绑定终末地角色')
    return binding

def do_daily_sign(cred, cfg):
    global run_message, account_num, sign_results
    try:
        roles = get_endfield_roles(cred, cfg)
        role = roles.get('defaultRole') or (roles.get('roles') and roles['roles'][0])
        role_str = f"3_{role['roleId']}_{role['serverId']}"

        random_delay(SIGN_DELAY_MIN, SIGN_DELAY_MAX)

        parse_url = parse.urlparse(cfg["SIGN_URL"])
        sign, sign_header = generate_sign(sign_token, parse_url.path, '')
        header = {
            'cred': cred,
            'platform': PLATFORM,
            'vName': VNAME,
            'timestamp': sign_header['timestamp'],
            'sk-language': 'en',
            'sign': sign,
            'sk-game-role': role_str,
            'Content-Type': 'application/json'
        }

        resp = requests.post(cfg["SIGN_URL"], headers=header, json=None, timeout=15).json()

        role_name = roles.get('defaultRole', {}).get('nickname', 'Unknown')
        channel = roles.get('defaultRole', {}).get('serverName', 'Unknown')
        uid = role.get('roleId', 'Unknown')

        if resp['code'] == 0:
            award_ids = resp['data'].get('awardIds', [])
            resource_map = resp['data'].get('resourceInfoMap', {})
            award_text = []
            if award_ids and resource_map:
                for award in award_ids:
                    award_id = award.get('id')
                    if award_id and award_id in resource_map:
                        res = resource_map[award_id]
                        award_text.append(f'{res["name"]} x{res.get("count", 1)}')
            reward_str = ', '.join(award_text) if award_text else 'Unknown'
            msg = f'[Account {account_num}] {role_name}({channel}) - Sign-in successful! Reward: {reward_str}'
            status = 'success'
        else:
            error_msg = resp.get("message", "Unknown error")
            if "请勿重复签到" in error_msg or "Please do not sign in again!" in error_msg:
                msg = f'[Account {account_num}] {role_name}({channel}) - Already signed in today'
                reward_str = 'Already claimed'
                status = 'already'
            else:
                msg = f'[Account {account_num}] {role_name}({channel}) - Sign-in failed: {error_msg}'
                reward_str = 'Failed'
                status = 'failed'

        # Save structured result for Discord webhook
        sign_results.append({
            'uid': uid,
            'name': role_name,
            'server': channel,
            'reward': reward_str,
            'status': status,
            'server_type': cfg['name']
        })

        run_message += msg + '\n'
        print(msg)

    except Exception as e:
        msg = f'[Account {account_num}] Error: {str(e)}'
        sign_results.append({
            'uid': 'N/A',
            'name': 'Unknown',
            'server': 'Unknown',
            'reward': 'Error',
            'status': 'failed',
            'server_type': cfg['name']
        })
        run_message += msg + '\n'
        print(msg)
    finally:
        account_num += 1

def main():
    global run_message, account_num
    print(f"Sign-in started {time.strftime('%Y-%m-%d %H:%M:%S')}")
    for cfg in SERVER_CONFIG.values():
        token_env = cfg.get("MANUAL_TOKENS") or os.getenv(cfg["ENV_TOKEN"], "")
        tokens = [t.strip() for t in token_env.split(";") if t.strip()]
        if not tokens:
            print(f"{cfg['name']} - No token configured, skipping...")
            continue
        for idx, token in enumerate(tokens, 1):
            print(f"\n===== Account {idx} =====")
            try:
                cred = login(token, cfg)
                do_daily_sign(cred, cfg)
            except Exception as e:
                err_msg = f"[{cfg['name']}] Account {account_num} error: {str(e)}"
                sign_results.append({
                    'uid': 'N/A', 'name': 'Unknown', 'server': 'Unknown',
                    'reward': 'Error', 'status': 'failed', 'server_type': cfg['name']
                })
                run_message += err_msg + '\n'
                print(err_msg)
                account_num += 1
            if idx < len(tokens):
                delay = random.uniform(ACCOUNT_DELAY_MIN, ACCOUNT_DELAY_MAX)
                print(f"Waiting {delay:.1f}s before next account...")
                time.sleep(delay)

    # Save results to file for the yml to pick up
    with open('result.json', 'w') as f:
        json.dump(sign_results, f)

    if run_message:
        send_notify('Endfield Sign-in Result', run_message)
    print(f"\nDone - {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nSummary:\n{run_message}")

if __name__ == "__main__":
    main()