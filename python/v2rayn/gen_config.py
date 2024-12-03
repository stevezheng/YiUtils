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
        listeners_config += f'  - name: mixed{local_port + i}\n    port: {local_port + i}\n    proxy: proxy{local_port + i}\n    type: mixed\n'
        proxies_config += f'  - name: proxy{local_port + i}\n    type: vmess\n    server: {ip}\n    port: {remote_port + i}\n    uuid: {uuid}\n    alterId: 0\n    cipher: auto\n    tls: false\n    network: ws\n    ws-opts: \n      path: {path}\n'
    config = base_config + listeners_config + proxies_config
    return config, listeners_config, proxies_config

if __name__ == "__main__":
    config, listeners_config, proxies_config = gen(55000, 55000, 300, '89.58.62.25', '45ba725f-0685-41fa-9ac4-b1bd98a80f3a', '/ws')
    pre = 'de'
    with open(pre + '_config.yml', 'w') as f:
        f.write(config)
    with open(pre+'_listeners_config.yml', 'w') as f:
        f.write(listeners_config)
    with open(pre+'_proxies_config.yml', 'w') as f:
        f.write(proxies_config)
