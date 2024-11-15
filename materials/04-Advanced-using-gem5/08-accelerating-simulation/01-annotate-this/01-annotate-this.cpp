#include <iostream>
#include <unistd.h>
#include <dirent.h>

// Include the gem5 m5ops header file

//

// Include the gem5 m5_mmap header file

//

int main() {

// Use the m5op_addr to input the "magic" address

//

// Use the map_m5_mem to map the "magic" address range to /dev/mem

//

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

// Use unmap_m5_mem to unmap the "magic" address range

//

    return 0;
}
