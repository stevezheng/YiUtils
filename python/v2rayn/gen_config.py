def gen(local_port, remote_port, count, ip, uuid, path):
    base_config = '''
allow-lan: true
dns:
  enable: true
  enhanced-mode: fake-ip
  fake-ip-range: 198.18.0.1/16
  default-nameserver:
    - 114.114.114.114
  nameserver:
    - https://doh.pub/dns-query
'''
    listeners_config = 'listeners:\n'
    proxies_config = 'proxies:\n'
    for i in range(0, count):
        listeners_config += f'  - name: mixed{i}\n    port: {local_port + i}\n    proxy: proxy{i}\n    type: mixed\n'
        proxies_config += f'  - name: proxy{i}\n    type: vmess\n    server: {ip}\n    port: {remote_port + i}\n    uuid: {uuid}\n    alterId: 0\n    cipher: auto\n    tls: false\n    network: ws\n    ws-opts: \n      path: {path}\n'
    config = base_config + listeners_config + proxies_config
    return config

if __name__ == "__main__":
    result = gen(30000, 30000, 300, '23.175.201.124', '8058b7b6-938f-4d68-9511-3b812624b300', '/ws')
    with open('config.yml', 'w') as f:
        f.write(result)
