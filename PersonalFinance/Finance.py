import Worker

"""
This financing program is meant to be run manually every monday to keep track of earnings
and make sure that the hours are being paid accordingly
"""
def exists( fileName ):
    with open( fileName +".txt", "r", encoding="utf-8" ) as file:
        return file.readline == "Worker: " + fileName

def get_worker_from_file( fileName ):
    with open( fileName+".txt", "r", encoding="utf-8") as file:
        name = file.readline.split()
        worker = Worker.Worker(name[1])
        worker.job = file.readline


if __name__ == "__main__":
    print("Welcome to your Financing App!")
    while True:
        workerName = input("What's your name?")
        if exists( workerName ):
            print("Welcome back %s! It's nice to see you again." %workerName )
        else:
            print("Nice to meet you, %s. I will manage your finances" %workerName)

        