import pandas as pd


data = pd.DataFrame(columns=("serviceKey", "traffic"))
serviceKey = ["Ee5WLqN4iRCKuFUsxlAF1P9anyOX5vH%2BOFG2%2BYM%2BcEoNQOg9emMEyyKM37eAmmVnl1ZxgTalHHL90VNl1B1zlg%3D%3D", #한지성1
              "Z5ilcKNuEfUpecXEfx7zC1DUkQ14RMOCnlRyrcd26XsNABq9l8JlUp6a9lB%2FrktCf22IXkr3SzhAKeWXOJWrcQ%3D%3D", # 한지성 2
              "Xx2HAkylYvV8NReOdvmjvyEC8IknQM0zGi6K%2FHOohlSqQYkiPHVbMGHlI4q8WQ76eWDiFIkeoLWiifvGUBRtpA%3D%3D", # 한지성 3
              "7oZHJT4sU22l%2FztC7xaZcrmPYkHuuw2gt%2FVz%2FZtiLdKHvTTGFJj9tZJbi2iA3VP9ThcCy4eOM7MV1L9nBiS1tw%3D%3D", # 김주안 1
              "GMpkYqmFQfJDk13VV798%2B0nZcpG9EMTF4TypQyMvZg76QGYxmk5F6lj22hbZI%2FfyaiOzTU%2FqsJhM57c9JTzvtA%3D%3D", # 김주안 2
              "nO0Ycvc7FFuYr7gjEVJIVkagqBQx%2Bq5mXNywiMZkLZ2GTIHNlJXrhBeL7ciRz9GS%2Bhtzo%2FUZXLPqDa0017ivdQ%3D%3D", # 이지우 1
              "YxN%2FPifj5Yhgp6Qb6xLFamJJFFZF1UThR2SlXB6eKCTEgpv6PVN7oktz%2Bzt6JTxNuPbB3pIjPNHwAp%2BBl1RA0Q%3D%3D", # 이지우 2
              "H3HKC7oTiu8NoT38nDfHbkgTdsghEPEAndvDcKRIfkRwlJY48OCeUOUNDN8Jzt3l4a9fQfzr9eee2lqr4UvO8A%3D%3D",# 이지우 3
              "Stcge98Sfrdk%2BpVaT9%2FvjYhWI0qv%2B9Z6hVci%2BViUlQxA7JNTqMNM0e7vtkytSyatQVvXprDw7hydxsX2P0%2FmVA%3D%3D"] # 김주안 3 적기

for idx in range(9):
    s = serviceKey[idx]
    t = 0
    data.loc[idx] = [s, t]

data.to_csv("key.csv", index =False)