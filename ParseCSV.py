import csv

class ParseCSV:
    FIELD = ['height', 'ball', 'waterfall', 'length', 'shield', 'time']
    FILE_NAME = 'data.csv'
    def __init__(self) -> None:
        pass

    @classmethod
    def str2bool(cls, value: str) -> bool:
        return value == 'True'

    @classmethod
    def checkData(cls, height: int, ball: bool, waterfall: bool, length: int, shield: bool):
        with open(cls.FILE_NAME, 'r') as file:
            reader = csv.DictReader(file)
            # Filter data
            data = [
                line for line in reader
                if int(line[cls.FIELD[0]]) >= (height - 1) and int(line[cls.FIELD[0]]) <= (height + 1)
                and cls.str2bool(line[cls.FIELD[1]]) == ball
                and cls.str2bool(line[cls.FIELD[2]]) == waterfall
                and int(line[cls.FIELD[3]]) >= (length - 1) and int(line[cls.FIELD[3]]) <= (length + 1)
                and cls.str2bool(line[cls.FIELD[4]]) == shield
            ]

            if len(data) == 1:
                return data
            else:
                return 0

    @classmethod
    def saveData(cls, height : int, ball : bool, waterfall : bool, length : int, shield : bool, time : float):
        time = round(time, 4)
        with open(cls.FILE_NAME, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=cls.FIELD, delimiter=',')
            writer.writerow({
                cls.FIELD[0] : height,
                cls.FIELD[1] : ball,
                cls.FIELD[2] : waterfall,
                cls.FIELD[3] : length,
                cls.FIELD[4] : shield,
                cls.FIELD[5] : time
            })
        print(f"{cls.FIELD[0]} {height} || "
              f"{cls.FIELD[1]} {ball} || "
              f"{cls.FIELD[2]} {waterfall} || "
              f"{cls.FIELD[3]} {length} || "
              f"{cls.FIELD[4]} {shield} || "
              f"{cls.FIELD[5]} {time}")

#-----------Testing---------------
if __name__ == "__main__":
    test = ParseCSV()
    print(type(test.FIELD[1]))
    output = test.checkData(517,False,False,0,False)
    print(output[0]['time'])

