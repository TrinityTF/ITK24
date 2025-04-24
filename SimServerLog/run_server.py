import time
import random
from datetime import datetime
from faker import Faker
import os
import shutil
import gzip
import sys

# Logifaili ja kausta nimi
LOG_DIR = "C:\\Temp"
LOG_FILE = os.path.join(LOG_DIR, "application.log")
GZ_LOG_FILE_TEMPLATE = os.path.join(LOG_DIR, "application.log.{num}.gz")
# Maksimaalne failisuurus baitides
FILE_SIZE = 10 * 1024  # 10 KB

# Näidistegevused logimiseks
ACTIONS = [
    "User logged in",
    "User logged out",
    "File uploaded",
    "File downloaded",
    "Email sent",
    "Email received",
    "Error: Invalid password",
    "Error: File not found",
    "Session expired",
    "Database connection established",
    "Database connection lost",
    "New user registered",
    "System update initiated",
    "System rebooted",
    "User password changed",
    "User profile updated",
    "Admin privileges granted",
    "Login attempt failed",
    "New device connected",
    "Service started",
    "Service stopped",
    "Backup created",
    "Backup restored",
    "Configuration file updated",
    "Notification sent",
    "Notification received",
]

# Levinud teenuste ja seadmete nimed
SERVICES = [
    "apache", "mysql", "ssh", "nginx", "web", "ftp", "redis",
    "lighttpd", "tomcat", "mariadb", "postgresql", "mongodb",
    "cassandra", "bind9", "dhcpd", "openvpn", "ipsec",
    "postfix", "sendmail", "exim", "dovecot", "spamassassin",
    "cron", "rsyslog", "journalctl", "auditd", "docker",
    "kubelet", "libvirtd", "qemu-kvm", "cups", "bluetoothd",
    "network-manager", "firewalld", "ntpd"
]
DEVICES = ["USB drive", "SD card", "SSD drive", "External HDD", "Bluetooth device", "WiFi adapter"]

# Faker objekt andmete genereerimiseks
faker = Faker()

# Kontrolli käsurea argumenti gzipimiseks
use_gzip = "no-gz" not in sys.argv


def setup_log_directory():
    """Loo logikaust ja eemalda vanad logid."""
    if os.path.exists(LOG_DIR):
        shutil.rmtree(LOG_DIR)  # Kustuta vana kaust ja failid
    os.makedirs(LOG_DIR)  # Loo uus kaust


def generate_log_entry():
    """Genereerib ühe logikirje kuupäeva, kellaaja ja juhusliku tegevusega."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    action = random.choice(ACTIONS)

    # Lisa konteksti tegevuse kohta
    if "user" in action.lower():
        detail = faker.user_name()
    elif "file" in action.lower():
        detail = faker.file_name()
    elif "email" in action.lower():
        detail = faker.email()
    elif "database" in action.lower():
        detail = faker.first_name()
    elif "system" in action.lower():
        detail = faker.hostname()
    elif "service" in action.lower():
        detail = random.choice(SERVICES)
    elif "device" in action.lower():
        detail = random.choice(DEVICES)
    elif "notification" in action.lower():
        detail = faker.sentence(nb_words=3)
    elif "backup" in action.lower():
        detail = faker.file_path(depth=2)
    elif "configuration" in action.lower():
        detail = faker.file_name(extension="cfg")
    elif "admin privileges granted" in action.lower():
        detail = faker.user_name()
    elif "invalid password" in action.lower():
        detail = faker.user_name()
    else:
        detail = "N/A"

    return f"[{timestamp}] {action} - {detail}"


def compress_file(input_file, output_file):
    """Pakkige fail gzip-vormingus."""
    with gzip.open(output_file, 'wb') as gz_file:
        with open(input_file, 'rb') as f_in:
            gz_file.write(f_in.read())


def rotate_logs():
    """Nimetab logifaili ümber vastavalt rotatsiooniskeemile (1-9), kus kõige suurema numbriga fail on vanim."""
    if use_gzip:
        # Gzip-rotatsioon
        oldest_file = GZ_LOG_FILE_TEMPLATE.format(num=9)
        if os.path.exists(oldest_file):
            os.remove(oldest_file)  # Eemalda kõige vanem fail

        for i in range(8, 0, -1):
            old_file = GZ_LOG_FILE_TEMPLATE.format(num=i)
            new_file = GZ_LOG_FILE_TEMPLATE.format(num=i + 1)
            if os.path.exists(old_file):
                os.rename(old_file, new_file)

        if os.path.exists(LOG_FILE):
            compress_file(LOG_FILE, GZ_LOG_FILE_TEMPLATE.format(num=1))
            os.remove(LOG_FILE)

    else:
        # Tavaline log-rotatsioon
        oldest_file = os.path.join(LOG_DIR, "application.log.9")
        if os.path.exists(oldest_file):
            os.remove(oldest_file)  # Eemalda kõige vanem fail

        for i in range(8, 0, -1):
            old_file = os.path.join(LOG_DIR, f"application.log.{i}")
            new_file = os.path.join(LOG_DIR, f"application.log.{i + 1}")
            if os.path.exists(old_file):
                os.rename(old_file, new_file)

        if os.path.exists(LOG_FILE):
            os.rename(LOG_FILE, os.path.join(LOG_DIR, "application.log.1"))


def write_log_to_file(entry):
    """Kirjutab logikirje faili."""
    # Kontrolli faili suurust
    if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > FILE_SIZE:
        rotate_logs()

    # Kirjuta uus logikirje faili
    with open(LOG_FILE, "a") as log_file:
        log_file.write(entry + "\n")


def manage_service_logs():
    """Loo ja eemalda juhuslikke logifaile teenuste nimedega."""
    while True:
        action = random.choice(["create", "delete"])
        service_name = random.choice(SERVICES)
        log_file = os.path.join(LOG_DIR, f"{service_name}.log")
        rotated_log_file = os.path.join(LOG_DIR, f"{service_name}.log.1")

        if action == "create":
            # Loo teenuse logifail ja lisa sisu
            with open(log_file, "wb") as f:
                f.write(os.urandom(random.randint(1024, 10 * 1024)))  # 1 KB kuni 10 KB
            if random.choice([True, False]):
                with open(rotated_log_file, "wb") as f:
                    f.write(os.urandom(random.randint(1024, 10 * 1024)))
        elif action == "delete":
            # Eemalda teenuse logifailid
            if os.path.exists(log_file):
                os.remove(log_file)
            if os.path.exists(rotated_log_file):
                os.remove(rotated_log_file)

        time.sleep(random.randint(5, 15))  # Oota 5–15 sekundit enne järgmist toimingut


def main():
    """Käivitab logide genereerimise tsüklis juhuslike pausidega."""
    setup_log_directory()
    print(f"Logimine algas. Kirjutatakse faili: {LOG_FILE}")

    # Käivita teenuse logihaldus eraldi lõimes
    import threading
    threading.Thread(target=manage_service_logs, daemon=True).start()

    while True:
        # Genereeri ja kirjuta logikirje
        log_entry = generate_log_entry()
        print(log_entry)
        write_log_to_file(log_entry)

        # Tee juhuslik paus (1 kuni 5 sekundit)
        time.sleep(random.randint(1, 5))


if __name__ == "__main__":
    main()
