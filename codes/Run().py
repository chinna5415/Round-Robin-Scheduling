from random import randint      #Used for randomly choosing an integer in a given range.
import Class_Schedule as S           #This class does the scheduling.

def Run():
    '''
    This function is used to input all the required data for Round Robin Scheduling.
    '''
    print('\n________ROUND ROBIN SCHEDULING________')
    n=int(input("Enter the number of tasks: "))
    
    task_name = [chr(65+i) for i in range(n)]     #Each task is given a name alphabetically, in chronological order.
    #-----
    print("\nDo you want to choose the arrival time, or should it be chosen randomly?")
    print("Press 'y' if you want to choose, else press 'n'")
    arrival_time = [0]                          #First task arrives at time = 0.
    choose_arrival = input()
    while True :
        if (choose_arrival == 'y'):
            print("The arrival time of A : 0")                  
            for i in range(1,n):
                print("Enter the arrival time of task",task_name[i],": ") 
                arrival_time.append(int(input()))            #Input the arrival time every task and append it to the list.
            break
        elif (choose_arrival == 'n'):
            for i in range(1,n):
                arrival_time.append(randint(arrival_time[i-1],i+10))    #Other tasks arrive (randomly) after their previous tasks have arrived.
            break    
        else:
            print('you have to choose [y/n]')
            choose_quantum = input()
    #-----
    print("\nDo you want to choose the time quantum, or should it be chosen randomly?")
    print("Press 'y' if you want to choose, else press 'n'")
    choose_quantum = input()
    while True:
        if (choose_quantum == 'y'):
            quantum = int(input("\nEnter the time quantum: "))      #Input the time quantum.
            break
        elif (choose_quantum == 'n'):
            quantum = randint(1,5)      #Time quantum is randomly chosen from the list [1,2,3,4,5].
            break
        else:
            print('you have to choose [y/n]')
            choose_quantum = input()
    #-----
    print("\nDo you want to choose the burst time, or should it be chosen randomly?")
    print("Press 'y' if you want to choose, else press 'n'")
    choose_burst = input()
    burst_time=[]                               #List of burst times of all tasks. 
    while True:
        if (choose_burst == 'y'):
            for i in range(n):
                print("Enter the Burst time of task",task_name[i],": ")
                burst_time.append(int(input()))         #Input the burst time every task and append it to the list.
            break
        elif (choose_burst == 'n'):
            burst_time = [randint(11,20) for i in range(n)] #Burst time for every task is randomly chosen from the list [10,11,12,13,14,15,16,17,18,19,20].
            break
        else:
            print('you have to choose [y/n]')
            choose_burst = input()
    
    print('\nTime quantum =',quantum,'.')   #Display the time quantum.
    #-----
    test = S.Schedule(task_name , n , arrival_time, quantum , burst_time)
    test.process()  #Function call to start scheduling.
    test.output()   #Function call to display the schedule.

if __name__ == '__main__':
    Run()

    
def check_bust_time(temp_bust_time, n):
    if temp_bust_time.count(0) == n:
        return 0
    return  1

def check_ready_queue(ready_queue, process_name):
    if process_name in ready_queue:
        return 0
    return  1

def getMinBust(ready_queue, time, process, temp_bust_time, arival_time):
    Min = 999
    idx = ''
    for i in ready_queue:
        if temp_bust_time[process.index(i)] < Min and temp_bust_time[process.index(i)] != 0:
            Min , idx = temp_bust_time[process.index(i)], i

    temp_bust_time[process.index(idx)] -= 1
    
    if temp_bust_time[process.index(idx)] == 0:
        time += 1
        ready_queue.remove(idx)
        return idx, time, 1
    else:
        time += 1
        return idx, time, 0

process = []
arival_time = []
bust_time = []

with open('data.txt','r') as file:
    for line in file:
        line = line.split(',')
        process.append(line[0])
        arival_time.append(int(line[1]))
        bust_time.append(int(line[2]))

ready_queue = []
gant_chart = []
complete_time = {i:0 for i in process}
temp_bust_time = []+bust_time
time = 0
length = len(process)

while check_bust_time(temp_bust_time, length):
    for i in range(length):
        if (arival_time[i] <= time and check_ready_queue(ready_queue, process[i])):
            ready_queue.append(process[i])

    if ready_queue != []:
        min_, time, flag = getMinBust(ready_queue, time, process, temp_bust_time, arival_time)

        if flag:
            complete_time[min_] = time
            gant_chart.append(min_)
        else:
            gant_chart.append(min_)

temp_gant_chart = [gant_chart[0]]

for i in range(1,len(gant_chart)):
    if gant_chart[i] != temp_gant_chart[-1]:
        temp_gant_chart.append(gant_chart[i])

print('order of exection')
print(*temp_gant_chart)

turn_around_time = []
sum_wt = 0
i = 0

for key, value in complete_time.items():
    turn_around_time.append((value - arival_time[i]))
    sum_wt += (turn_around_time[-1] - bust_time[i])
    i += 1

print('Avarage turn around time : %.2f'%(sum(turn_around_time)/length))
print('Avarage waiting time : %.2f'%(sum_wt/length))
    
