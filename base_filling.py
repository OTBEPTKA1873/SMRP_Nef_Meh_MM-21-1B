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
    with open("Base_filling_txt/CPU.txt", "r") as f:  # Читаем CPU
        new = f.read()
    new = new.replace(" $ ", "\n")  # Заменяем все символы $ на пробелы
    new = new.split("\n")  # Разбиваем текст на список строк
    i = 0
    while i in range(len(new)):
        new_CPU = CPU(CPU_name=new[i], ALU=new[i + 1], freq=new[i + 2], socket=new[i + 3], TDP=new[i + 4])
        session.add(new_CPU)
        i += 5
    del new[:]
    # Работа с GPU
    with open("Base_filling_txt/GPU.txt", "r") as f:  # Открываем и считываем GPU
        new = f.read()
    new = new.replace(" $ ", "\n")  # Заменяем все символы $ на пробелы
    new = new.split("\n")  # Разбиваем текст на список строк
    i = 0
    while i in range(len(new)):
        new_GPU = GPU(GPU_name=new[i], freq=new[i + 1], ALU=new[i + 2], volume=new[i + 3], GPU_type=new[i + 4])
        session.add(new_GPU)
        i += 5
    del new[:]
    # Работа с MB
    with open("Base_filling_txt/MB.txt", "r") as f:  # Открываем и считываем MB
        new = f.read()
    new = new.replace(" $ ", "\n")  # Заменяем все символы $ на пробелы
    new = new.split("\n")  # Разбиваем текст на список строк
    i = 0
    while i in range(len(new)):
        new_MB = MB(MB_name=new[i], form_factor=new[i + 1], socket_type=new[i + 2], RAM_type=new[i + 3], RAM_count=new[i + 4], freq=new[i + 5], GPU_type=new[i + 6])
        session.add(new_MB)
        i += 7
    del new[:]
    # Работа с RAM
    with open("Base_filling_txt/RAM.txt", "r") as f:  # Открываем и считываем RAM
        new = f.read()
    new = new.replace(" $ ", "\n")  # Заменяем все символы $ на пробелы
    new = new.split("\n")  # Разбиваем текст на список строк
    i = 0
    while i in range(len(new)):
        new_RAM = RAM(RAM_name=new[i], RAM_type=new[i + 1], volume=new[i + 2], freq=new[i + 3])
        session.add(new_RAM)
        i += 4
    del new[:]
    # Работа с PU
    with open("Base_filling_txt/PU.txt", "r") as f:  # Открываем и считываем PU
        new = f.read()
    new = new.replace(" $ ", "\n")  # Заменяем все символы $ на пробелы
    new = new.split("\n")  # Разбиваем текст на список строк
    i = 0
    while i in range(len(new)):
        new_pus = PU(PU_name=new[i], watt=new[i + 1])
        session.add(new_pus)
        i += 2
    del new[:]
    # Работа с Cooler
    with open("Base_filling_txt/Cooler.txt", "r") as f:  # Открываем и считываем Cooler
        new = f.read()
    new = new.replace(" $ ", "\n")  # Заменяем все символы $ на пробелы
    new = new.split("\n")  # Разбиваем текст на список строк
    i = 0
    while i in range(len(new)):
        new_pus = Cooler(cooler_name=new[i], socket=new[i + 1], DH=new[i + 2], noise=new[i + 3])
        session.add(new_pus)
        i += 4
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
    for coolers in Coolers:
        session.delete(coolers)
    print('Delete')
session.commit()
session.close()