import json
import time
from collections import defaultdict
from pathlib import Path


def generate_chrome_bookmarks(grouped, output_dir='output', group_size=10):
    """
    为每个 creator_id 生成单独的 Chrome 书签 HTML 文件
    每 group_size 个书签为一组
    """
    timestamp = int(time.time())
    output_path = Path(output_dir)

    for creator_id, channels in grouped.items():
        records = list(channels.values())
        html_lines = [
            '<!DOCTYPE NETSCAPE-Bookmark-file-1>',
            '<!-- This is an automatically generated file.',
            '     It will be read and overwritten.',
            '     DO NOT EDIT! -->',
            '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">',
            '<TITLE>Bookmarks</TITLE>',
            '<H1>Bookmarks</H1>',
            '<DL><p>'
        ]

        # 按每 group_size 个为一组
        for i in range(0, len(records), group_size):
            group_start = i + 1
            group_end = min(i + group_size, len(records))
            group_records = records[i:group_end]

            # 创建分组文件夹
            html_lines.append(f'    <DT><H3>Channels {group_start}-{group_end}</H3>')
            html_lines.append('    <DL><p>')

            # 添加该组的书签
            for record in group_records:
                url = f"https://www.youtube.com/channel/{record['channel_id']}"
                name = record['name']
                html_lines.append(f'        <DT><A HREF="{url}" ADD_DATE="{timestamp}">{name}</A>')

            html_lines.append('    </DL><p>')

        html_lines.append('</DL><p>')

        output_file = output_path / f'creator_{creator_id}.html'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(html_lines))

        print(f'Created: {output_file}')





def process_accounts(input_file='accounts.json'):
    """
    处理 accounts.json 文件：
    1. channel_id 去重（只保留唯一的 channel_id）
    2. 按 creator_id 分组
    3. 输出多个文件
    """
    # 读取数据
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f'Total records: {len(data)}')

    # 按 creator_id 分组，同时保证 channel_id 唯一
    grouped = defaultdict(dict)  # {creator_id: {channel_id: record}}

    for item in data:
        creator_id = item['creator_id']
        channel_id = item.get('channel_id', '')

        # 跳过 channel_id 为空的记录
        if not channel_id:
            continue

        # 只保留第一次出现的记录（去重）
        if channel_id not in grouped[creator_id]:
            grouped[creator_id][channel_id] = item

    # 统计去重后的数据
    total_after_dedup = sum(len(channels) for channels in grouped.values())
    print(f'Total records after deduplication: {total_after_dedup}')

    # 输出文件
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)

    for creator_id, channels in grouped.items():
        output_file = output_dir / f'creator_{creator_id}.json'
        records = list(channels.values())

        # 添加 url 字段
        for record in records:
            record['url'] = f"https://www.youtube.com/channel/{record['channel_id']}"

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)

        print(f'Created: {output_file} ({len(records)} records)')

    print(f'\nTotal output files: {len(grouped)}')

    # 生成 Chrome 书签文件
    generate_chrome_bookmarks(grouped)


if __name__ == '__main__':
    process_accounts()
