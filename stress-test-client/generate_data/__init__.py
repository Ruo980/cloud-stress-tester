# 数据生成包：主要是生成MySQL和Redis原始数据，方便后续的查询和插入。
# 考虑到Redis主要将数据存放在内存，因此Redis最好做读取而不是存入。所以Redis的初始数据量要大方便查询
# MySQL主要用于大规模的数据存储，因此MySQL最好初始数据较少，而进行做规模以上数据的村粗