# -*- coding: utf-8 -*-
# Vajalikud moodulid:
# Pythoni standardteegis olevad moodulid: glob, re, collections, gzip
# Väliseid mooduleid ei ole vaja paigaldada.

import glob
import re
from collections import Counter
import gzip # Lisatud gzip toe jaoks

# Ülesande konfiguratsioon
LOG_DIR = r"C:\Temp"
LOG_FILE_PATTERN = "tuntud_access.*" # See leiab nii tuntud_access.log kui tuntud_access.log.gz
OUTPUT_FILE = "task09.txt"

BOT_NAME_EXTRACTOR_REGEX = re.compile(
    r"""
    (?:^|\s|;|/\s*|[\(\[])
    (
        [a-zA-Z0-9\._-]*?
        (?:bot|crawler|robot)
        [a-zA-Z0-9\._-]*?
    )
    (?:/|[\s\);\]]|$)
    """, 
    re.IGNORECASE | re.VERBOSE
)

def extract_user_agent(log_line):
    match = re.search(r'"([^"]*)"$', log_line)
    if match:
        return match.group(1)
    return None

def get_dynamic_bot_name(user_agent_string):
    if not user_agent_string:
        return None
    
    match = BOT_NAME_EXTRACTOR_REGEX.search(user_agent_string)
    if match and match.group(1):
        name = match.group(1)
        name = re.sub(r"[/;,()\[\]\s].*$", "", name)
        name = name.strip(" .,:;-")
        if name:
            return name
            
    if "bot" in user_agent_string.lower(): return "GenericBot"
    if "crawler" in user_agent_string.lower(): return "GenericCrawler"
    if "robot" in user_agent_string.lower(): return "GenericRobot"
    
    return None

def main():
    log_files = glob.glob(f"{LOG_DIR}\\{LOG_FILE_PATTERN}")

    if not log_files:
        msg = f"Viga: Ei leidnud ühtegi logifaili mustriga '{LOG_FILE_PATTERN}' kaustast '{LOG_DIR}'."
        print(msg)
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f_out:
            f_out.write(msg + "\n")
        return

    bot_counts = Counter()
    print(f"Analüüsin faile kaustas {LOG_DIR} mustriga {LOG_FILE_PATTERN} (dünaamiline nime eraldus, .gz tugi)...\n")
    
    unidentified_bots_examples = []

    for log_file_path in log_files:
        print(f"Töötlen faili: {log_file_path}")
        try:
            # Kontrolli, kas fail on .gz ja ava vastavalt
            if log_file_path.endswith(".gz"):
                opener = gzip.open
                # gzip.open tagastab baidid, seega peame dekodeerima
                read_mode = 'rt' # Loe tekstirežiimis, 't' on oluline
            else:
                opener = open
                read_mode = 'r'

            with opener(log_file_path, mode=read_mode, encoding='utf-8', errors='ignore') as f:
                for line_number, line_content in enumerate(f, 1):
                    # 'line_content' on juba string tänu 'rt' mode'ile gzip.open puhul
                    # ja 'r' mode'ile tavalise open puhul
                    user_agent = extract_user_agent(line_content.strip())
                    if user_agent:
                        bot_name = get_dynamic_bot_name(user_agent)
                        if bot_name:
                            bot_counts[bot_name] += 1
                        elif any(kw in user_agent.lower() for kw in ["bot", "crawler", "robot"]) and len(unidentified_bots_examples) < 10:
                             unidentified_bots_examples.append(user_agent)
        except gzip.BadGzipFile:
            print(f"  Viga: Fail {log_file_path} ei ole korrektne gzip fail või on vigane. Jätan vahele.")
            continue
        except Exception as e:
            print(f"  Viga faili {log_file_path} töötlemisel: {e}")
            continue

    if unidentified_bots_examples:
        print("\nMärkus: Mõned potentsiaalsed bot'id jäid identifitseerimata või üldistati. Näited UA stringidest:")
        for ua_example in unidentified_bots_examples:
            print(f"  - {ua_example}")
        print("Võib vajada BOT_NAME_EXTRACTOR_REGEX täpsustamist.\n")

    if not bot_counts:
        message = "Ühtegi bot'i (bot, crawler, robot) ei leitud kasutajaagentidest."
        print(message)
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f_out:
            f_out.write(message + "\n")
        return

    sorted_bots = sorted(bot_counts.items(), key=lambda item: (-item[1], item[0]))

    max_name_len = 0
    if sorted_bots:
        max_name_len = max(len(name) for name, count in sorted_bots)
    max_name_len = max(max_name_len, len("Bot")) 

    output_lines = []
    header_title = "Leitud bot'id ja nende külastuste arv (dünaamiliselt eraldatud nimed):"
    header_columns = f"{'Bot':<{max_name_len}} | {'Num':>5}"
    separator = "-" * (max_name_len + 3 + 5)
    
    print(header_title)
    print(header_columns)
    print(separator)
    
    output_lines.append(header_title)
    output_lines.append(header_columns)
    output_lines.append(separator)

    for name, count in sorted_bots:
        line_output = f"{name:<{max_name_len}} | {count:>5}"
        print(line_output)
        output_lines.append(line_output)

    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f_out:
            for line_item in output_lines:
                f_out.write(line_item + "\n")
        print(f"\nTulemused salvestatud faili {OUTPUT_FILE}")
    except IOError as e:
        print(f"Viga faili {OUTPUT_FILE} kirjutamisel: {e}")

if __name__ == "__main__":
    main()