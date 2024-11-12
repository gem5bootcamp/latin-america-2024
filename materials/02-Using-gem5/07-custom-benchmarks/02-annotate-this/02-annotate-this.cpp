#include <iostream>
#include <unistd.h>
#include <dirent.h>

// Include the gem5 m5ops header file

//
int main() {

// Use the gem5 m5ops to annotate the start of the ROI

//
    write(1, "This will be output to standard out\n", 36);
// Use the gem5 m5ops to annotate the end of the ROI

//

    struct dirent *d;
    DIR *dr;
    dr = opendir(".");
    if (dr!=NULL) {
        std::cout<<"List of Files & Folders:\n";
        for (d=readdir(dr); d!=NULL; d=readdir(dr)) {
            std::cout<<d->d_name<< ", ";
        }
        closedir(dr);
    }
    else {
        std::cout<<"\nError Occurred!";
    }
    std::cout<<std::endl;

    return 0;
}


