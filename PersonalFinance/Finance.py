import Worker

"""
This financing program is meant to be run manually every monday to keep track of earnings
and make sure that the hours are being paid accordingly
"""
def exists( fileName ):
    file = open( fileName +".txt", "r", encoding="utf-8" )
    return file.readline == "Worker: " + fileName

def get_worker_from_file( fileName ):
    file = open( fileName+".txt", "r", encoding="utf-8")
    worker = Worker.Worker(file.readline)
    job = 
    worker.set_job

if __name__ == "__main__":
    print("Welcome to your Financing App!")
    while True:
        workerName = input("What's your name?")
        if exists( workerName ):

        