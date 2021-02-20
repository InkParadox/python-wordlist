fileName = "data/6-character-iteration-part-"

result = 0

for j in range(0,30):

    file = open(fileName + str(j+1) + ".txt","r") 

    Content = file.read() 
    CoList = Content.split("\n") 
    
    for i in CoList: 
        if i: 
            result += 1
            
    print("lines in file " + str(j+1) + " : " + str(result))