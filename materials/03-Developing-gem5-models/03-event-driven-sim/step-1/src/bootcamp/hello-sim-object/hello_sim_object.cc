#include "bootcamp/hello-sim-object/hello_sim_object.hh"

#include <iostream>

#include "base/trace.hh"
#include "debug/HelloExampleFlag.hh"

namespace gem5
{

HelloSimObject::HelloSimObject(const HelloSimObjectParams& params):
    SimObject(params),
    remainingHellosToPrintByEvent(params.num_hellos),
    nextHelloEvent([this](){ processNextHelloEvent(); }, name() + ".nextHelloEvent")
{
    fatal_if(params.num_hellos <= 0, "num_hellos should be positive!");
    for (int i = 0; i < params.num_hellos; i++) {
        std::cout << "i: " << i << ", Hello from HelloSimObject's constructor!" << std::endl;
    }
    DPRINTF(HelloExampleFlag, "%s: Hello from HelloSimObject's constructor!\n", __func__);
}

void
HelloSimObject::startup()
{
    panic_if(curTick() != 0, "startup called at a tick other than 0");
    panic_if(nextHelloEvent.scheduled(), "nextHelloEvent is scheduled before HelloSimObject::startup is called!");
    schedule(nextHelloEvent, curTick() + 500);
}

void
HelloSimObject::processNextHelloEvent()
{
    std::cout << "tick: " << curTick() << ", Hello from HelloSimObject::processNextHelloEvent!" << std::endl;
    remainingHellosToPrintByEvent--;
    if (remainingHellosToPrintByEvent > 0) {
        schedule(nextHelloEvent, curTick() + 500);
    }
}

} // namespace gem5
