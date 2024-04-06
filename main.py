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

print('---------------------------')
for i in CPUs:
    print(i)
print('---------------------------')
new_CPU = CPU(CPU_name="itel", ALU=8, freq=3200, socket="LGA 1700", TDP=50)#seq позволяет через autoincrement назначить новое id
session.add(new_CPU)
session.commit()
print('Create')
CPUs = session.query(CPU).all()
for i in CPUs:
    print(i)
print('---------------------------')
#del_CPU = session.query(CPU).where(CPU.CPU_id == 4).one()
del_CPU = session.query(CPU).order_by(CPU.CPU_id.desc()).limit(1).one()
session.delete(del_CPU)
session.commit()
CPUs = session.query(CPU).all()
print('Delete')
for i in CPUs:
    print(i)
print('---------------------------')

session.close()