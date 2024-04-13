from ORM import CPU, GPU, MB, PU, RAM, Lot, Memory, Cooler, Buyer, Seller, Receipt, User, get_session
from ORM import CPU_MB, GPU_MB, RAM_MB, Cooler_MB

session = get_session()
CPUs = session.query(CPU).all()
GPUs = session.query(GPU).all()
MBs = session.query(MB).all()
PUs = session.query(PU).all()
RAMs = session.query(RAM).all()
Memorys = session.query(Memory).all()
Coolers = session.query(Cooler).all()

Lots = session.query(Lot).all()
Users = session.query(User).all()
Sellers = session.query(Seller).all()
Buyers = session.query(Buyer).all()
Receipts = session.query(Receipt).all()

CPU_MBs = session.query(CPU_MB).all()
GPU_MBs = session.query(GPU_MB).all()
RAM_MBs = session.query(RAM_MB).all()
Cooler_MBs = session.query(Cooler_MB).all()
# 1-заполнение БД, 2-проверка совместимости, 3-удаление всей инфы из БД
del_or_cre = 2
if del_or_cre == 1:
    # Заполняем CPU
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
    # Заполняем GPU
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
    # Заполняем MB
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
    # Заполняем RAM
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
    # Заполняем PU
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
    # Заполняем Cooler
    with open("Base_filling_txt/Cooler.txt", "r") as f:  # Открываем и считываем Cooler
        new = f.read()
    new = new.replace(" $ ", "\n")  # Заменяем все символы $ на пробелы
    new = new.split("\n")  # Разбиваем текст на список строк
    i = 0
    while i in range(len(new)):
        new_pus = Cooler(cooler_name=new[i], socket=new[i + 1], DH=new[i + 2], noise=new[i + 3])
        session.add(new_pus)
        i += 4
    # Заполняем Memory
    with open("Base_filling_txt/Memory.txt", "r") as f:  # Открываем и считываем Cooler
        new = f.read()
    new = new.replace(" $ ", "\n")  # Заменяем все символы $ на пробелы
    new = new.split("\n")  # Разбиваем текст на список строк
    i = 0
    while i in range(len(new)):
        new_pus = Memory(mem_name=new[i], mem_type=new[i + 1], volume=new[i + 2], speed=new[i + 3])
        session.add(new_pus)
        i += 4
    print('Create')
elif del_or_cre == 2:
    # Делаем совместимость по сокету MotherBoard и CPU
    i = 0
    while i in range(len(CPUs)):
        j = 0
        while j in range(len(MBs)):
            if CPUs[i].socket == MBs[j].socket_type:
                new_MB_CPU = CPU_MB(CPU_id=CPUs[i].CPU_id, MB_id=MBs[j].MB_id)
                session.add(new_MB_CPU)
            j += 1
        i += 1
    # Делаем совместимость по сокету MotherBoard и GPU
    i = 0
    while i in range(len(GPUs)):
        j = 0
        while j in range(len(MBs)):
            if GPUs[i].GPU_type == MBs[j].GPU_type:
                new_MB_GPU = GPU_MB(GPU_id=GPUs[i].GPU_id, MB_id=MBs[j].MB_id)
                session.add(new_MB_GPU)
            j += 1
        i += 1
    i = 0
    # Делаем совместимость по MotherBoard и RAM
    while i in range(len(RAMs)):
        j = 0
        while j in range(len(MBs)):
            if RAMs[i].RAM_type == MBs[j].RAM_type:
                new_MB_RAM = RAM_MB(RAM_id=RAMs[i].RAM_id, MB_id=MBs[j].MB_id)
                session.add(new_MB_RAM)
            j += 1
        i += 1
    i = 0
    # Делаем совместимость по MotherBoard и Cooler
    while i in range(len(Coolers)):
        j = 0
        while j in range(len(MBs)):
            if Coolers[i].socket == MBs[j].socket_type:
                new_Cooler_CPU = Cooler_MB(cooler_id=Coolers[i].cooler_id, MB_id=MBs[j].MB_id)
                session.add(new_Cooler_CPU)
            j += 1
        i += 1
    print("Create compability")
else:
    # Удаление пользователей, чеков, лотов (вроде в правильном порядке)
    for receipts in Receipts:
        session.delete(receipts)
    for buyers in Buyers:
        session.delete(buyers)
    for lots in Lots:
        session.delete(lots)
    for sellers in Sellers:
        session.delete(sellers)
    for users in Users:
        session.delete(users)
    # Удаление информации о совместимостей
    for cpu_mb in CPU_MBs:
        session.delete(cpu_mb)
    for gpu_mb in GPU_MBs:
        session.delete(gpu_mb)
    for ram_mb in RAM_MBs:
        session.delete(ram_mb)
    for cooler_mb in Cooler_MBs:
        session.delete(cooler_mb)
    #Удаление информации о компонентах
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
