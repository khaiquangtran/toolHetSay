import csv

class ParseCSV:
    FIELD = ['height', 'ball', 'waterfall', 'length', 'shield', 'time']
    def __init__(self) -> None:
        pass

    @classmethod
    def str2bool(cls, value: str) -> bool:
        return value == 'True'

    @classmethod
    def checkData(cls, height: int, ball: bool, waterfall: bool, length: int, shield: bool):
        with open('data.csv', 'r') as file:
            reader = csv.DictReader(file)
            #filter data
            data = [
                line for line in reader
                if int(line['height']) >= (height - 1) and int(line['height']) <= (height + 1)
                and cls.str2bool(line['ball']) == ball
                and cls.str2bool(line['waterfall']) == waterfall
                and int(line['length']) >= (length - 1) and int(line['length']) <= (length + 1)
                and cls.str2bool(line['shield']) == shield
            ]

            if len(data) == 1:
                return data
            else:
                return 0

    @classmethod
    def saveData(cls, height : int, ball : bool, waterfall : bool, length : int, shield : bool, time : float):
        isDataExit = cls.checkData(height, ball, waterfall, length, shield)
        if isDataExit == 0:
            time = round(time, 4)
            with open('data.csv', 'a', newline='') as new_file:
                writer = csv.DictWriter(new_file, fieldnames=cls.FIELD, delimiter=',')
                writer.writerow({
                    'height': height,
                    'ball': ball,
                    'waterfall': waterfall,
                    'length': length,
                    'shield' : shield,
                    'time' : time
                })
            print(f"height {height} || ball {ball} || waterfall {waterfall} || length {length} || shield {shield} || time {time}")

#-----------Testing---------------
if __name__ == "__main__":
    test = ParseCSV()
    output = test.checkData(517,False,False,0,False)
    print(output[0]['time'])

