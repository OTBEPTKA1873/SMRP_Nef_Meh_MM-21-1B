from ORM import CPU, GPU, MB, PU, RAM, Lot, Memory, Cooler, Buyer, Seller, Receipt, User, get_session
from ORM import CPU_MB, GPU_MB, RAM_MB, Cooler_MB

session = get_session()
CPUs = session.query(CPU).all()
GPUs = session.query(GPU).all()
MBs = session.query(MB).all()
PUs = session.query(PU).all()
RAMs = session.query(RAM).all()
Lots = session.query(Lot).all()
Memorys = session.query(Memory).all()
Coolers = session.query(Cooler).all()
Buyers = session.query(Buyer).all()
Sellers = session.query(Seller).all()
Receipts = session.query(Receipt).all()
Users = session.query(User).all()

CPU_MBs = session.query(CPU_MB).all()
GPU_MBs = session.query(GPU_MB).all()
RAM_MBs = session.query(RAM_MB).all()
Cooler_MBs = session.query(Cooler_MB).all()


del_or_cre = 1
if del_or_cre == 1:
    # Работа с CPU
    with open("Base_filling_txt/CPU.txt", "r") as f:# Читаем CPU
        cpus = f.read()
    cpus = cpus.replace(" $ ", "\n")# Заменяем все символы $ на пробелы
    cpus = cpus.split("\n")# Разбиваем текст на список строк
    i = 0
    while i in range(len(cpus)):
        new_CPU = CPU(CPU_name=cpus[i], ALU=cpus[i+1], freq=cpus[i+2], socket=cpus[i+3], TDP=cpus[i+4])
        session.add(new_CPU)
        i += 5
    # Работа с GPU
    with open("Base_filling_txt/GPU.txt", "r") as f:# Открываем и считываем GPU
        gpus = f.read()
    gpus = gpus.replace(" $ ", "\n")# Заменяем все символы $ на пробелы
    gpus = gpus.split("\n")# Разбиваем текст на список строк
    i = 0
    while i in range(len(gpus)):
        new_GPU = GPU(GPU_name=gpus[i], freq=gpus[i+1], ALU=gpus[i+2], volume=gpus[i+3], GPU_type=gpus[i+4])
        session.add(new_GPU)
        i += 5
    # Работа с MB
    with open("Base_filling_txt/MB.txt", "r") as f:  # Открываем и считываем MB
        mbs = f.read()
    mbs = mbs.replace(" $ ", "\n")  # Заменяем все символы $ на пробелы
    mbs = mbs.split("\n")  # Разбиваем текст на список строк
    i = 0
    while i in range(len(mbs)):
        new_MB = MB(MB_name=mbs[i], form_factor=mbs[i + 1], socket_type=mbs[i + 2], RAM_type=mbs[i + 3], RAM_count=mbs[i + 4], freq=mbs[i + 5], GPU_type=mbs[i + 6])
        session.add(new_MB)
        i += 7
    # Работа с RAM
    with open("Base_filling_txt/RAM.txt", "r") as f:  # Открываем и считываем RAM
        rams = f.read()
    rams = rams.replace(" $ ", "\n")  # Заменяем все символы $ на пробелы
    rams = rams.split("\n")  # Разбиваем текст на список строк
    i = 0
    while i in range(len(rams)):
        new_RAM = RAM(RAM_name=rams[i], RAM_type=rams[i + 1], volume=rams[i + 2], freq=rams[i + 3])
        session.add(new_RAM)
        i += 4
    # Работа с PU
    with open("Base_filling_txt/PU.txt", "r") as f:  # Открываем и считываем PU
        pus = f.read()
    pus = pus.replace(" $ ", "\n")  # Заменяем все символы $ на пробелы
    pus = pus.split("\n")  # Разбиваем текст на список строк
    i = 0
    while i in range(len(pus)):
        new_pus = PU(PU_name=pus[i], watt=pus[i + 1])
        session.add(new_pus)
        i += 2
    print('Create')
else:
    for cpus in CPUs:
        session.delete(cpus)
    for gpus in GPUs:
        session.delete(gpus)
    for mbs in MBs:
        session.delete(mbs)
    for rams in RAMs:
        session.delete(rams)
    for pus in PUs:
        session.delete(pus)
    print('Delete')
session.commit()
session.close()