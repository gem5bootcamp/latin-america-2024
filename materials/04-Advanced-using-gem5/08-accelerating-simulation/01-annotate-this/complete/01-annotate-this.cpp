#include <iostream>
#include <unistd.h>
#include <dirent.h>

// Include the gem5 m5ops header file
#include <gem5/m5ops.h>
//

// Include the gem5 m5_mmap header file
#include <m5_mmap.h>
//

int main() {

// Use the m5op_addr to input the "magic" address
    m5op_addr = 0XFFFF0000;
//

// Use the map_m5_mem to map the "magic" address range to /dev/mem
    map_m5_mem();
//

// Use the gem5 m5ops to annotate the start of the ROI
    m5_work_begin_addr(0, 0);
//
    write(1, "This will be output to standard out\n", 36);
// Use the gem5 m5ops to annotate the end of the ROI
    m5_work_end_addr(0, 0);
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
    unmap_m5_mem();
//

    return 0;
}
