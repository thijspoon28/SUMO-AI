from utils.parsing import modify_basho_date


basho_date = ("202303", 14)

basho_date = modify_basho_date(basho_date, -16, -13)
print(basho_date)