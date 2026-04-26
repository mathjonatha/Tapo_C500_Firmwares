import subprocess
import os
import requests
from pathlib import Path

# Lista completa de firmwares C500 v1 e v2 extraída do servidor
firmwares = [
    # C500 V1
    "firmware/Tapo_C500v1_en_1.0.0_Build_221102_Rel.37658n_u_1672801957478.bin",
    "firmware/Tapo_C500v1_en_1.0.1_Build_221123_Rel.70890n_u_1674890537152.bin",
    "firmware/Tapo_C500v1_en_1.0.3_Build_230404_Rel.64834n_up_boot-signed_1681119458966.bin",
    "firmware/Tapo_C500v1_en_1.0.4_Build_230412_Rel.46201n_up_boot-signed_1682584958094.bin",
    "firmware/Tapo_C500v1_en_1.0.6_Build_230609_Rel.72971n_up_boot-signed_1688023374447.bin",
    "firmware/Tapo_C500v1_en_1.1.1_Build_230908_Rel.75459n_up_boot-signed_1695376339486.bin",

    # C500 V2
    "firmware/Tapo_C500v2_en_1.0.1_Build_240523_Rel.57729n_up_boot-signed_1717582198519.bin",
    "firmware/Tapo_C500v2_en_1.0.2_Build_240605_Rel.32561n_up_boot-signed_1720489991161.bin",
    "firmware/Tapo_C500v2_en_1.0.3_Build_240716_Rel.36544n_up_boot-signed_1723717610011.bin",
    "firmware/Tapo_C500v2_en_1.0.4_Build_240902_Rel.38194n_up_boot-signed_1729245173712.bin",
    "firmware/Tapo_C500v2_en_1.0.5_Build_241009_Rel.53058n_up_boot-signed_1735282568483.bin",
    "firmware/Tapo_C500v2_en_1.0.6_Build_250107_Rel.35614n_up_boot-signed_1737013933162.bin",
    "firmware/Tapo_C500v2_en_1.0.7_Build_250327_Rel.71908n_up_boot-signed_1743405729841.bin",
    "firmware/Tapo_C500v2_en_1.1.1_Build_250228_Rel.53276n_up_boot-signed_1741243028059.bin",
    "firmware/Tapo_C500v2_en_1.1.2_Build_250326_Rel.61993n_up_boot-signed_1747274829157.bin",
    "firmware/Tapo_C500v2_en_1.1.3_Build_250826_Rel.62380n_up_boot-signed_1757245927067.bin",
    "firmware/Tapo_C500v2_en_1.2.1_Build_250919_Rel.39923n_up_boot-signed_1760428335479.bin",
    "firmware/Tapo_C500v2_en_1.2.2_Build_251016_Rel.58785n_up_boot-signed_1761723435023.bin",
    "firmware/Tapo_C500v2_en_1.2.3_Build_251107_Rel.39788n_up_boot-signed_1764821270204.bin",
    "firmware/Tapo_C500v2_en_1.3.1_Build_260106_Rel.63845n_up_boot-signed_1770190627914.bin",
    "firmware/Tapo_C500v2_en_1.3.2_Build_260309_Rel.8833n_up_boot-signed_1775040746167.bin",
]

BASE_URL = "https://download.tplinkcloud.com/"

def get_version_folder(filename):
    """Extrai a versão do nome do arquivo e retorna o nome da pasta"""
    # Ex: Tapo_C500v2_en_... -> Tapo_C500v2
    parts = filename.split("/")[-1]  # pega só o nome do arquivo
    # Pega modelo + versão hardware: Tapo_C500v1 ou Tapo_C500v2
    model_ver = "_".join(parts.split("_")[:2])  # Tapo_C500v1 ou Tapo_C500v2
    hw_ver = model_ver.replace("Tapo_C500v", "")
    return f"Tapo_C500v{hw_ver}"

def get_fw_version(filename):
    """Extrai a versão do firmware do nome do arquivo"""
    parts = filename.split("/")[-1].split("_")
    for i, p in enumerate(parts):
        if p == "en" and i + 1 < len(parts):
            return parts[i + 1]
    return "unknown"

def download_firmware(path, dest_folder):
    url = BASE_URL + path
    filename = path.split("/")[-1]
    dest = Path(dest_folder) / filename

    if dest.exists():
        print(f"  [JÁ EXISTE] {filename}")
        return True

    print(f"  Baixando {filename}...")
    try:
        r = requests.get(url, stream=True, timeout=30)
        if r.status_code == 200:
            with open(dest, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            size_mb = dest.stat().st_size / 1024 / 1024
            print(f"  [OK] {filename} ({size_mb:.1f} MB)")
            return True
        else:
            print(f"  [ERRO {r.status_code}] {filename}")
            return False
    except Exception as e:
        print(f"  [FALHA] {filename}: {e}")
        return False

# Organiza por versão de hardware
folders = {}
for fw in firmwares:
    folder = get_version_folder(fw)
    if folder not in folders:
        folders[folder] = []
    folders[folder].append(fw)

print("=" * 60)
print("Download de Firmwares - Tapo C500")
print("=" * 60)

base_dir = Path("Tapo_C500_Firmwares")
base_dir.mkdir(exist_ok=True)

total_ok = 0
total_err = 0

for folder_name in sorted(folders.keys()):
    folder_path = base_dir / folder_name
    folder_path.mkdir(exist_ok=True)
    print(f"\n📁 {folder_name} ({len(folders[folder_name])} firmwares)")
    print("-" * 40)

    for fw in folders[folder_name]:
        fw_ver = get_fw_version(fw)
        ok = download_firmware(fw, folder_path)
        if ok:
            total_ok += 1
        else:
            total_err += 1

print("\n" + "=" * 60)
print(f"Concluído! ✅ {total_ok} baixados | ❌ {total_err} erros")
print(f"Pasta: {base_dir.resolve()}")
print("=" * 60)
