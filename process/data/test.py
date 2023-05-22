from pandas import read_csv

data_path = "/home/zhangs/Github/JUNE_NZ_data/group/test2.csv"
data = read_csv(data_path)

df = data.dropna(axis=1, how="all")


"""
            "0 0 0 0 1"           :   15
            "0 0 0 1 0"           :   20
            "0 0 0 0 2"           :   11
            "0 0 0 2 0"           :   24
            "1 0 >=0 2 0"         :   12
            ">=2 0 >=0 2 0"       :    9
            "0 0 >=1 2 0"         :    6
            "1 0 >=0 1 0"         :    5
            ">=2 0 >=0 1 0"       :    3
            "0 0 >=1 1 0"         :    7
            "1 0 >=0 >=1 >=0"     :    0
            ">=2 0 >=0 >=1 >=0"   :    1
            "0 >=1 0 0 0"         :    0
            "0 0 0 0 >=2"         :    0
            "0 0 >=0 >=0 >=0"     :    1
            ">=0 >=0 >=0 >=0 >=0" :    0
            }
            The encoding follows the rule "1 2 3 4 5" = 1 kid, 2 students (that live in student households), 3 young adults, 4 adults, and 5 old people.

"""


{
    "Couple only": {
        "No dependent children": {"adult": 2, "kid": 0}
    },
    "Couple only and other person(s)": {
        "No dependent children": {"adult": ">=2", "kid": 0},
        "One dependent child": {"adult": ">=2", "kid": 1},
        
    }

}


"0 0 0 2 0": ("Couple only", "No dependent children")

"adult > 2": ("Couple only and other person(s)", "No dependent children")
">=0 >=0 >=0 >=0 >=0": ("Couple only and other person(s)", "No dependent children")



df[["Couple only", "Couple with child(ren)", ]]


"Couple only": "0 0 0 2 0"
