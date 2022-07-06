#include <stdio.h>
#include <stdlib.h>



//hashF(CL, root_state, discriminator)


// starting state  ->       integer
// finishing states ->


void *rootStates;
void *nonRootStates;





///////////////////////////////////////////////////////
// CONTENT LABEL
///////////////////////////////////////////////////////
//
// number of ancestors (2b)     (2)
// 5x character (8+1b)          (47)
// root state (10b)             (57)
// finishing states (5b)            (62)
// discriminator (2b)               (64)


void *loadFromFile(const char *filename){

    FILE *fd;

    if ((fd = fopen(filename, "r")) == NULL){
        fprintf(stderr, "CRAP, couldn't open input file\n");
        exit(1);
    }

    rsSize = readRootStateSize();
    rs = readNumberOfRootStates();
    
    rootStates = malloc (rs * rsSize)
    
    
    
    nrs = readNumberOfNonRootStates();
    nrsSize = readNonRootStateSize();
    
    nonRootStates = malloc(nrs * nrsSize)
    
    
    for (int i = 0; i < rs; i++)
        storeRootState(i, readRootState());        //  <-- read function is inline
        
    for (int i = 0; i < nrs; i++)
        storeNonRootState(i, readNonRootState());  // <-- read function is inline
    


    fclose(fd);

}

int main(){

    bool isCurRoot;
    int curState = starting_state;
    
    curInput = getNextInput()
    while((futureInput = getNextInput()) != EOF){
        
        // get content label from current state and input symbol
        // if content label contains future input, proceed by computing the hash
        // else go to the root state
        if (isCurRoot)
             curCL = getCLFromRoot(curState, curInput);              // <-- inline function
        else
             curCL = nonRootStates(curState /*index*/, curInput, curCL)    // <-- inline function
        
        if (future input is in curCL)
            curState = hash(firstAncestorFromCL(curCL), rootFromCL(curCL), discriminatorFromCL(curCL), nrsSize);
        else
            curState = rootFromCL(curCL)    // <-- inline function

        curInput = futureInput;
    }
        

    return 0;
}
