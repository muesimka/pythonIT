import json
import os
import platform
import psutil

def bytes_to_gb(value: int) -> float:
    return round(value / (1024 ** 3), 2)

def main():
    data = search_data()
    save_data(data)

def search_data():
    comp_name = f"{platform.node()}_{os.getpid()}"
    memory = psutil.virtual_memory()
    total_memory = bytes_to_gb(memory.total)
    used_memory = bytes_to_gb(memory.used)
    processes = list(psutil.process_iter(['num_threads']))
    active_processes = len(processes)
    total_threads = sum(p.info['num_threads'] or 0 for p in processes)
    cpu_load = psutil.cpu_percent(interval=1)
    disk = psutil.disk_usage('/')
    used_disk = bytes_to_gb(disk.used)
    cpu_freq = psutil.cpu_freq()
    cpu_speed = round(cpu_freq.current / 1000, 2) if cpu_freq else None  # МГц → ГГц

    data = {
        "имя компа": comp_name,
        "общая память (ГБ)": total_memory,
        "используемая память (ГБ)": used_memory,
        "число активных процессов": active_processes,
        "число потоков": total_threads,
        "загрузка процессора (%)": cpu_load,
        "занятая память на жестком диске (ГБ)": used_disk,
        "скорость процессора (ГГц)": cpu_speed
    }
    return data

def save_data(data: dict):
    name = "data.json"
    with open(name, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()
