import json
import uuid
import IPy

def get_ip_list(begin_ip, count, netmask):
    ip_list = '' #用来存放生成的IP地址
    begin_ip = IPy.IP(begin_ip)
    ip_list += str(begin_ip) + '\n' #将第一个地址放入ip_列表中
    if begin_ip.version() == 4:
        for i in range(count):
            ip = IPy.IP(begin_ip)
            new_ip = IPy.IP(ip.ip + 2 ** (32 - netmask))
            begin_ip =  str(new_ip)
            ip_list += begin_ip + '\n'
    else:
        for i in range(count):
            ipv6 = IPy.IP(begin_ip)
            new_ipv6 = IPy.IP(ipv6.ip + 2 ** (128 - netmask))
            begin_ip =  str(new_ipv6)
            ip_list += begin_ip + '\n'
    return ip_list

def generate_xray_json(start_port=20000, begin_ipv6='2401:b60:e00e:7121::', count=3, netmask=127):
    # 基础配置
    config = {
        "api": {
            "services": ["HandlerService", "LoggerService", "StatsService"],
            "tag": "api"
        },
        "stats": {},
        "policy": {
            "levels": {
                "0": {
                    "handshake": 10,
                    "connIdle": 100,
                    "uplinkOnly": 2,
                    "downlinkOnly": 3,
                    "statsUserUplink": True,
                    "statsUserDownlink": True,
                    "bufferSize": 10240
                }
            },
            "system": {
                "statsInboundDownlink": True,
                "statsInboundUplink": True
            }
        }
    }

    # 获取IPv6列表
    ipv6_list = get_ip_list(begin_ipv6, count, netmask).split('\n')[:-1]

    # 生成UUID
    user_id = str(uuid.uuid4())

    # 基础入站配置
    inbounds = [{
        "listen": "127.0.0.1",
        "port": 62789,
        "protocol": "dokodemo-door",
        "settings": {"address": "127.0.0.1"},
        "tag": "api"
    }]

    # 初始化出站和路由规则
    outbounds = [{"protocol": "blackhole", "settings": {}, "tag": "blocked"}]
    routing_rules = [
        {"inboundTag": ["api"], "outboundTag": "api", "type": "field"},
        {"ip": ["geoip:private"], "outboundTag": "blocked", "type": "field"},
        {"outboundTag": "blocked", "protocol": ["bittorrent"], "type": "field"}
    ]

    # 生成配置
    for i in range(count):
        tag = f"tag_{i+1}"
        port = start_port + i

        # 入站配置
        inbound = {
            "port": port,
            "protocol": "vmess",
            "tag": tag,
            "settings": {
                "clients": [{"id": user_id}]
            },
            "streamSettings": {
                "network": "ws",
                "wsSettings": {"path": "/ws"}
            }
        }
        inbounds.append(inbound)

        # 出站配置
        outbound = {
            "sendThrough": ipv6_list[i],
            "protocol": "freedom",
            "tag": tag
        }
        outbounds.append(outbound)

        # 路由规则
        routing_rules.append({
            "type": "field",
            "inboundTag": tag,
            "outboundTag": tag
        })

    # 组装完整配置
    config["inbounds"] = inbounds
    config["outbounds"] = outbounds
    config["routing"] = {"rules": routing_rules}

    # 写入JSON文件
    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    generate_xray_json(
        start_port=30000,
        begin_ipv6='2401:b60:e00e:7121::2',
        count=300,
        netmask=127
    )