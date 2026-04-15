import platform
import psutil

def obter_info_sistema():
    so_tipo = platform.system()
    so_nome_completo = ""

    if so_tipo == "Linux":
        # segundo o gemini o freedesktop_os_release é melhor para retornar detalhes da distro (ex: Ubuntu, 22.04)
        try:
            info =platform.freedesktop_os_release()
            so_nome_completo = f"{info['NAME']} {info.get('VERSION_ID', '')}"
        except:
            so_nome_completo = f"Linux {platform.release()}"
    elif so_tipo == "Windows":
        so_nome_completo = f"Windows {platform.release()} (v{platform.version()})"
        
    else:
        so_nome_completo = f"{so_tipo} {platform.release()}"

    try:
        import cpuinfo
        cpu = cpuinfo.get_cpu_info()['brand_raw']
    except:
        cpu = platform.processor()

    return {
        "so_versao": so_nome_completo,
        "processador": cpu,
        "cores_fisicos": psutil.cpu_count(logical=False),
        "threads_logicos": psutil.cpu_count(logical=True),
        "ram_gb": round(psutil.virtual_memory().total / (1024**3), 2)
    }

if __name__ == "__main__":
    os_info = obter_info_sistema()

    print(os_info)