from unlockappleid import  unlockAccount
from handle_excel import HandExcel

handexcel = HandExcel()
accountInfos = handexcel.get_excel_data()

for a in accountInfos:
    try:
        unlockAccount(a[1],a[2],a[3],a[4])
    except Exception as e:
        pass
    continue

