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

# Открываем и считываем
with open("Base_filling_txts/CPU.txt", "r") as f:
    cpus = f.read()
cpus = cpus.replace(" $ ", "\n")# Заменяем все символы $ на пробелы
cpus = cpus.split("\n")# Разбиваем текст на список строк
i = 0
while i in range(len(cpus)):
    new_CPU = CPU(CPU_name=cpus[i], ALU=cpus[i+1], freq=cpus[i+2], socket=cpus[i+3], TDP=cpus[i+4])
    session.add(new_CPU)
    i += 5
session.commit()
with open("Base_filling_txts/GPU.txt", "r") as f:
    gpus = f.read()
gpus = gpus.replace(" $ ", "\n")# Заменяем все символы $ на пробелы
gpus = gpus.split("\n")# Разбиваем текст на список строк
i = 0
while i in range(len(gpus)):
    new_GPU = GPU(GPU_name=gpus[i], freq=gpus[i+1], ALU=gpus[i+2], volume=gpus[i+3], GPU_type=gpus[i+4])
    session.add(new_GPU)
    i += 5
session.commit()
print('Create')
session.close()