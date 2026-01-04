import os
import re

SOURCE_BASE = r"d:\Backup\Documents\Website\REDE\poprede.top"
DEST_BASE = r"d:\WORK PROGRAM\DANGEROUS WEBSITE\agents"

def extract_info(content):
    # Extract WhatsApp number
    wa = re.search(r'href="[^"]*wa\.me/(\d+)"', content)
    
    # Extract Telegram Personal
    # Looks for t.me link in an anchor that contains "Telegram" text
    # We use (?:(?!</a>).)*? to ensure we don't cross into another anchor tag
    tg = re.search(r'<a[^>]+href="([^"]*t\.me/[^"]+)"[^>]*>(?:(?!</a>).)*?<span>Telegram</span>', content, re.DOTALL | re.IGNORECASE)
    
    # Extract Telegram Group
    # Looks for t.me link in an anchor that contains "Grupo" text
    group = re.search(r'<a[^>]+href="([^"]*t\.me/[^"]+)"[^>]*>(?:(?!</a>).)*?<span>Grupo</span>', content, re.DOTALL | re.IGNORECASE)
    
    return {
        'wa': wa.group(1) if wa else None,
        'tg': tg.group(1) if tg else None,
        'group': group.group(1) if group else None
    }

def update_agent(agent_name):
    source_path = os.path.join(SOURCE_BASE, agent_name, "index.html")
    dest_path = os.path.join(DEST_BASE, agent_name, "index.html")
    
    if not os.path.exists(source_path):
        # Some folders might not be agents or might be missing index.html
        return
    if not os.path.exists(dest_path):
        print(f"Skipping {agent_name}: Destination not found")
        return
        
    try:
        with open(source_path, 'r', encoding='utf-8') as f:
            source_content = f.read()
    except Exception as e:
        print(f"Error reading source {agent_name}: {e}")
        return
        
    info = extract_info(source_content)
    
    if not info['wa'] and not info['tg'] and not info['group']:
        print(f"Warning: No contact info found for {agent_name}")
        return

    try:
        with open(dest_path, 'r', encoding='utf-8') as f:
            dest_content = f.read()
    except Exception as e:
        print(f"Error reading dest {agent_name}: {e}")
        return
        
    new_content = dest_content
    
    # Update WA (replace numbers in wa.me links)
    if info['wa']:
        # Regex to match wa.me/NUMBER but keep the rest (like ?text=...)
        # We assume the dest has wa.me/5511... or similar placeholder
        new_content = re.sub(r'(href="[^"]*wa\.me/)\d+', r'\g<1>' + info['wa'], new_content)
        
    # Update TG Personal
    if info['tg']:
        def replace_tg_href(match):
            tag = match.group(0)
            # Replace the href attribute value
            return re.sub(r'href="[^"]+"', f'href="{info["tg"]}"', tag)
            
        # Match the anchor tag with specific class
        new_content = re.sub(r'<a[^>]+class="contact-btn telegram"[^>]*>', replace_tg_href, new_content)

    # Update Group
    if info['group']:
        def replace_group_href(match):
            tag = match.group(0)
            return re.sub(r'href="[^"]+"', f'href="{info["group"]}"', tag)
            
        new_content = re.sub(r'<a[^>]+class="group-btn"[^>]*>', replace_group_href, new_content)
        
    if new_content != dest_content:
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {agent_name}: WA={info['wa']}, TG={info['tg']}, Group={info['group']}")
    else:
        print(f"No changes needed for {agent_name}")

def main():
    print("Starting contact update...")
    if not os.path.exists(SOURCE_BASE):
        print(f"Source base not found: {SOURCE_BASE}")
        return
        
    count = 0
    for item in os.listdir(SOURCE_BASE):
        if os.path.isdir(os.path.join(SOURCE_BASE, item)):
            # Skip non-agent folders if any (like 'i.ibb.co' or 'hts-cache')
            if item in ['i.ibb.co', 'hts-cache']:
                continue
            update_agent(item)
            count += 1
    print(f"Processed {count} folders.")

if __name__ == "__main__":
    main()
