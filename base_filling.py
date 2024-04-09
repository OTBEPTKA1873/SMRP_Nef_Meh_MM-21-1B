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
    print('Create')
else:
    for cpus in CPUs:
        session.delete(cpus)
    for gpus in GPUs:
        session.delete(gpus)
    for mbs in MBs:
        session.delete(mbs)
    print('Delete')
session.commit()
session.close()